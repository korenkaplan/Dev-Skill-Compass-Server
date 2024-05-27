""" A service class for database interactions with TechnologiesCounts table"""
from usage_stats.models import TechnologiesCounts
from core.models import Roles, Technologies

"""
  expected_result = {
        "backend developer": {
            "databases": {
                "postgresql": 2,
                "sqlite": 1,
                "redis": 1
            },
            "web_frameworks": {
                "node.js": 1,
                "django": 1,
                "spring boot": 1
            },
            "programming_languages": {
                "typescript": 2,
                "python": 1,
                "java": 1
            }
        }
"""


def update_technologies_counts_table_in_db_pipeline(role_techs_tuple: (str, dict)):
    # Get the role id from db
    role = get_role_from_db(role_techs_tuple[0])

    # Get the technology id and update the count
    tech_categories_dict: dict[str, dict[str, int]] = role_techs_tuple[1]
    for category, tech_count_dict in tech_categories_dict.items():
        for tech_name, count in tech_count_dict.items():
            tech = get_technology_from_db(tech_name)
            update_count_of_technology_in_db(tech, role, count)


# Get the role id from db
def get_role_from_db(role: str):
    role = Roles.objects.filter(name=role).first()
    return role


# Get the technology id form db
def get_technology_from_db(tech_name: str):
    tech = Technologies.objects.filter(name=tech_name).first()
    return tech


# update the count of the technology
def update_count_of_technology_in_db(tech: int, role: Roles, count: int):
    #  Get the object from db
    tech_count_obj = TechnologiesCounts.objects.filter(role_id=role, technology_id=tech).first()

    # check if exists
    if tech_count_obj:
        tech_count_obj.counter += count
        tech_count_obj.save()
    # if not exist create
    else:
        new_tech_count = TechnologiesCounts.objects.create(role_id=role, technology_id=tech, counter=count)
