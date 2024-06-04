""" A service class for database interactions with MonthlyTechnologiesCounts table"""

from usage_stats.models import MonthlyTechnologiesCounts
from core.models import Roles, Technologies

"""
backend_developer : {
programming_language : {'python': 10,'js': 11},
databases: {'mysql':2, 'postgresql':4}
}
"""

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
    try:
        # Get the role id from db
        role = get_role_from_db(role_techs_tuple[0])
    except Exception as e:
        print(f"Error getting role from database for role '{role_techs_tuple[0]}': {e}")
        return

    # Get the technology id and update the count
    tech_categories_dict: dict[str, dict[str, int]] = role_techs_tuple[1]

    for category, tech_count_dict in tech_categories_dict.items():
        for tech_name, count in tech_count_dict.items():
            try:
                tech = get_technology_from_db(tech_name)
            except Exception as e:
                print(
                    f"Error getting technology from database for tech '{tech_name}': {e}"
                )
                continue

            try:
                update_count_of_technology_in_db(tech, role, count)
            except Exception as e:
                print(
                    f"Error updating count of technology '{tech_name}' for role '{role_techs_tuple[0]}': {e}"
                )
                continue


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
    tech_count_obj = MonthlyTechnologiesCounts.objects.filter(
        role_id=role, technology_id=tech
    ).first()

    # check if exists
    if tech_count_obj:
        tech_count_obj.counter += count
        tech_count_obj.save()
    # if not exist create
    else:
        MonthlyTechnologiesCounts.objects.create(
            role_id=role, technology_id=tech, counter=count
        )


# clear the table for monthly reset
def truncate_technologies_count_table():
    try:
        MonthlyTechnologiesCounts.objects.all().delete()
        print("Deleted all rows in table")
    except Exception as e:
        print("Error trunctating table: %s" % e)
