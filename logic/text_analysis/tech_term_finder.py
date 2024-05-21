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
from concurrent.futures import ThreadPoolExecutor
from logic.text_analysis.data.skills_data import get_tech_set


def remove_subsets(tech_list: list) -> set:
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


def preprocess_text(text: str) -> str:
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
    text = re.sub(r'[^a-z0-9\s/#]', '', text)
    return text.strip()


def tokenize_text_with_slash(text: str) -> list[str]:
    """
    Tokenize the preprocessed text into words while preserving specific patterns like ci/cd, ui/ux.

    Parameters:
    text (str): The preprocessed text.

    Returns:
    list: A list of tokenized words.
    """
    return re.findall(r'\b\w+(?:/\w+)?\b', text)


def tokenize_text(text: str) -> list[str]:
    """
  Tokenize the preprocessed text into words while preserving specific patterns like ci/cd, ui/ux.

  Parameters:
  text (str): The preprocessed text.

  Returns:
  list: A list of tokenized words.
  """
    return re.findall(r'\b\w+#|#\w+|\b\w+\b|\'\w+', text)


def find_phrases(words, tech_set: set) -> list[str]:
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


def find_tech_terms(text: str, tech_set: set) -> set:
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


def find_tech_terms_pool_threads(listings_list: list[str], tech_set: set) -> list[list[str]]:
    """Handle multiple listings with thread pool simultaneously"""
    result = []
    # start the thread pool
    with ThreadPoolExecutor(max_workers=len(listings_list)) as executor:
        # submit task for each listing
        futures = [executor.submit(find_tech_terms, listing, tech_set) for listing in listings_list]

        # collect and store results from all tasks
        for future in futures:
            print(future.result())
            result.append(future.result())

    return result



sample_data_developer_job_listings = [
    "Backend Engineer (Python/Django): Build and maintain scalable web applications using Python and Django framework. (RESTful API, Databases)",
    "Node.js Developer (Social Media): Develop real-time features and backend services for a high-traffic social media platform. (JavaScript, express.js, MongoDB)",
    "Java Backend Developer (FinTech): Create secure and reliable backend systems for financial transactions. (Spring Boot, Java EE, Microservices)",
    "Go Developer (Cloud Infrastructure): Develop and maintain backend services for a cloud platform using Go. (Concurrency, Postgresql)",
    "DevOps Engineer (E-commerce): Automate infrastructure provisioning and integrate development and deployment processes. (Linux, K8's, Docker)",
    "API Developer (Healthcare): Develop secure and well-documented APIs for healthcare data exchange. (RESTful APIs, OAuth, Security)",
    "Backend Developer (Machine Learning): Build backend infrastructure to support machine learning models and data pipelines. (Python, TensorFlow, Cloud Storage)",
    "Software Engineer (Embedded Systems): Develop low-level software for interacting with hardware components. (C/C++, Assembly)",
    "Front-End Developer (React/JS): Build interactive and user-friendly web interfaces using React and JavaScript. (HTML, CSS, UI/UX Design)",
    "Angular Developer (E-commerce): Develop single-page applications for an e-commerce platform using Angular. (TypeScript, RxJS)",
    "UI/UX Designer & Front-End Developer (Mobile App): Design and develop user interfaces for a mobile application. (React Native/Flutter, UI/UX Best Practices)",
    "Front-End Developer (VR/AR): Develop interactive front-end experiences for virtual and augmented reality platforms. (WebGL, Three.js)",
    "Front-End Developer (SSR): Build server-side rendered web applications for improved SEO and performance. (Next.js, Nuxt.js)",
  ]

myset = get_tech_set()
find_tech_terms_pool_threads(sample_data_developer_job_listings, myset)
