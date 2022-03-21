import re


def finding_all_unique_words_and_freq(words):
    words_unique = []
    word_freq = {}
    for word in words:
        if word not in words_unique:
            words_unique.append(word)
    for word in words_unique:
        word_freq[word] = words.count(word)
    return word_freq


def finding_freq_of_word_in_doc(word, words):
    freq = words.count(word)


def remove_special_characters(text):
    regex = re.compile("[^a-zA-Z0-9\s]")
    text_returned = re.sub(regex, "", text)
    return text_returned
