from nltk.tokenize import word_tokenize
import math


def tf_idf_stat(corpus, unique_processed_words, processed_words, original_file, stemmer):
    """
    A method that calculates TF-IDF metric for each specified word.
    :parameter corpus: Path to the corpus of files.
    :parameter unique_processed_words - A set of stemmed and tokenized words (can not contain duplicates).
    :parameter processed_words - A list of stemmed and tokenized words (can contain duplicates).
    :parameter original_file - Path to the file specified by the user.
    :parameter stemmer: Stemmer used for stemming.
    :returns A dictionary which keys represent words, and their values represent TF-IDF metric of those words.
    """

    # Initialize an empty dictionary
    tf_df_idf_scores = {word: [0, 0, 0] for word in unique_processed_words}

    # Iterate through all the files in the corpus
    for file in corpus:
        # Check whether the current file is the same as the one which is already tokenized and stemmed
        if file != original_file:
            # If it is not, open the file
            with open(file, 'r', encoding='utf-8') as f:
                # Then read the file and save it's content
                current_file_content = f.read()
                # Tokenize words in the content of the current file
                current_file_content = word_tokenize(current_file_content)
                # Stem words and remove the ones that are not alphanumeric, then save them as a list
                current_file_content_processed = [stemmer.stem(word) for word in current_file_content if word.isalnum()]
                # Remove all duplicates
                current_file_content_processed = set(current_file_content_processed)

                for word in unique_processed_words:
                    # For every word for which the DF metric needs to be calculated, check whether that word is
                    # contained within the current file
                    if word in current_file_content_processed:
                        # If it is contained within the current file, increase it's DF metric by 1
                        tf_df_idf_scores[word][1] += 1
        else:
            # If the current file is the same as the one which is already tokenized and stemmed, just iterate the
            # DF value for each word, because it is surely there
            for word in unique_processed_words:
                tf_df_idf_scores[word][1] += 1

    # For every word for which the TF-IDF metric needs to be calculated
    for word in unique_processed_words:
        # Get and save TF metric in a dictionary
        tf_df_idf_scores[word][0] = processed_words.count(word)
        # Calculate the IDF metric of that word, based on the formula log(N/k(t)), where N is the number of documents in
        # the corpus, and k(t) is the number of documents that contain that word (or DF metric)
        idf = math.log(len(corpus) / tf_df_idf_scores[word][1])
        # Calculate and save the TF-IDF metric inside a dictionary
        tf_df_idf_scores[word][2] = tf_df_idf_scores[word][0] * idf

    # Save only words and their TF-IDF metrics inside the dictionary
    word_and_tfidf_score = {k: v[2] for k, v in tf_df_idf_scores.items()}
    # Sort dictionary by the TF-IDF metric of every word, and if there are words with the same TF-IDF metric values,
    # sort them lexicographically
    sorted_dict = sorted(word_and_tfidf_score.items(), key=lambda t: (-t[1], t[0]))
    # Transform a dictionary into a list of tuples, for easier access to the values
    final_words = [(tuple_word[0], tuple_word[1]) for tuple_word in sorted_dict]
    # Return dictionary of words and it's TF-IDF metric values, sorted by their TF-IDF metric values
    return {x[0]: x[1] for x in final_words}
