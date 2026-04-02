"""
Тесты для задачи 2. Дешифратор
"""

import unittest
from hw2.decrypt import decrypt


class TestDecrypt(unittest.TestCase):
    """Тесты для функции decrypt"""

    def test_no_dots(self):
        """
        Группа 1: Шифры без точек
        """
        test_cases = [
            ("абра-кадабра.", "абра-кадабра"),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_double_dots(self):
        """
        Группа 2: Шифры с двумя точками
        """
        test_cases = [
            ("абраа..-кадабра", "абра-кадабра"),
            ("абра--..кадабра", "абра-кадабра"),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_triple_dots(self):
        """
        Группа 3: Шифры с тремя точками
        """
        test_cases = [
            ("абраа..-.кадабра", "абра-кадабра"),
            ("абрау...-кадабра", "абра-кадабра"),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_many_dots(self):
        """
        Группа 4: Шифры с множеством точек
        """
        test_cases = [
            ("абра........", ""),
            ("абр......a.", "a"),
            ("1.......................", ""),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_dots_with_numbers(self):
        """
        Группа 5: Шифры с точками и числами
        """
        test_cases = [
            ("1..2.3", "23"),
            (".", ""),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)


if __name__ == '__main__':
    unittest.main()
