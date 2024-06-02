"""Module for initializing the database with initial data"""

import logging
import sys
from typing import List, Tuple
from core.models import Categories, Technologies, Roles, Synonyms


def _get_logger() -> logging.Logger:
    """
    Get a logger instance configured for logging to stdout and stderr.

    Returns:
        logging.Logger: A logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    return logger


def _extract_keys_from_dictionary(tech_dict: dict) -> List[str]:
    """
    Extract keys from a dictionary.

    Args:
        tech_dict (dict): The dictionary to extract keys from.

    Returns:
        list: A list of keys extracted from the dictionary.
    """
    return list(tech_dict.keys())


def _extract_tech_and_category_from_dictionary(
    tech_dict: dict, category_key: str
) -> Tuple[str, set]:
    """
    Extract technologies and category from a dictionary.

    Args:
        tech_dict (dict): The dictionary containing technologies.
        category_key (str): The key of the category to extract.

    Returns:
        tuple: A tuple containing the category name and a set of technologies.
    """
    tech_set = set(tech_dict[category_key].keys())
    return category_key, tech_set


def _insert_technologies_to_db_pipeline(tech_dict: dict) -> int:
    """
    Insert technologies into the database.

    Args:
        tech_dict (dict): A dictionary containing categories as keys and technologies as values.

    Returns:
        int: The total number of technologies inserted into the database.
    """
    logger = _get_logger()
    total_inserted = 0

    try:
        for category_key, techs_dict in tech_dict.items():
            category_id = Categories.objects.filter(name=category_key).first()
            if category_id:
                for tech_key in techs_dict.keys():
                    new_tech = Technologies.objects.create(
                        name=tech_key, category_id=category_id
                    )
                    if new_tech:
                        total_inserted += 1
            else:
                logger.warning("No Category found with the name: %s", category_key)

    except Exception as e:
        logger.error("Error occurred while inserting technologies: %s", str(e))

    return total_inserted


def _insert_roles_to_db(roles: List[str]) -> int:
    """
    Insert roles into the database.

    Args:
        roles (list): A list of role names to insert.

    Returns:
        int: The total number of roles inserted into the database.
    """
    logger = _get_logger()
    try:
        res = [Roles.objects.create(name=role) for role in roles]
        return len(res)
    except Exception as e:
        logger.error("Error occurred while inserting roles: %s", str(e))
        return 0


def _insert_categories_to_db(categories: List[str]) -> int:
    """
    Insert categories into the database.

    Args:
        categories (list): A list of category names to insert.

    Returns:
        int: The total number of categories inserted into the database.
    """
    logger = _get_logger()
    try:
        res = [Categories.objects.create(name=category) for category in categories]
        return len(res)
    except Exception as e:
        logger.error("Error occurred while inserting categories: %s", str(e))
        return 0


def _insert_synonyms_to_db(synonyms: set[str], technology: Technologies) -> int:
    logger = _get_logger()
    try:
        res = [
            Synonyms.objects.create(origin_tech_id=technology, name=synonym)
            for synonym in synonyms
        ]
        return len(res)
    except Exception as e:
        logger.error("Error occurred while inserting Synonyms: %s", str(e))
        return 0


def _insert_synonyms_to_db_pipeline(tech_dict: dict) -> int:
    logger = _get_logger()
    total_inserted = 0
    try:
        for category, synonyms_dict in tech_dict.items():
            for tech_name, synonyms_list in synonyms_dict.items():
                tech_object = Technologies.objects.filter(name=tech_name).first()
                total_inserted += _insert_synonyms_to_db(
                    set(synonyms_list), tech_object
                )
        return total_inserted

    except Exception as e:
        logger.error("Error occurred while inserting synonyms: %s", str(e))
        return 0


def initialize_pipeline(tech_dict: dict, roles: List[str]):
    """
    Initialize the database with initial data.

    Args:
        tech_dict (dict): A dictionary containing categories as keys and technologies as values.
        roles (list): A list of role names.

    Returns:
        None
    """
    logger = _get_logger()

    try:
        categories_keys: List[str] = _extract_keys_from_dictionary(tech_dict)

        insert_count_categories = _insert_categories_to_db(categories_keys)
        insert_count_roles = _insert_roles_to_db(roles)
        insert_count_techs = _insert_technologies_to_db_pipeline(tech_dict)
        insert_count_synonyms = _insert_synonyms_to_db_pipeline(tech_dict)
        result = f"""Total insert sum:
            Roles: {insert_count_roles}
            Categories: {insert_count_categories}
            Technologies: {insert_count_techs}
            Synonyms: {insert_count_synonyms}
"""
        logger.info(result)
        return result
    except Exception as e:
        return "Error occurred during database initialization: %s", str(e)
