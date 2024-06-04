from core.models import Categories
from usage_stats.models import HistoricalTechCounts, MonthlyTechnologiesCounts, AggregatedTechCounts
from usage_stats.services.historical_tech_counts_service import get_tech_counts_from_last_number_of_months


def format_aggregated_tech_count(items: list[AggregatedTechCounts]):
    return [{'ID': item.id, 'Tech': item.technology_id.name, 'Amount': item.counter, 'Role': item.role_id.name,
             'Created At': item.created_at.strftime('%d/%m/%Y')} for item in items]


def truncate_table():
    AggregatedTechCounts.objects.all().delete()


def insert_from_historical_table(items: list[HistoricalTechCounts]) -> list[AggregatedTechCounts]:
    result = []
    for item in items:
        exist_obj: HistoricalTechCounts = AggregatedTechCounts.objects.filter(technology_id=item.technology_id,
                                                                              role_id=item.role_id).first()

        if exist_obj:
            exist_obj.counter += item.counter
            exist_obj.save()
        else:
            obj = AggregatedTechCounts.objects.create(technology_id=item.technology_id, role_id=item.role_id,
                                                      counter=item.counter)
            result.append(obj)

    return result


def insert_from_monthly_table(items: list[MonthlyTechnologiesCounts]) -> list[AggregatedTechCounts]:
    result = []
    for item in items:
        exist_obj: AggregatedTechCounts = AggregatedTechCounts.objects.filter(technology_id=item.technology_id,
                                                                              role_id=item.role_id).first()

        if exist_obj:
            exist_obj.counter += item.counter
            exist_obj.save()
        else:
            obj = AggregatedTechCounts.objects.create(technology_id=item.technology_id, role_id=item.role_id,
                                                      counter=item.counter)
            result.append(obj)

    return result


def refresh_aggregated_table(number_of_months: int):
    # Clear the table
    truncate_table()

    # Get all from monthly counts
    monthly_counts_objects = MonthlyTechnologiesCounts.objects.all()

    # Get the historical data from last X months
    historical_counts_objects = get_tech_counts_from_last_number_of_months(number_of_months)

    # insert into the table
    if monthly_counts_objects:
        objects_inserted_from_monthly_table = insert_from_monthly_table(monthly_counts_objects)
        print(f"Total inserted from Monthly table: {len(objects_inserted_from_monthly_table)}")
    if historical_counts_objects:
        objects_inserted_from_historical_table = insert_from_historical_table(historical_counts_objects)
        print(f"Total inserted from Monthly table: {len(objects_inserted_from_historical_table)}")


# region ===================== Endpoints functions================================


def get_top_category_for_role(role: str):
    items = AggregatedTechCounts.objects.filter(role_id__name=role,
                                                technology_id__category_id__name='programming_languages').order_by(
        '-counter')[:10]
    return format_aggregated_tech_count(items)


def get_top_by_category_role(role: str, categories: list[str], limit=-1):
    if limit is None or limit < 0:
        limit = 10
    result_dict = dict()

    if categories[0].lower() == 'all':
        categories = [category.name for category in Categories.objects.all()]

    for category in categories:
        items = AggregatedTechCounts.objects.filter(
            role_id__name=role,
            technology_id__category_id__name=category).order_by('-counter')[:limit]

        if items is not None and len(items) > 0:
            formatted_items = format_aggregated_tech_count(items)
            result_dict[category] = formatted_items

    return result_dict
# endregion
