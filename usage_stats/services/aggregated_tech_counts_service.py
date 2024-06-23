from core.models import Categories, Roles
from init_db.data.data import get_top_categories_for_role_data
from init_db.init_database_functions import get_category_objects
from usage_stats.models import HistoricalTechCounts, MonthlyTechnologiesCounts, AggregatedTechCounts
from usage_stats.services.historical_tech_counts_service import get_tech_counts_from_last_number_of_months
from django.db.models import QuerySet
from utils.settings import NUMBER_OF_CATEGORIES, NUMBER_OF_ITEMS_PER_CATEGORY, NUMBER_OF_ITEMS_ALL_CATEGORIES
from typing import Tuple, List, Dict
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def update_count_aggregated_table(tech: int, role: Roles, count: int):
    #  Get the object from db
    tech_count_obj = AggregatedTechCounts.objects.filter(
        role_id=role, technology_id=tech
    ).first()

    # check if exists
    if tech_count_obj:
        tech_count_obj.counter += count
        tech_count_obj.save()
    # if not exist create
    else:
        AggregatedTechCounts.objects.create(
            role_id=role, technology_id=tech, counter=count
        )


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

    # Get the historical data from last X months
    historical_counts_objects = get_tech_counts_from_last_number_of_months(number_of_months)

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

def get_role_count_stats(role_id: int, number_of_categories=NUMBER_OF_CATEGORIES,
                         limit=NUMBER_OF_ITEMS_PER_CATEGORY,
                         all_categories_limit=NUMBER_OF_ITEMS_ALL_CATEGORIES) -> dict:
    """
    Get the count statistics for a role across multiple categories.

    Args:
        role_id (int): The ID of the role.
        number_of_categories (int): The number of top categories to retrieve.
        limit (int): The limit of items per category.
        all_categories_limit (int): The limit of items for all categories category.
    Returns:
        dict: A dictionary containing the overall top counts and category-specific counts.
    """
    result = {}

    try:
        # Find the role
        role: Roles = Roles.objects.get(pk=role_id)
    except Roles.DoesNotExist:
        raise ValueError(f"Role with id {role_id} does not exist.")

    try:
        # Set the overall top counts for all categories
        result['all categories'] = get_top_counts_overall(role.id, all_categories_limit)
    except Exception as e:
        raise RuntimeError(f"({role.name}) Error fetching overall top counts for role {role.id}: {e}")

    categories: QuerySet[Categories] = Categories.objects.all()
    try:
        # Initialize dictionaries to store valid and not valid category counts
        valid_categories_counts = {}
        not_valid_categories_counts = {}

        # Gather counts for all categories
        for category in categories:

            try:
                # Get the top count list for this role-category combination
                category_role_count: list[dict] = get_top_count_for_role_category(role.id, category.id, limit)
            except Exception as e:
                raise RuntimeError(f"Error fetching top count for role {role.id} and category {category.id}: {e}")

            if len(category_role_count) >= limit:
                valid_categories_counts[category.name] = category_role_count
            else:
                not_valid_categories_counts[category.name] = category_role_count

        # Sort all categories by list length and first item amount
        sorted_valid_counts = get_sorted_dict_based_on_list_length(valid_categories_counts)

        # Check first if there is enough valid categories before sorting the not valid categories
        if len(sorted_valid_counts) >= number_of_categories:
            # Convert the dictionary to a list of tuples (key, value)
            sorted_valid_list = list(sorted_valid_counts.items())
            # Slice the list to get the first number_of_categories items
            sliced_valid_dict = dict(sorted_valid_list[:number_of_categories])
            result.update(sliced_valid_dict)
            return result

        sorted_invalid_counts = get_sorted_dict_based_on_list_length(not_valid_categories_counts)
        # Merge sorted valid and invalid counts into result
        result.update(sorted_valid_counts)
        result.update(sorted_invalid_counts)

    except Exception as e:
        raise RuntimeError(f"({role.name}) Error processing category counts: {e}")

    result_list = list(result.items())
    return dict(result_list[:number_of_categories])


