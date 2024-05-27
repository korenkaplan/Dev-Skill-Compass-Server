# region WSGI INITIAL
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_server.settings')
application = get_wsgi_application()
# endregion
from logic.main_pipeline.main import (get_all_roles, get_all_techs_from_db, scrape_job_listings,
                                      extract_tech_words_from_job_listings, process_the_tech_words_from_analysis,
                                      update_the_database)
import json
from usage_stats.models import TechnologiesCounts
role = "Backend Developer"


def test_get_all_roles():
    roles = get_all_roles()
    print('test_get_all_roles: ', roles is not None and len(roles) > 10)
    return roles


def test_get_all_techs_from_db():
    techs = get_all_techs_from_db()
    print('test_get_all_techs_from_db: ', techs is not None and len(techs) > 500)
    return techs


def test_scrape_job_listings():
    listings = scrape_job_listings(role)
    print('test_scrape_job_listings: ', listings is not None and len(listings) > 5)
    return listings


def test_extract_tech_words_from_job_listings(listingss, tech_set):
    sets_lists = extract_tech_words_from_job_listings(listingss, tech_set)
    print('test_extract_tech_words_from_job_listings: ', sets_lists is not None and len(sets_lists) > 5)

    return sets_lists


def test_process_the_tech_words_from_analysis(sets_lists):
    res = process_the_tech_words_from_analysis(sets_lists, role)
    print('test_process_the_tech_words_from_analysis: ', res is not None and res[0] == role and len(res[1]) > 0)
    return res


def test_update_the_database(role_techs_tuple):
    update_the_database(role_techs_tuple)


def get_top_techs_for_role(role_id, count):
    technologies_counts = [tech for tech in TechnologiesCounts.objects.filter(role_id=role_id).order_by('-counter')[:10]]
    top_programming_languages = [tech for tech in technologies_counts if tech.technology_id.category_id.id == 1]

    for index, tech_count in enumerate(technologies_counts):
        legnth = 100
        name = tech_count.technology_id.name
        counter = tech_count.counter
        role = tech_count.role_id.name
        category = tech_count.technology_id.category_id.name
        part_a = f'Role: {role} | Category: {category} | Tech: {name} '
        remaining_length = legnth - len(part_a)
        part_b = " " * remaining_length + str(counter)
        print(str(f'{index+1}. ') + part_a + part_b)


if __name__ == '__main__':
    # roles = test_get_all_roles()
    # techs = test_get_all_techs_from_db()
    # listings = test_scrape_job_listings()
    # sets_list = test_extract_tech_words_from_job_listings(listings, techs)
    # tuple_tech = test_process_the_tech_words_from_analysis(sets_list)
    # test_update_the_database(tuple_tech)
    get_top_techs_for_role(3, 10)



