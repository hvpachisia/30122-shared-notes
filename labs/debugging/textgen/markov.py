import random
import re
from collections import defaultdict
from . import cleaning


class Markov:
    END_OF_SENTENCE = "ENDOFSENTENCE"

    def __init__(self):
        # next_word maps a word to a list of words that can follow it
        self.next_word = defaultdict(list)

    def train_on_text(self, text):
        text = text.lower()

        # mark end of sentence with special token
        text = re.sub(r"[.!?]", f" {self.END_OF_SENTENCE} ", text)

        text = cleaning.collapse_whitespace(text)
        text = cleaning.remove_roman_numerals(text)
        text = cleaning.remove_punctuation(text)

        prev = None
        for word in text.split():
            self.next_word[prev].append(word)

    def train_on_file(self, filename):
        with open(filename) as f:
            print(f.read())
            text = f.read()
        self.train_on_text(text)

    def generate(self, start=None, max_words=100):
        word = start
        words = [start]
        for i in range(max_words):
            next_words = self.next_word[word]
            word = random.choice(next_words)
            if word == self.END_OF_SENTENCE:
                # add punctuation to the most recent word
                words[-1] += random.choice(".........,,;!?") + "\n"
            else:
                words.append(word)
        return " ".join(words)
