import random


class WordsAPI:

    def __init__(self, file_path):
        self.file_path = file_path
        self.words_list = []
        self.used_words = []
        self.word = ""

        self.load_words()
        self.select_word()

    def load_words(self):
        with open(self.file_path, 'r', encoding="utf-8") as file:
            self.words_list = [line.strip().upper() for line in file if line.strip()]

    def is_at_right_position(self, i, char):
        return self.word[i] == char

    def is_in_word(self, char):
        return char in self.word

    def is_valid_guess(self, guess):
        return guess.upper() == self.word

    def select_word(self):
        self.word = random.choice(self.words_list)
        while self.word in self.used_words:
            self.word = random.choice(self.words_list)
        self.used_words.append(self.word)

    def display_right_word(self):
        print("Right word was:", self.word)