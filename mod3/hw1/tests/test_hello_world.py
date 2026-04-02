import unittest
from freezegun import freeze_time
from hw1.hello_word_with_day import GREETINGS, app


class TestHelloWorld(unittest.TestCase):
    """Тесты для endpoint /hello-world/<name>"""

    @classmethod
    def setUpClass(cls):
        """Создаём тестовый клиент"""
        cls.client = app.test_client()
        app.config['TESTING'] = True

    def test_can_get_correct_username_with_weekdate(self):
        """
        Проверяет, что функция возвращает корректное имя пользователя
        и корректный день недели
        """
        # Проверяем все дни недели
        test_dates = [
            ("2024-01-01", "Хорошего понедельника"),  # Понедельник
            ("2024-01-02", "Хорошего вторника"),  # Вторник
            ("2024-01-03", "Хорошей среды"),  # Среда
            ("2024-01-04", "Хорошего четверга"),  # Четверг
            ("2024-01-05", "Хорошей пятницы"),  # Пятница
            ("2024-01-06", "Хорошей субботы"),  # Суббота
            ("2024-01-07", "Хорошего воскресенья")  # Воскресенье
        ]

        name = "Саша"

        for date_str, expected_greeting in test_dates:
            with freeze_time(date_str):
                response = self.client.get(f'/hello-world/{name}')
                response_text = response.data.decode()

                # Проверяем имя пользователя
                self.assertIn(name, response_text)

                # Проверяем корректность дня недели
                self.assertIn(expected_greeting, response_text)

    def test_weekday_correctness_separate(self):
        """
        Отдельная функция для проверки корректности дня недели
        """
        # Тестируем каждый день недели
        for i in range(7):
            # Устанавливаем дату так, чтобы weekday() возвращал i
            date_str = f"2024-01-{i + 1:02d}"

            with freeze_time(date_str):
                response = self.client.get('/hello-world/Тест')
                response_text = response.data.decode()

                # Проверяем, что приветствие соответствует ожидаемому
                expected = GREETINGS[i]
                self.assertIn(expected, response_text)

    def test_username_with_good_weekday(self):
        """
        Проверяет случай, когда в username передается 'Хорошей среды'
        """
        with freeze_time("2024-01-03"):  # Среда
            username = "Хорошей среды"
            response = self.client.get(f'/hello-world/{username}')
            response_text = response.data.decode()

            # Имя пользователя должно быть в ответе
            self.assertIn(username, response_text)
            # День недели тоже должен быть в ответе
            self.assertIn("Хорошей среды", response_text)


if __name__ == '__main__':
    unittest.main()