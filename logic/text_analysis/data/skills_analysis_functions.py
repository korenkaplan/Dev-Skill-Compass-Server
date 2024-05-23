from data import get_tech_dict

tech_dict = get_tech_dict()


def find_duplicate_words_with_lists():
    # Create a dictionary to store word counts and associated lists
    word_counts = {}

    # Iterate through each category in the dictionary
    for category, sub_dict in tech_dict.items():
        # Iterate through each sub-category list in the sub-dictionary
        for list_name, word_list in sub_dict.items():
            # Iterate through each word in the list
            for word in word_list:
                # If the word is already in the word_counts dictionary, update its count and add the list name
                if word in word_counts:
                    word_counts[word]['count'] += 1
                    word_counts[word]['lists'].append(category)
                # Otherwise, initialize the count for the word and store the list name
                else:
                    word_counts[word] = {'count': 1, 'lists': [category]}

    # Filter the word counts to get only the duplicates
    duplicate_counts = {word: info for word, info in word_counts.items() if info['count'] > 1}

    # Return the dictionary of duplicate word counts with associated lists
    return duplicate_counts


def find_word_in_dict(word):
    result = []
    for category, category_dict in tech_dict.items():
        for group_word, group_list in category_dict.items():
            if word in group_list:
                result.append({category, group_word})

    return result
