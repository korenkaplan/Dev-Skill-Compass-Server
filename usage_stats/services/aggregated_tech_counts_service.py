from typing import Any
from core.models import Categories, Roles
from init_db.data.data import get_top_categories_for_role_data
from init_db.init_database_functions import get_category_objects
from usage_stats.models import HistoricalTechCounts, MonthlyTechnologiesCounts, AggregatedTechCounts
from usage_stats.services.historical_tech_counts_service import get_tech_counts_from_last_number_of_months
from django.db.models import QuerySet
from utils.settings import NUMBER_OF_CATEGORIES, NUMBER_OF_ITEMS_PER_CATEGORY


def format_aggregated_tech_count(items: QuerySet[AggregatedTechCounts]):
    return [{'id': item.id, 'tech': item.technology_id.name, 'amount': item.counter, 'role': item.role_id.name}
            for item in items]


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

def get_role_count_stats(role_id: int, number_of_categories=NUMBER_OF_CATEGORIES, limit=NUMBER_OF_ITEMS_PER_CATEGORY):
    result = dict()

    # find the role
    role: Roles = Roles.objects.filter(pk=role_id).first()

    # get he queryset of categories from Data
    categories_str_list: list[str] = get_top_categories_for_role_data(role.name,
                                                                      number_of_categories)

    # get the categories objects
    categories_objects: list[Categories] = get_category_objects(categories_str_list)
    result['all categories'] = get_top_counts_overall(role.id, limit)
    # iterate through the categories and add to dictionary
    for category in categories_objects:
        # Get a formatted list of categories in dictionary
        category_role_count: list[dict] = get_top_count_for_role_category(role.id, category.id,
                                                                          limit)
        # add the category as key and the counts as value
        result[category.name] = category_role_count

    # return the duct
    return result


def get_last_scan_date_and_time():
    res: AggregatedTechCounts = AggregatedTechCounts.objects.all().order_by('-created_at').first()
    date, time = str(res.created_at.strftime("%d/%m/%y %H:%M")).split(' ')
    return {'date': date, 'time': time}


def get_top_count_for_role_category(role_id, category_id, limit=NUMBER_OF_ITEMS_PER_CATEGORY) -> list[dict]:
    res: QuerySet[AggregatedTechCounts] = AggregatedTechCounts.objects.filter(role_id=role_id,
                                                                              technology_id__category_id=category_id) \
                                              .order_by('-counter')[:limit]

    formatted_list = format_aggregated_tech_count(res)
    return formatted_list


def get_top_counts_overall(role_id: int, limit=NUMBER_OF_ITEMS_PER_CATEGORY):
    res: QuerySet[AggregatedTechCounts] = AggregatedTechCounts.objects.filter(role_id=role_id) \
                                                                            .order_by('-counter')[:limit]
    return format_aggregated_tech_count(res)
