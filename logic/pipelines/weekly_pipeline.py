from logic.pipelines.main import process_pool_role_pipline_test
from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
from usage_stats.models import MonthlyTechnologiesCounts, AggregatedTechCounts
from usage_stats.services.aggregated_tech_counts_service import insert_from_monthly_table
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def weekly_pipeline():
    period: GoogleJobsTimePeriod = GoogleJobsTimePeriod.WEEK
    # Run the main pipline with the period time set to one week
    process_pool_role_pipline_test(period)

    # get the min date
    today = timezone.now()
    past_date = today - relativedelta(days=1)

    # get the monthly counts from last scan
    items: list[MonthlyTechnologiesCounts] = MonthlyTechnologiesCounts.objects.filter(created_at__gte=past_date)

    # Update the aggregated table
    inserted_items: list[AggregatedTechCounts] = insert_from_monthly_table(items)

    print(f"Is all inserted successfully: {len(inserted_items) == len(items)}")

