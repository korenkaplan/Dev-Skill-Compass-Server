"""
Module: tech_term_finder

A collection of functions to find technical terms in a given text.

Functions:
- remove_subsets(tech_list): Removes subsets from a list of technical terms.
- preprocess_text(text): Preprocesses the input text by converting it to lowercase and removing special characters,
                          numbers, and punctuation except for specific patterns like ci/cd, ui/ux.
- tokenize_text(text): Tokenizes the preprocessed text into words while preserving specific patterns like ci/cd, ui/ux.
- find_phrases(words, tech_set): Finds phrases from the tokenized words that match any terms in the provided tech set.
- find_tech_terms(text, tech_set): Finds technical terms in the input text based on the provided set of technical terms.
"""

import re
from data.skills_data import get_tech_set


def remove_subsets(tech_list):
    """
    Remove subsets from a list of technical terms.

    Parameters:
    tech_list (list): A list of technical terms.

    Returns:
    set: A set of technical terms with subsets removed.
    """
    cleaned_tech_set = set()  # Initialize an empty set to store cleaned tech words
    for i, tech_word in enumerate(tech_list):
        # Check if the current tech word is not a subset of any other tech word in the list
        if not any(
            tech_word != other_word and set(tech_word.split()).issubset(set(other_word.split()))
            for j, other_word in enumerate(tech_list) if i != j
        ):
            # If the current tech word is not a subset, add it to the cleaned set
            cleaned_tech_set.add(tech_word)
    return cleaned_tech_set


def preprocess_text(text):
    """
    Preprocess the input text by converting it to lowercase and removing special characters,
    numbers, and punctuation except for specific patterns like ci/cd, ui/ux.

    Parameters:
    text (str): The input text to preprocess.

    Returns:
    str: The preprocessed text.
    """
    # Convert text to lowercase
    text = text.lower()
    # Remove special characters, numbers, and punctuation except for specific patterns like ci/cd, ui/ux
    text = re.sub(r'[^a-z0-9\s/]', '', text)
    return text


def tokenize_text_with_slash(text):
    """
    Tokenize the preprocessed text into words while preserving specific patterns like ci/cd, ui/ux.

    Parameters:
    text (str): The preprocessed text.

    Returns:
    list: A list of tokenized words.
    """
    return re.findall(r'\b\w+(?:/\w+)?\b', text)


def tokenize_text(text):
    """
    Tokenize the preprocessed text into words while preserving specific patterns like ci/cd, ui/ux.

    Parameters:
    text (str): The preprocessed text.

    Returns:
    list: A list of tokenized words.
    """
    return re.findall(r'\b\w+\b', text)


def find_phrases(words, tech_set):
    """
    Find and return phrases from the tokenized words that match any terms in the provided tech set.

    Parameters:
    words (list): A list of tokenized words.
    tech_set (set): A set of technical terms to search for.

    Returns:
    list: A list of found technical terms from the input text.
    """
    found_phrases = []
    for i in range(len(words)):
        for j in range(i + 1, min(len(words) + 1, i + 4)):  # Adjust range for phrase length
            phrase = " ".join(words[i:j])
            if phrase in tech_set:
                found_phrases.append(phrase)
    return found_phrases


def find_tech_terms(text, tech_set):
    """
    Find technical terms in the input text based on the provided set of technical terms.

    Parameters:
    text (str): The input text to search for technical terms.
    tech_set (set): A set of technical terms to search for.

    Returns:
    list: A list of found technical terms from the input text.
    """
    # Preprocess the text
    preprocessed_text = preprocess_text(text)
    # Tokenize the text
    words = tokenize_text(preprocessed_text)
    # Find and return matching phrases
    found_tech_words = find_phrases(words, tech_set)
    return remove_subsets(found_tech_words)


if __name__ == '__main__':
    job = """Sightfull is a rapidly growing Revenue Analytics startup backed by top-tier VCs. Our platform helps SaaS companies quickly drive revenue growth by leveraging the full power of their real-time business data.
This is a rare opportunity to join a startup on the ground floor. You will join a small but powerful R&D team that is ambitious and dynamic. We take pride in creating a hugely impactful product that is being built at the highest level of craft and execution and is already delighting multiple customers.
Who are we looking for?
•	You are a positive problem solver with a can-do spirit, an autodidact, and enjoy working in a team
•	You are looking to make a significant impact on the company and its journey
•	You take pride in writing high-quality code with attention to product needs
What will you be doing?
•	As a senior backend engineer, you will take a central role in building Sightfull’s platform. You will have a real impact on our product and company.
•	You will choose and use cutting-edge technologies and methodologies.
•	You’ll take full ownership of new features by defining the need together with our PMs; designing and implementing scalable solutions for them, and improving them using immediate feedback from our users.
•	You will work on all parts of the platform – from our infrastructure, backend services and APIs.
Requirements
•	6+ Years of hands-on experience as a backend engineer
•	Experience in at least two modern runtimes/languages such as Node (Typescript/JavaScript), GoLang, Python, JVM-based (Java / Scala / Kotlin), etc.
•	Experience with AWS and/or GCP, preferably with k8s/ and container-based deployments
Advantages
•	Experience working in small startup companies
•	Experience working with modern data stacks, columnar databases and data processing
•	Experience with cloud platforms (e.g AWS, GCP, Azure)
•	Experience with contributing to open source code
•	Experience with modern CI/CD pipelines.
•	Github actions
•	Sql server
•	Microsoft sql server
•	Ux/ui
If your experience is close but doesn’t fulfill all requirements, please apply! We value talent and motivation and believe that specific knowledge will follow.
Our Tech Stack
 Our requirements are not limited to our current tech stack. However, because some are curious, our current tech stack is mainly composed of Node/Typescript, React/Typescript, Python, big-scale ETL, SQL, Columnar databases, GraphQL, Pulumi, Kubernetes, AWS, and many more :).

"""
    sett = get_tech_set()
    print(sorted(find_tech_terms(job, sett)))
