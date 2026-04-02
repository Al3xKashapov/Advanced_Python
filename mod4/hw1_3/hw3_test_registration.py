"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_3.hw1_registration import app

class TestRegistrationForm(unittest.TestCase):
    def setUp(self):
        """Настройка тестового клиента перед каждым тестом"""
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_registration(self):
        """Тест успешной регистрации с валидными данными"""
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456,
            'comment': 'Test comment'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered', response.data.decode())

    def test_email_validation(self):
        """Тесты валидации email"""
        # Пустой email
        response = self.app.post('/registration', data={
            'email': '',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data.decode())

        # Неверный формат email
        response = self.app.post('/registration', data={
            'email': 'invalid-email',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data.decode())

        # Валидный email
        response = self.app.post('/registration', data={
            'email': 'valid@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 200)

    def test_phone_validation(self):
        """Тесты валидации телефона"""
        # Пустой телефон
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': '',
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response.data.decode())

        # Телефон с неправильной длиной (9 цифр)
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 123456789,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response.data.decode())

        # Отрицательный телефон
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': -1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response.data.decode())

        # Валидный телефон
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 200)

    def test_name_validation(self):
        """Тесты валидации имени"""
        # Пустое имя
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': '',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data.decode())

        # Валидное имя
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 200)

    def test_address_validation(self):
        """Тесты валидации адреса"""
        # Пустой адрес
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '',
            'index': 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('address', response.data.decode())

        # Валидный адрес
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 200)

    def test_index_validation(self):
        """Тесты валидации индекса"""
        # Пустой индекс
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': ''
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('index', response.data.decode())

        # Отрицательный индекс
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': -123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('index', response.data.decode())

        # Валидный индекс
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 200)

    def test_comment_optional(self):
        """Тест, что комментарий - опциональное поле"""
        # Без комментария
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456
        })
        self.assertEqual(response.status_code, 200)

        # С комментарием
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 123456,
            'comment': 'Some comment'
        })
        self.assertEqual(response.status_code, 200)

    def test_multiple_fields_missing(self):
        """Тест отсутствия нескольких обязательных полей"""
        response = self.app.post('/registration', data={
            'email': 'user@example.com',
            'name': 'John Doe'
            # Отсутствуют phone, address, index
        })
        self.assertEqual(response.status_code, 400)
        response_data = response.data.decode()
        self.assertIn('phone', response_data)
        self.assertIn('address', response_data)
        self.assertIn('index', response_data)


if __name__ == '__main__':
    unittest.main()
