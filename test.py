import unittest
from io import StringIO
from unittest import mock
from unittest.mock import patch
from game_words import hangman_words
from hangman_session import HangmanSession

class TestHangmanSession(unittest.TestCase):

    # @patch('hangman_session.input', return_value='К')
    def test_correct_word_selection(self):  # Тесты для проверки правильности выбора слова из списка
        session = HangmanSession(level='easy', category='animals', num_attempts=7)
        self.assertTrue(len(session.word) > 0)  # Проверяем, что слово есть
        self.assertTrue(session.word in hangman_words['easy']['animals'])

        session = HangmanSession(level='medium', category='countries', num_attempts=3)
        self.assertTrue(len(session.word) > 0)
        self.assertTrue(session.word in hangman_words['medium']['countries'])

        session = HangmanSession(level='hard', category='jobs', num_attempts=3)
        self.assertTrue(len(session.word) > 0)
        self.assertTrue(session.word in hangman_words['hard']['jobs'])

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_state_1(self, mock_stdout): # Проверьте корректность отображения состояния игры после каждого ввода пользователя.
        session = HangmanSession(level='easy', category='animals', num_attempts=7)
        session.word = "КОТ"
        # 1
        session.guessed_letters = ['К']
        session.display_status()

        expected_output = "К _ _"
        output_lines = mock_stdout.getvalue().splitlines()

        word_line = next(line for line in output_lines if line.startswith("Слово:"))
        self.assertEqual(word_line.strip(), f"Слово: {expected_output}")

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_state_2(self, mock_stdout):  # Проверьте корректность отображения состояния игры после каждого ввода пользователя.
        session = HangmanSession(level='easy', category='animals', num_attempts=7)
        session.word = "КОТ"
        # 2
        session.guessed_letters = ['К', 'О']
        session.display_status()

        expected_output = "К О _"
        output_lines = mock_stdout.getvalue().splitlines()

        word_line = next(line for line in output_lines if line.startswith("Слово:"))
        self.assertEqual(word_line.strip(), f"Слово: {expected_output}")

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_state_3(self, mock_stdout):  # Проверьте корректность отображения состояния игры после каждого ввода пользователя.
        session = HangmanSession(level='easy', category='animals', num_attempts=7)
        session.word = "КОТ"
        # 2
        session.guessed_letters = ['К', 'О', 'Т']
        session.display_status()

        expected_output = "К О Т"
        output_lines = mock_stdout.getvalue().splitlines()

        word_line = next(line for line in output_lines if line.startswith("Слово:"))
        self.assertEqual(word_line.strip(), f"Слово: {expected_output}")

    @patch('hangman_session.input', side_effect=['к', 'О', 'т'])
    def test_letter_case_insensitive(self, mock_input):  # Убедитесь, что введенные буквы корректно обрабатываются вне зависимости от их регистра.
        session = HangmanSession(level='easy', category='animals', num_attempts=7)
        session.word = "КОТ"
        session.guessed_letters = []
        session.play()
        self.assertIn('К', session.guessed_letters)
        self.assertIn('О', session.guessed_letters)
        self.assertIn('Т', session.guessed_letters)

    def test_invalid_word_length(self):  # Игра не запускается, если загадываемое слово имеет некорректную длину.
        with self.assertRaises(ValueError, msg="Некорректная длина слова!"):
            # Мокаем случайную генерацию слова, чтобы вернуть пустую строку
            with mock.patch('hangman_session.hangman_words', {'easy': {'animals': ['']}}):
                session = HangmanSession(level='easy', category='animals', num_attempts=7)
                session.generate_word()

    @mock.patch('builtins.input', side_effect=['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж'])
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_exceeding_max_attempts(self, mock_stdout, mock_input): # После превышения заданного количества попыток игра всегда возвращает поражение.
        session = HangmanSession(level='easy', category='animals', num_attempts=7)
        session.word = "КОТ"
        session.play()

        # Проверяем, что осталось 0 попыток
        self.assertEqual(session.num_attempts, 0)

        # игра завершилась с сообщением о поражении
        output_lines = mock_stdout.getvalue().splitlines()
        word_line = next(line for line in output_lines if line.startswith("Вы проиграли."))
        self.assertIn("Вы проиграли. Загаданное слово было:", word_line.strip())


    @patch('hangman_session.input', side_effect=['К', 'О', 'Т']) # Состояние изменяется корректно
    def test_state_change_on_guess(self, mock_input):
        session = HangmanSession(level='easy', category='animals', num_attempts=7)
        session.word = "КОТ"  # Загаданное слово
        session.play()
        self.assertEqual(session.word, 'КОТ')


    @patch('hangman_session.input', side_effect=['КО', 'К', 'О', 'Т'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_input_length(self, mock_stdout, mock_input): # при отгадывании ввод строки длиной больше чем 1 (опечатка)
        session = HangmanSession(level='easy', category='animals', num_attempts=5)
        session.word = "КОТ"
        session.play()
        output_lines = mock_stdout.getvalue().splitlines()

        # при вводе 'КО' количество попыток не изменилось
        word_line = next(line for line in output_lines if line.startswith("Оставшиеся попытки:"))
        self.assertIn("Оставшиеся попытки: 5", word_line.strip())

        # 'КО' не было добавлено в список угаданных букв
        self.assertNotIn('КО', session.guessed_letters)

        # после правильного ввода 'К' количество попыток осталось прежним
        self.assertIn('К', session.guessed_letters)
        self.assertEqual(session.num_attempts, 5)


if __name__ == '__main__':
    unittest.main()
