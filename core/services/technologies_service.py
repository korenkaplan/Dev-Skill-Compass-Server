from collections import defaultdict
from core.models import Technologies, Categories, Roles, Synonyms
from usage_stats.models import MonthlyTechnologiesCounts


def get_tech_dict() -> dict:
    # create a dict
    result_dict = defaultdict(lambda: defaultdict(list))
    # Get all technologies
    technologies: list[Technologies] = Technologies.objects.all()
    # iterate through the technologies and get all the synonyms of the technology
    for technology in technologies:
        # get all the synonyms of the technology
        synonyms: list[str] = [
            synonym.name
            for synonym in Synonyms.objects.filter(origin_tech_id=technology)
        ]
        # get the category of the technology
        category: Categories = technology.category_id
        # add to dictionary
        result_dict[category.name][technology.name] = synonyms

    return result_dict


def get_count_of_technologies_for_role(role_name: str) -> dict:
    # create a dict
    result_dict = defaultdict(lambda: defaultdict(dict))
    # verify the role
    role = Roles.objects.filter(name=role_name).first()
    if role is None:
        raise ValueError("No such role: %s" % role)
    # get the technologies for this role
    role_tech_counts: list[MonthlyTechnologiesCounts] = MonthlyTechnologiesCounts.objects.filter(
        role_id=role
    )
    # create the keys from the technologies
    for tech_count_row in role_tech_counts:
        # get the technology from the row
        technology_obj: Technologies = tech_count_row.technology_id
        # get the category from the technology
        category_obj: Categories = technology_obj.category_id
        # create the dictionary
        result_dict[role.name][category_obj.name][
            technology_obj.name
        ] = tech_count_row.counter

    # return the dictionary result
    return result_dict
