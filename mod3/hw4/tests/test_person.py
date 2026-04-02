import unittest
from datetime import datetime
from freezegun import freeze_time
from hw4.person import Person


class TestPerson(unittest.TestCase):
    """Тесты для всех методов класса Person"""

    def setUp(self):
        """Создаём тестовые объекты перед каждым тестом"""
        self.person1 = Person("Иван", 1990, "Москва")
        self.person2 = Person("Мария", 2000)
        self.person3 = Person("Петр", 1985, "")

    # Тесты для __init__
    def test_init_with_all_parameters(self):
        """Проверяет инициализацию со всеми параметрами"""
        person = Person("Анна", 1995, "СПб")
        self.assertEqual(person.name, "Анна")
        self.assertEqual(person.yob, 1995)
        self.assertEqual(person.address, "СПб")

    def test_init_without_address(self):
        """Проверяет инициализацию без адреса"""
        person = Person("Сергей", 1992)
        self.assertEqual(person.name, "Сергей")
        self.assertEqual(person.yob, 1992)
        self.assertEqual(person.address, "")

    # Тесты для get_age
    @freeze_time("2024-01-01")
    def test_get_age_returns_correct_age(self):
        """Проверяет, что get_age возвращает правильный возраст"""
        person = Person("Тест", 2000)
        self.assertEqual(person.get_age(), 24)

    @freeze_time("2024-12-31")
    def test_get_age_at_end_of_year(self):
        """Проверяет возраст в конце года"""
        person = Person("Тест", 2000)
        self.assertEqual(person.get_age(), 24)

    def test_get_age_for_different_birth_years(self):
        """Проверяет возраст для разных годов рождения"""
        with freeze_time("2024-01-01"):
            test_cases = [
                (2020, 4),
                (2015, 9),
                (2000, 24),
                (1990, 34),
            ]
            for birth_year, expected_age in test_cases:
                person = Person("Тест", birth_year)
                self.assertEqual(person.get_age(), expected_age)

    # Тесты для get_name
    def test_get_name_returns_correct_name(self):
        """Проверяет, что get_name возвращает правильное имя"""
        self.assertEqual(self.person1.get_name(), "Иван")
        self.assertEqual(self.person2.get_name(), "Мария")

    # Тесты для set_name
    def test_set_name_changes_name(self):
        """Проверяет, что set_name изменяет имя"""
        self.person1.set_name("Алексей")
        self.assertEqual(self.person1.get_name(), "Алексей")

    def test_set_name_to_empty_string(self):
        """Проверяет установку пустого имени"""
        self.person1.set_name("")
        self.assertEqual(self.person1.get_name(), "")

    def test_set_name_multiple_times(self):
        """Проверяет множественную смену имени"""
        self.person1.set_name("Анна")
        self.assertEqual(self.person1.get_name(), "Анна")
        self.person1.set_name("Мария")
        self.assertEqual(self.person1.get_name(), "Мария")

    # Тесты для get_address
    def test_get_address_returns_correct_address(self):
        """Проверяет, что get_address возвращает правильный адрес"""
        self.assertEqual(self.person1.get_address(), "Москва")
        self.assertEqual(self.person2.get_address(), "")

    # Тесты для set_address
    def test_set_address_changes_address(self):
        """Проверяет, что set_address изменяет адрес"""
        self.person1.set_address("СПб")
        self.assertEqual(self.person1.get_address(), "СПб")

    def test_set_address_to_empty_string(self):
        """Проверяет установку пустого адреса"""
        self.person1.set_address("")
        self.assertEqual(self.person1.get_address(), "")

    def test_set_address_multiple_times(self):
        """Проверяет множественную смену адреса"""
        self.person2.set_address("Казань")
        self.assertEqual(self.person2.get_address(), "Казань")
        self.person2.set_address("Новосибирск")
        self.assertEqual(self.person2.get_address(), "Новосибирск")

    # Тесты для is_homeless
    def test_is_homeless_returns_false_when_address_exists(self):
        """Проверяет, что is_homeless возвращает False, если адрес есть"""
        self.assertFalse(self.person1.is_homeless())

    def test_is_homeless_returns_true_when_no_address(self):
        """Проверяет, что is_homeless возвращает True, если адреса нет"""
        self.assertTrue(self.person2.is_homeless())

    def test_is_homeless_returns_true_when_address_is_empty_string(self):
        """Проверяет, что is_homeless возвращает True при пустом адресе"""
        self.assertTrue(self.person3.is_homeless())

    def test_is_homeless_changes_after_setting_address(self):
        """Проверяет изменение статуса бездомности после установки адреса"""
        self.assertTrue(self.person2.is_homeless())
        self.person2.set_address("Казань")
        self.assertFalse(self.person2.is_homeless())

    def test_is_homeless_changes_after_removing_address(self):
        """Проверяет изменение статуса бездомности после удаления адреса"""
        self.assertFalse(self.person1.is_homeless())
        self.person1.set_address("")
        self.assertTrue(self.person1.is_homeless())


if __name__ == '__main__':
    unittest.main()