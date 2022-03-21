import re
from typing import Union, Dict

from nltk.tokenize import word_tokenize
from tqdm import tqdm

from models import HeadNode, Node
from preprocessing.utils import (
    remove_special_characters,
    finding_all_unique_words_and_freq,
)
from preprocessing.vocab import Vocabulary


class PostingListProcessor:
    posting_lists: Dict[str, Union[HeadNode, Node]] = {}

    def __init__(self, vocab: Vocabulary) -> None:
        self.vocab = vocab

    def posting_is_built(self):
        return len(self.posting_lists) != 0

    def _create_head_list(self) -> None:
        for word in self.vocab.unique_words_all:
            self.posting_lists[word] = HeadNode()
            self.posting_lists[word].head = Node(1, Node)

    def build_posting_list(self):
        if not self.vocab.is_built():
            self.vocab.build_vocab()

        print("Creating posting lists...")
        self._create_head_list()
        for idx, filename in tqdm(enumerate(self.vocab.filenames)):
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
                text = remove_special_characters(text)
                text = re.sub(re.compile("\d"), "", text)
                words = word_tokenize(text)
                words = [word for word in words if len(words) > 1]
                words = [word.lower() for word in words]
                # words = [word for word in words if word not in self.vocab.stop_words]
                word_freq_in_doc = finding_all_unique_words_and_freq(words)
                for word in word_freq_in_doc.keys():
                    posting_list = self.posting_lists[word].head
                    while posting_list.next_val is not None:
                        posting_list = posting_list.next_val
                    posting_list.next_val = Node(idx + 1, word_freq_in_doc[word])
