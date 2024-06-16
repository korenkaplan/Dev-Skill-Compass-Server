# region WSGI
"""
WSGI config for django_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")

application = get_wsgi_application()
# endregion

from collections import defaultdict
from django.db.models import QuerySet
from core.models import Technologies, Categories, Roles, Synonyms
from usage_stats.models import MonthlyTechnologiesCounts


def get_tech_dict():
    # Create a nested defaultdict
    result_dict = defaultdict(lambda: defaultdict(list))

    # Get all technologies and synonyms at once
    technologies: QuerySet[Technologies] = Technologies.objects.select_related('category_id').all()
    synonyms: QuerySet[Synonyms] = Synonyms.objects.all()
    # Create a dictionary to map technology IDs to their synonyms
    synonyms_dict = defaultdict(list)
    for synonym in synonyms:
        synonyms_dict[synonym.origin_tech_id_id].append(synonym.name)

    # Iterate through technologies to build the result dictionary
    for technology in technologies:
        category_name = technology.category_id.name
        technology_name = technology.name
        tech_synonyms = synonyms_dict.get(technology.id, [])
        result_dict[category_name][technology_name] = tech_synonyms

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


