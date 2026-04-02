
import unittest
from hw3.accounting import app, storage, parse_date


class TestAccounting(unittest.TestCase):
    """Тесты для приложения Учёт финансов"""

    @classmethod
    def setUpClass(cls):
        """Заполняем storage изначальными данными"""
        cls.client = app.test_client()
        app.config['TESTING'] = True

    def setUp(self):
        """Очищаем storage перед каждым тестом и восстанавливаем тестовые данные"""
        storage.clear()
        storage[2024] = {
            1: {1: 1000, 15: 500},
            2: {1: 2000},
            12: {31: 300}
        }
        storage[2025] = {
            1: {1: 100}
        }

    # Тесты для /add/ endpoint
    def test_add_endpoint_works(self):
        """Проверяет, что endpoint /add/ работает"""
        response = self.client.get('/add/20260101/500')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Добавлена трата 500 руб. за 20260101", response.data.decode())

    def test_add_endpoint_adds_to_storage(self):
        """Проверяет, что /add/ добавляет данные в storage"""
        self.client.get('/add/20260315/300')
        self.assertIn(2026, storage)
        self.assertIn(3, storage[2026])
        self.assertIn(15, storage[2026][3])
        self.assertEqual(storage[2026][3][15], 300)

    def test_add_endpoint_multiple_entries_same_day(self):
        """Проверяет добавление нескольких трат за один день"""
        self.client.get('/add/20260410/100')
        self.client.get('/add/20260410/200')
        self.assertEqual(storage[2026][4][10], 300)

    # Тесты для /calculate/year endpoint
    def test_calculate_year_works_with_data(self):
        """Проверяет, что /calculate/year работает с данными"""
        response = self.client.get('/calculate/2024')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Суммарные траты за 2024 год: 3800 руб.", response.data.decode())

    def test_calculate_year_works_with_empty_storage(self):
        """Проверяет /calculate/year при пустом storage"""
        storage.clear()
        response = self.client.get('/calculate/2024')
        self.assertEqual(response.status_code, 404)
        self.assertIn("За 2024 год трат не найдено", response.data.decode())

    def test_calculate_year_returns_zero_for_no_data(self):
        """Проверяет /calculate/year за год без данных"""
        response = self.client.get('/calculate/2023')
        self.assertEqual(response.status_code, 404)
        self.assertIn("За 2023 год трат не найдено", response.data.decode())

    # Тесты для /calculate/year/month endpoint
    def test_calculate_month_works_with_data(self):
        """Проверяет, что /calculate/year/month работает с данными"""
        response = self.client.get('/calculate/2024/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Суммарные траты за 2024-01: 1500 руб.", response.data.decode())

    def test_calculate_month_works_with_empty_storage(self):
        """Проверяет /calculate/year/month при пустом storage"""
        storage.clear()
        response = self.client.get('/calculate/2024/1')
        self.assertEqual(response.status_code, 404)
        self.assertIn("За 2024-01 месяц трат не найдено", response.data.decode())

    def test_calculate_month_returns_zero_for_no_data(self):
        """Проверяет /calculate/year/month за месяц без данных"""
        response = self.client.get('/calculate/2024/3')
        self.assertEqual(response.status_code, 404)
        self.assertIn("За 2024-03 месяц трат не найдено", response.data.decode())

    # Тесты для проверки формата даты (невалидные значения)
    def test_add_endpoint_rejects_invalid_date_format(self):
        """Проверяет, что /add/ принимает дату только в формате YYYYMMDD"""
        # Только те даты, которые не пройдут валидацию в parse_date
        # но не вызовут 404 от Flask
        invalid_dates = [
            "20241301",  # неверный месяц
            "20240132",  # неверный день
            "20240001",  # месяц 0
            "20240100",  # день 0
            "abcd1234",  # не цифры
        ]

        for invalid_date in invalid_dates:
            with self.subTest(invalid_date=invalid_date):
                response = self.client.get(f'/add/{invalid_date}/100')
                self.assertEqual(response.status_code, 400)
                self.assertIn("Ошибка", response.data.decode())

    def test_add_endpoint_rejects_invalid_month(self):
        """Проверяет, что /add/ отклоняет неверный месяц"""
        response = self.client.get('/add/20241301/100')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Ошибка", response.data.decode())

    def test_add_endpoint_rejects_invalid_day(self):
        """Проверяет, что /add/ отклоняет неверный день"""
        response = self.client.get('/add/20240132/100')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Ошибка", response.data.decode())

    # Тесты для parse_date функции (проверка исключений)
    def test_parse_date_raises_error_for_invalid_format(self):
        """Проверяет, что parse_date вызывает исключение при неверном формате"""
        with self.assertRaises(ValueError):
            parse_date("2024-01-01")

        with self.assertRaises(ValueError):
            parse_date("202401")

        with self.assertRaises(ValueError):
            parse_date("abcd1234")

    def test_parse_date_raises_error_for_invalid_month(self):
        """Проверяет, что parse_date вызывает исключение при неверном месяце"""
        with self.assertRaises(ValueError):
            parse_date("20241301")

        with self.assertRaises(ValueError):
            parse_date("20240001")

    def test_parse_date_raises_error_for_invalid_day(self):
        """Проверяет, что parse_date вызывает исключение при неверном дне"""
        with self.assertRaises(ValueError):
            parse_date("20240132")

        with self.assertRaises(ValueError):
            parse_date("20240100")


if __name__ == '__main__':
    unittest.main()