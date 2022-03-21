from nltk.tokenize import word_tokenize

from engine.posting import PostingListProcessor
from preprocessing.vocab import Vocabulary


class LyricsSearch:
    zeros_and_ones = []
    zeroes_and_ones_of_all_words = []

    def __init__(
        self, vocab: Vocabulary, posting_list_processor: PostingListProcessor
    ) -> None:
        if not posting_list_processor.posting_is_built():
            posting_list_processor.build_posting_list()
        self.vocab = vocab
        self.posting_list_processor = posting_list_processor

    def _preprocess_query(self, query) -> None:
        self.connecting_words = []
        self.different_words = []

        self.query_expression = query
        self.query = word_tokenize(query)

        for word in self.query:
            if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
                self.different_words.append(word.lower())
            else:
                self.connecting_words.append(word.lower())

    def _find_occurrence(self):
        total_files = len(self.vocab.files_with_index)
        for word in self.different_words:
            if word.lower() in self.vocab.unique_words_all:
                zeroes_and_ones = [0] * total_files
                linkedlist = self.posting_list_processor.posting_lists[word].head
                while linkedlist.next_val is not None:
                    zeroes_and_ones[linkedlist.next_val.doc - 1] = 1
                    linkedlist = linkedlist.next_val
                self.zeroes_and_ones_of_all_words.append(zeroes_and_ones)
            else:
                raise Exception(f"Word {word} not found")

    def search(self, query: str) -> None:
        self._preprocess_query(query)
        self._find_occurrence()

        bitwise_op = []
        for word in self.connecting_words:
            word_list1 = self.zeroes_and_ones_of_all_words[0]
            word_list2 = self.zeroes_and_ones_of_all_words[1]
            if word == "and":
                bitwise_op = [w1 & w2 for (w1, w2) in zip(word_list1, word_list2)]
                self.zeroes_and_ones_of_all_words.remove(word_list1)
                self.zeroes_and_ones_of_all_words.remove(word_list2)
                self.zeroes_and_ones_of_all_words.insert(0, bitwise_op)
            elif word == "or":
                bitwise_op = [w1 | w2 for (w1, w2) in zip(word_list1, word_list2)]
                self.zeroes_and_ones_of_all_words.remove(word_list1)
                self.zeroes_and_ones_of_all_words.remove(word_list2)
                self.zeroes_and_ones_of_all_words.insert(0, bitwise_op)
            elif word == "not":
                bitwise_op = [not w1 for w1 in word_list2]
                bitwise_op = [int(b) for b in bitwise_op]
                self.zeroes_and_ones_of_all_words.remove(word_list2)
                self.zeroes_and_ones_of_all_words.remove(word_list1)
                bitwise_op = [w1 & w2 for (w1, w2) in zip(word_list1, bitwise_op)]

        self.zeroes_and_ones_of_all_words.insert(0, bitwise_op)

        files = []
        lis = self.zeroes_and_ones_of_all_words[0]
        for cnt, index in enumerate(lis):
            if index == 1:
                files.append(self.vocab.files_with_index[cnt + 1])

        # print("Files with index", self.vocab.files_with_index)
        print("Boolean Output", lis)
        print("Relevant Documents", files)
