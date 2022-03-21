import os
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm

from preprocessing.utils import (
    remove_special_characters,
    finding_all_unique_words_and_freq,
)


class Vocabulary:
    unique_words_all = None
    word_to_freq = {}
    files_with_index = {}
    stop_words = set(stopwords.words("english"))

    def __init__(self, path: str) -> None:
        self.filenames = [os.path.join(path, file) for file in os.listdir(path)]

    def is_built(self):
        return len(self.word_to_freq) != 0

    def build_vocab(self):
        print("Building vocab...")
        for idx, filename in tqdm(enumerate(self.filenames)):
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
                text = remove_special_characters(text)
                text = re.sub(re.compile("\d"), "", text)
                words = word_tokenize(text)
                words = [word for word in words if len(words) > 1]
                words = [word.lower() for word in words]
                # words = [word for word in words if word not in self.stop_words]
                self.word_to_freq.update(finding_all_unique_words_and_freq(words))
                self.files_with_index[idx + 1] = os.path.basename(filename)
        self.unique_words_all = set(self.word_to_freq.keys())
