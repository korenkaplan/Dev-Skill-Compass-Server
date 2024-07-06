import time
from django.core.management.base import BaseCommand

from core.models import Technologies, Roles
from decorators.decorator_measure_function_time import measure_function_time
from utils.functions import retry_function
import os
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.utils import timezone
from usage_stats.models import MonthlyTechnologiesCounts, AggregatedTechCounts, HistoricalTechCounts
from utils.functions import write_text_to_file
from utils.settings import NUMBER_OF_MONTHS_TO_AGGREGATE
from django.db import transaction

# Determine the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the log file
log_file_path = os.path.join(project_root, "Logs", "monthly_pipeline.log.txt")


class Command(BaseCommand):
    help = "Run the main pipeline"

    @measure_function_time
    def handle(self, *args, **options):
        # Call your initialization function here
        retry_function(monthly_pipeline, role_name='monthly_pipeline')
        # process_pool_role_pipline()
        self.stdout.write("run_monthly_pipeline command executed")


@transaction.atomic
def monthly_pipeline():
    """
    Executes the monthly pipeline to move data from the MonthlyTechnologiesCounts table to
    the HistoricalTechCounts table,
    and updates the aggregated counts table with the latest data from the last `number_of_months` months.

    Raises:
        ValueError: If `number_of_months` is not a positive integer.
    """
    print("Started Monthly pipeline")
    number_of_months = NUMBER_OF_MONTHS_TO_AGGREGATE
    if number_of_months <= 0:
        raise ValueError("number_of_months must be a positive integer")

    try:
        # Get all the rows from the monthly tech counts table
        technology_counts = MonthlyTechnologiesCounts.objects.all()

        print("Started creating HistoricalTechCounts object from MonthlyTechnologiesCounts rows...")

        # Prepare data for bulk insert into HistoricalTechCounts
        historical_insert_data = [
            HistoricalTechCounts(
                technology_id=row.technology_id,
                role_id=row.role_id,
                counter=row.counter
            )
            for row in technology_counts
        ]

        print("Started creating HistoricalTechCounts objects in the database...")
        # Bulk insert into HistoricalTechCounts
        HistoricalTechCounts.objects.bulk_create(historical_insert_data)

        print("Started truncating table MonthlyTechnologiesCounts ...")
        # Truncate the monthly stats table
        MonthlyTechnologiesCounts.objects.all().delete()

        print("Started truncating table AggregatedTechCounts ...")
        # Truncate the aggregated stats table
        AggregatedTechCounts.objects.all().delete()

        # Calculate past date
        today = timezone.now()
        past_date = today - relativedelta(months=number_of_months)

        # Aggregate and insert into AggregatedTechCounts
        print("Started Aggregate counts by role_id and technology_id from HistoricalTechCounts...")
        start_time = time.time()
        # Aggregate counts by role_id and technology_id
        aggregated_data = HistoricalTechCounts.objects.filter(created_at__gte=past_date).values('role_id',
                                                                                                'technology_id').annotate(
            total_counter=Sum('counter'))

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"HistoricalTechCounts aggregation executed in {execution_time:.2f} seconds")

        # Fetch all relevant Technologies and Roles in batches
        technology_ids = set(item['technology_id'] for item in aggregated_data)
        role_ids = set(item['role_id'] for item in aggregated_data)

        technologies = Technologies.objects.filter(id__in=technology_ids)
        roles = Roles.objects.filter(id__in=role_ids)

        # Create lookup dictionaries for quick access
        technology_map = {tech.id: tech for tech in technologies}
        role_map = {role.id: role for role in roles}

        counter = 0
        total_rows = len(aggregated_data)
        aggregated_insert_data = []

        print("Started creating the AggregatedTechCounts objects...")
        for item in aggregated_data:
            counter += 1
            progress_message = f"Processing row {counter}/{total_rows}"
            print(f"\r{progress_message}", end="", flush=True)

            # Fetch Technologies and Roles objects using the pre-built maps
            technology = technology_map.get(item['technology_id'])
            role = role_map.get(item['role_id'])

            # Create AggregatedTechCounts instance and append to list
            aggregated_instance = AggregatedTechCounts(
                technology_id=technology,
                role_id=role,
                counter=item['total_counter']
            )
            aggregated_insert_data.append(aggregated_instance)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"AggregatedTechCounts creation executed in {execution_time:.2f} seconds")
        print("Started Bulk insert into AggregatedTechCounts...")

        # Bulk insert into AggregatedTechCounts
        AggregatedTechCounts.objects.bulk_create(aggregated_insert_data)

        print("Finished monthly pipeline")

    except Exception as e:
        # Log the error or handle it as needed
        message = f"An error occurred during the monthly pipeline: {e}"
        print(message)
        write_text_to_file(log_file_path, 'a', message)
        # Rollback transaction on error
        transaction.set_rollback(True)
