from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize
from utils.list_files import list_of_files
from nltk.tokenize import word_tokenize
from tf_idf import tf_idf_stat


if __name__ == '__main__':

    # Receive the input from the user
    corpus_folder_path = input('Insert the path to the corpus: ')
    filepath = input('Insert the path for the file that needs to be summarized: ')

    # Setup the stemmer
    stemmer = SnowballStemmer('english')

    # Get the content of the file specified by the user
    content_of_file = ''
    with open(filepath, 'r', encoding='utf-8') as file:
        content_of_file += file.read()

    # Get the paths for every text file in the folder (corpus)
    corpus = list_of_files(corpus_folder_path)

    # Tokenize, filter non-alphanumeric and stem the words in the content of the specified file
    words = [stemmer.stem(x) for x in word_tokenize(content_of_file) if x.isalnum()]

    # Get all words inside the file content and their TF-IDF metric values
    words_and_scores = tf_idf_stat(corpus, set(words), words, filepath, stemmer)

    print('Keywords:')
    # Print the top 10 words with the greatest TF-IDF score
    print(', '.join(list(words_and_scores.keys())[:10]))

    # Tokenize the sentences
    sentences = sent_tokenize(content_of_file)

    # If there is less then 5 sentences inside the file, print them all
    if len(sentences) <= 5:
        print(content_of_file)
    else:
        # Else, firstly initialize an empty dictionary
        sentences_and_scores = {}

        # For every sentence in the file
        for sentence in sentences:

            # Initialize it's TF-IDF metric to 0
            sentences_and_scores[sentence] = 0

            # Tokenize all words in the current sentence
            token_words = word_tokenize(sentence)

            # Stem and filter non-alphabetic words in the tokenized words
            stemmed_tokenized_sentence = [stemmer.stem(x) for x in token_words if x.isalnum()]

            # Sort words in the sentence, firstly descending by the TF-IDF metric values of it's words, then
            # lexicographically if there are words with the same TF-IDF metric values
            stemmed_tokenized_sentence = sorted(stemmed_tokenized_sentence, key=lambda e: (-words_and_scores[e], e))

            # Calculate the TF-IDF score for the current sentence based on the sum of it's top 10 most relevant words
            # (words with the greatest TF-IDF metric values)
            for word in stemmed_tokenized_sentence[:10]:
                sentences_and_scores[sentence] += words_and_scores[word]

        # Get the top 5 sentences and their TF-IDF metric values by their TF-IDF metric values
        sentences_with_top_value = sorted(sentences_and_scores.items(), key=lambda t: -t[1])[:5]

        # Save only top 5 sentences, without it's TF-IDF metric values
        top_sentences = [tuple_sentence[0] for tuple_sentence in sentences_with_top_value]

        # For every sentence in the file content
        task2_final = []
        for sentence in sentences:
            # If top 5 sentences are found, break out the loop
            if len(task2_final) > 5:
                break
            else:
                # Else, if top 5 sentences are not found, check whether the current sentence is inside the top 5
                if sentence in top_sentences:
                    # If it is, append it to the final list
                    task2_final.append(sentence)
        print('Summarized document:')
        # Print the final list (summary of the document)
        print(' '.join(task2_final))
