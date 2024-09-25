import os
import random
import time
from hangman_picture import hangman_pictures
from game_words import hangman_words
from hints import hints

class HangmanSession:
    def __init__(self, level, category, num_attempts):
        self.translate_category = {'countries': 'Страны', 'animals': 'Животные', 'jobs': 'Профессии'}
        self.level = level
        self.category = category
        self.num_attempts = int(num_attempts)
        self.word = ''
        self.guessed_letters = []
        self.generate_word()


    def play(self):
        while self.num_attempts > 0:
            self.clear_terminal()
            self.display_status()
            guess = input("Введите букву: ").upper()
            if len(guess) >= 2:
                continue

            if guess in self.guessed_letters:
                print("Вы уже угадывали эту букву.")
                time.sleep(0.7)
                continue

            self.guessed_letters.append(guess)

            if guess not in self.word:
                self.num_attempts -= 1

            if all(letter in self.guessed_letters for letter in self.word):
                self.clear_terminal()
                self.display_status()
                print("Поздравляем! Вы угадали слово:", self.word)
                time.sleep(2)
                break
        else:
            self.clear_terminal()
            self.display_status()
            print("Вы проиграли. Загаданное слово было:", self.word)
            time.sleep(2)

    def display_status(self):
        print(hangman_pictures[7 - self.num_attempts])
        print("Слово:", ' '.join(letter if letter in self.guessed_letters else '_' for letter in self.word))
        print("Категория:", self.translate_category[self.category])
        print("Оставшиеся попытки:", self.num_attempts)
        if self.num_attempts <= 2:
            if self.word in hints:
                print("Подказка: ", hints[self.word])

    def generate_word(self):
        words = hangman_words[self.level][self.category]
        ind = random.randint(0, len(words) - 1)
        self.word = words[ind]
        if not self.word or len(self.word) < 2:
            raise ValueError("Некорректная длина слова!")

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

