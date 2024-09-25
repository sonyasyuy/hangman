import random
import time
import os
from hangman_session import HangmanSession


class Hangman:
    def __init__(self):
        self.level_dict = {'1': 'easy', '2': 'medium', '3': 'hard'}
        self.category_dict = {'1': 'countries', '2': 'animals', '3': 'jobs'}
        self.level_choice = None
        self.category_choice = None
        self.attempts_amount = None

    def ChooseLevel(self):
        print("\nВыберите уровень сложности:")
        print("1. Легкий")
        print("2. Средний")
        print("3. Тяжелый")
        print("4. Выбрать случайный уровень")
        print("5. Выйти из игры")

        self.level_choice = input("Введите цифру (1/2/3/4/5): ")
        if self.level_choice == '5':
            self.Exit()
        elif self.level_choice not in {'1', '2', '3'}:
            self.level_choice = str(random.randint(1, 3))
            print("\n-Выбран случайный уровень сложности")
            time.sleep(0.5)

        self.level_choice = self.level_dict[self.level_choice]

    def ChooseCategory(self):
        print("\nВыберите категорию:")
        print("1. Страны")
        print("2. Животные")
        print("3. Профессии")
        print("4. Выбрать случайную категорию")
        print("5. Выйти из игры")

        self.category_choice = input("Введите цифру (1/2/3/4/5): ")
        if self.category_choice == '5':
            self.Exit()
        elif self.category_choice not in {'1', '2', '3'}:
            self.category_choice = str(random.randint(1, 3))
            print("\n-Выбрана случайная категория")
            time.sleep(0.5)

        self.category_choice = self.category_dict[self.category_choice]

    def ChooseAttemptsAmounts(self):
        self.attempts_amount = input("\nВведите количество возможных ошибок от 1 до 7: ")
        if self.attempts_amount not in {'1', '2', '3', '4', '5', '6', '7'}:
            self.attempts_amount = '7'
            print(f"\n-Количество возможных ошибок: {self.attempts_amount}")
            time.sleep(0.5)

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def Exit(self):
        print("Exiting...")
        time.sleep(1)
        self.clear_terminal()
        exit(0)

    def start(self):
        print("Добро пожаловать в игру \"Виселица\"")
        print("Хотите ознакомиться с правилами игры?")
        print("1. Да")
        print("2. Нет")
        need_rules = input("Введите цифру (1/2): ")

        if need_rules == '1':
            with open('game_rules.txt') as file:
                for line in file.readlines():
                    print(line)
            time.sleep(2)

            flag = input("\nВведите любой символ, чтобы продолжить:")

        while True:
            self.clear_terminal()
            self.ChooseLevel()
            self.clear_terminal()
            self.ChooseCategory()
            self.clear_terminal()
            self.ChooseAttemptsAmounts()
            self.clear_terminal()
            session = HangmanSession(level=self.level_choice, category=self.category_choice,
                                     num_attempts=self.attempts_amount)
            session.play()


if __name__ == "__main__":
    hangman = Hangman()
    hangman.start()