def fill_with_valid_counts(result_dict: dict, categories_str_list: list[str],
                           role: Roles, number_of_categories: int, limit: int) -> Tuple[dict, dict, int, bool]:
    """
    Fill the result dictionary with valid category counts.

    Args:
        result_dict (dict): The result dictionary to fill.
        categories_str_list (list[str]): List of category names.
        role (Roles): The role object.
        number_of_categories (int): Number of valid categories needed.
        limit (int): Limit of items per category.

    Returns:
        tuple: A tuple containing the result dictionary, not valid categories counts,
        valid categories count, and a boolean indicating if the result is filled.
    """
    valid_categories_count = 0
    not_valid_categories_counts = {}
    is_filled = False

    for category_name in categories_str_list:
        try:
            category = Categories.objects.get(name=category_name)
        except Categories.DoesNotExist:
            continue

        try:
            # Get the top count list for this role-category combination
            category_role_count: list[dict] = get_top_count_for_role_category(role.id, category.id, limit)
        except Exception as e:
            raise RuntimeError(f"Error fetching top count for role {role.id} and category {category.id}: {e}")

        if len(category_role_count) >= limit:
            result_dict[category.name] = category_role_count
            valid_categories_count += 1
        else:
            not_valid_categories_counts[category.name] = category_role_count

        if valid_categories_count >= number_of_categories:
            is_filled = True
            break

    return result_dict, not_valid_categories_counts, valid_categories_count, is_filled


def fill_with_invalid_counts(result_dict: dict, not_valid_counts_dict: dict,
                             valid_categories_count: int, max_num_of_valid_categories: int) -> dict:
    """
    Fill the result dictionary with invalid category counts.

    Args:
        result_dict (dict): The result dictionary to fill.
        not_valid_counts_dict (dict): Dictionary of invalid category counts.
        valid_categories_count (int): Current number of valid categories.
        max_num_of_valid_categories (int): Maximum number of valid categories needed.

    Returns:
        dict: The updated result dictionary.
    """
    sorted_not_valid_counts_dict = get_sorted_dict_based_on_list_length(not_valid_counts_dict)

    for key, value in sorted_not_valid_counts_dict.items():
        result_dict[key] = value
        valid_categories_count += 1

        if valid_categories_count >= max_num_of_valid_categories:
            break

    return result_dict


def get_sorted_dict_based_on_list_length(dict_to_sort: Dict[str, List[dict]]) -> Dict[str, List[dict]]:
    """
    Sort a dictionary by the length of its lists in descending order and by the highest 'amount' value in each list.

    Args:
        dict_to_sort (dict): The dictionary to sort.

    Returns:
        dict: The sorted dictionary.
    """

    def list_sort_key(item):
        # Check if the list is empty
        if item[1]:  # Check if list is not empty
            # Sort key: (-len(item[1]), -item[1][0]['amount'])
            # -len(item[1]) sorts by descending length of the list
            # -item[1][0]['amount'] sorts by descending 'amount' value of the first item in the list
            return -item[1][0].get('amount', 0), -len(item[1])
        else:
            # If the list is empty, ensure it is placed at the end
            return 0, 0

    sorted_dict = dict(sorted(dict_to_sort.items(), key=list_sort_key))
    return sorted_dict


def get_last_scan_date_and_time():
    res: AggregatedTechCounts = AggregatedTechCounts.objects.all().order_by('-created_at').first()
    created_at = res.created_at + relativedelta(hours=3)
    date, time = str(created_at.strftime("%d/%m/%y %H:%M")).split(' ')
    return {'date': date, 'time': time}


def get_top_count_for_role_category(role_id, category_id, limit=NUMBER_OF_ITEMS_PER_CATEGORY) -> list[dict]:
    res = AggregatedTechCounts.objects.filter(role_id=role_id,
                                              technology_id__category_id=category_id).order_by('-counter')[:limit]

    formatted_list = format_aggregated_tech_count(res)
    return formatted_list


def get_top_counts_overall(role_id: int, limit=NUMBER_OF_ITEMS_PER_CATEGORY):
    res = AggregatedTechCounts.objects.filter(role_id=role_id).order_by('-counter')[:limit]
    return format_aggregated_tech_count(res)


def get_role_count_stats_copy(role_id: int, number_of_categories=NUMBER_OF_CATEGORIES,
                              limit=NUMBER_OF_ITEMS_PER_CATEGORY):
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
