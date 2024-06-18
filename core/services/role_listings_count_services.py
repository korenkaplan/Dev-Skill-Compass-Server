from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.utils import timezone
from core.models import RoleListingsCount, Roles
from utils.settings import NUMBER_OF_MONTHS_TO_AGGREGATE


def update_job_listings_count_table(job_listings_amount: int, role_name: str):
    now = timezone.now()
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    role = Roles.objects.filter(name=role_name).first()

    if not role:
        raise ValueError(f"Role with name {role_name} does not exist.")

    try:
        role_count_entry = RoleListingsCount.objects.filter(
            role_id=role,
            created_at__gte=current_month_start
        ).first()

        if role_count_entry:
            role_count_entry.counter += job_listings_amount
            role_count_entry.save()
        else:
            RoleListingsCount.objects.create(
                role_id=role,
                counter=job_listings_amount,
                created_at=timezone.now()  # Use current time to record the creation date accurately
            )
    except Exception as e:
        raise RuntimeError(f"(update_job_listings_count_table) error: {e}")


def get_job_listings_counts_from_last_number_of_months(role_id: int):
    try:
        role = Roles.objects.get(pk=role_id)
    except Roles.DoesNotExist:
        raise ValueError(f"Role with id {role_id} does not exist.")

    try:
        past_date = timezone.now() - relativedelta(months=NUMBER_OF_MONTHS_TO_AGGREGATE)

        # Get all the counts from the past date from all the months
        entries = RoleListingsCount.objects.filter(
            role_id=role,
            created_at__gte=past_date
        )

        # Sum the counts
        sum_of_counts = entries.aggregate(Sum('counter'))['counter__sum'] or 0

        return sum_of_counts
    except Exception as e:
        raise RuntimeError(f"(get_job_listings_counts_from_last_number_of_months) error: {e}")
