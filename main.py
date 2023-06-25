from collections import Counter
from nltk.corpus import stopwords
import nltk
from nltk.stem import PorterStemmer

FILE_PATH = "input1.txt"
STOP_WORDS = "stop_words.txt"
STEMMER = PorterStemmer()
nltk.download("stopwords")
NLTK_STOP_WORDS = stopwords.words('english')

def read_file_and_split_sentences_or_words(file_path, split):
    """
    A function to read a passage of text in a text file
    and split the text either by words of sentence
    depending on the input
    """
    with open(file_path) as file:
        text_file = file.read()
        if split == "by_word":
            text = text_file.split()
        else:
            text = text_file.split(".")
        return text

def read_stop_words_file(file_path):
    """
    A function to read a text file which
    contains words that we do not
    want to appear in the list of
    words as they are not interesting.
    """
    with open(file_path) as file:
        text_file = file.readlines()
        stop_words = []
        for line in text_file:
            line = line.strip('\n')
            stop_words.append(line)
    return stop_words


def make_words_lower_case(words):
    """
    A function that makes all words
    in a list lower case and strips
    out unnecessary characters.
    """
    lower_case_words = []
    for word in words:
        format_word = word.lower().strip(".").strip(':').strip(",").strip(';')
        lower_case_words.append(format_word)

    return lower_case_words

def remove_none_interesting_words(lower_case_words):
    """
    A function to remove none interesting words
    that appear in the NLTK toolkit and the stop
    words text.
    """
    words_of_interest = []
    for word in lower_case_words:
        if word not in NLTK_STOP_WORDS:
            if word not in additional_stop_words:
                words_of_interest.append(word)

    return words_of_interest

def get_stem_of_words(words_of_interest):
    """
    This will get the stem of a word
    so that it is easier to determine
    whether particular variations
    of a word appear in the text.
    """
    stemmed_words = []
    for word in words_of_interest:
        stemmed_word = STEMMER.stem(word)
        stemmed_words.append(stemmed_word)
    return stemmed_words

def get_interesting_words(top_10_words, top_10_stemmed_words, word_type):
    """
    This will return the most interesting words
    """

    list_of_interesting_words = []
    list_of_interesting_stemmed_words = []

    for word, num in top_10_words:
        for stemmed_word, stem_num in top_10_stemmed_words:
            if word.startswith(stemmed_word):
                list_of_interesting_words.append(word)
                list_of_interesting_stemmed_words.append(stemmed_word)

    if word_type == "stemmed":
        return list_of_interesting_stemmed_words
    else:
        return list_of_interesting_words

def find_salient_sentence_to_summarise_text(sentences):
    """
    This will determine which sentence is most
    interesting based on how many interesting words
    appear in it.
    """
    sentence_to_check = ''
    count_num_of_stemmed_words_in_sentence = 0

    for sentence in sentences:
        count = 0
        for stem in list_of_interesting_stemmed_words:
            if stem in sentence:
                count += 1
        if count > count_num_of_stemmed_words_in_sentence:
            count_num_of_stemmed_words_in_sentence = count
            sentence_to_check = sentence

    return sentence_to_check


# Reading words and sentences from a text file and reading words
# from a file that we want to exclude from the text
words = read_file_and_split_sentences_or_words(FILE_PATH, "by_word")
sentences = read_file_and_split_sentences_or_words(FILE_PATH, "by_sentence")
additional_stop_words = read_stop_words_file(STOP_WORDS)


# Formatted the words, getting words of intetest and the stem of interesting words
lower_case_words = make_words_lower_case(words)
words_of_interest = remove_none_interesting_words(lower_case_words)
stemmed_words = get_stem_of_words(words_of_interest)

# Counting the number of times the word and a stemmed word appears and then sorting these by
# the top 10 appearances
appearances_of_words = Counter(words_of_interest)
top_10_words = sorted(appearances_of_words.items(), key=lambda x:x[1], reverse=True)[:10]
appearances_of_stemmed_words = Counter(stemmed_words)
top_10_stemmed_words = sorted(appearances_of_stemmed_words.items(), key=lambda x:x[1], reverse=True)[:10]

# Getting a list of interesting words, interesting stem words and the most salient sentence to summarise
# the passage.
list_of_interesting_words = get_interesting_words(top_10_words, top_10_stemmed_words, "normal")
list_of_interesting_stemmed_words = get_interesting_words(top_10_words, top_10_stemmed_words, "stemmed")
salient_sentence = find_salient_sentence_to_summarise_text(sentences)

# Printing the results for the user
print(f'The passage is about: {", ".join(list_of_interesting_words)}.')
print(f'Most salient quote from the text is: {salient_sentence}')
