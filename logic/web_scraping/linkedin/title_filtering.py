"""This module is responsible for checking if the title of the listing match the role searched for"""
from init_db.data.data import get_words_to_remove_from_title, get_synonyms_words_title
import re


# region Sub Functions
def format_role_title(title: str) -> str:
    # remove everything beside letters
    only_letters_regex_pattern = r"[^a-zA-Z]"
    result = re.sub(only_letters_regex_pattern, "", title)
    return result



def remove_words(text: str, words: list) -> str:
    # remove all the common words
    for word in words:
        text = text.replace(word, "").strip()
        text = text.replace(" ", "")

    return text


def remove_non_letters_characters(text: str) -> str:
    # remove everything beside letters
    only_letters_regex_pattern = r"[^a-zA-Z]"
    result = re.sub(only_letters_regex_pattern, "", text)
    return result


def is_title_in_synonyms_words(role: str, clean_title: str) -> bool:
    # get the synonyms words for the role
    synonyms_words: list[str] = get_synonyms_words_title(role)

    # clean the words (remove spaces and to lower and signs)
    formatted_words: list[str] = [word.replace(" ", "").lower().strip() for word in synonyms_words]

    # compare each clean word against the cleaned title
    for word in formatted_words:
        if word in clean_title:
            return True
    # return false if not found
    return False

# endregion


def is_title_match_role(role: str, title: str) -> bool:
    try:
        # Get the words to remove from the title by role
        words_to_remove = get_words_to_remove_from_title(role)

        # Remove the words from the title
        cleaned_title = remove_words(title.lower(), words_to_remove)
        cleaned_role = remove_words(role.lower(), words_to_remove)

        # Clean the non alphabet letters
        cleaned_role = remove_non_letters_characters(cleaned_role)
        cleaned_title = remove_non_letters_characters(cleaned_title)

        # Check if the cleaned role is in the cleaned title
        res = cleaned_role in cleaned_title
        if res is False:
            res = is_title_in_synonyms_words(role, cleaned_title)

        if res is False:
            print(f"""False match: {cleaned_title}({title} <-> {cleaned_role}({role})""")

        return res
    except Exception as e:
        print(f"Function is_title_match_role error: {e}")
        return False
