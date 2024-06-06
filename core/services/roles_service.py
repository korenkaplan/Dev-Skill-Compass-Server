from core.models import Roles, Categories
from init_db.data.data import get_top_categories_for_role_data
from init_db.init_database_functions import get_category_objects
from usage_stats.services.aggregated_tech_counts_service import get_top_count_for_role_category


def create_role(name: str):
    return Roles.objects.create(name=name)


def get_role_by_name(name: str) -> Roles:
    return Roles.objects.get(name=name)


def get_role_by_pk(id_to_find: int) -> Roles:
    return Roles.objects.get(id=id_to_find)


def get_top_categories_for_role(role_name, number_of_categories) -> list[Categories]:
    # get the roles dictionary
    categories_names_list = get_top_categories_for_role_data(role_name, number_of_categories)

    # get the categories objects
    categories_objects = get_category_objects(categories_names_list)

    return categories_objects


def get_top_counts_for_role_from_aggregated_counts(role_name: str, role_id: int, number_of_categories: int, limit=10):
    result = dict()

    # get the top categories objects for the role
    categories = get_top_categories_for_role(role_name, number_of_categories)

    # get the top count for each category & role combination
    for category in categories:
        result[category.name] = get_top_count_for_role_category(role_id, category.id, limit)

    return result
