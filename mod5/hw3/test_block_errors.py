import unittest
from hw3.block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):

    def test_ignore_specific_error(self):
        """Тест: ошибка игнорируется (пример 1 из задания)"""
        err_types = {ZeroDivisionError, TypeError}

        try:
            with BlockErrors(err_types):
                a = 1 / 0
        except Exception:
            self.fail("Исключение не должно было быть выброшено")

    def test_propagate_unexpected_error(self):
        """Тест: неожидаемая ошибка прокидывается выше (пример 2 из задания)"""
        err_types = {ZeroDivisionError}

        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'

    def test_nested_blocks_outer_ignores(self):
        """Тест: внешний блок игнорирует, внутренний прокидывает (пример 3 из задания)"""
        outer_err_types = {TypeError}
        inner_err_types = {ZeroDivisionError}

        try:
            with BlockErrors(outer_err_types):
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
        except Exception:
            self.fail("Внешний блок должен был игнорировать исключение")

    def test_ignore_parent_error(self):
        """Тест: дочерние ошибки игнорируются (пример 4 из задания)"""
        err_types = {Exception}

        try:
            with BlockErrors(err_types):
                a = 1 / '0'
        except Exception:
            self.fail("Дочернее исключение TypeError должно быть проигнорировано")

    def test_no_error(self):
        """Тест: если ошибки нет, блок выполняется нормально"""
        err_types = {ZeroDivisionError}
        result = 0

        try:
            with BlockErrors(err_types):
                result = 10
        except Exception:
            self.fail("Не должно быть исключений")

        self.assertEqual(result, 10)

    def test_multiple_errors_in_collection(self):
        """Тест: игнорирование нескольких типов ошибок"""
        err_types = {ValueError, KeyError, ZeroDivisionError}

        # Проверяем игнорирование ZeroDivisionError
        try:
            with BlockErrors(err_types):
                a = 1 / 0
        except Exception:
            self.fail("ZeroDivisionError должен быть проигнорирован")

        # Проверяем игнорирование ValueError
        try:
            with BlockErrors(err_types):
                int('not a number')
        except Exception:
            self.fail("ValueError должен быть проигнорирован")

        # Проверяем, что другие ошибки не игнорируются
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'

    def test_nested_different_errors(self):
        """Тест: разные ошибки во вложенных блоках"""
        try:
            with BlockErrors({TypeError}):
                with BlockErrors({ZeroDivisionError}):
                    a = 1 / 0  # Игнорируется внутренним блоком
                # Здесь выполнение продолжается
                b = 1 / '0'  # Игнорируется внешним блоком
        except Exception:
            self.fail("Обе ошибки должны быть проигнорированы")

    def test_propagate_from_inner_to_outer(self):
        """Тест: ошибка прокидывается из внутреннего блока во внешний"""
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                with BlockErrors({ValueError}):
                    a = 1 / 0  # Не игнорируется ни одним блоком

    def test_empty_error_collection(self):
        """Тест: пустая коллекция ошибок - все ошибки прокидываются"""
        err_types = set()

        with self.assertRaises(ZeroDivisionError):
            with BlockErrors(err_types):
                a = 1 / 0

        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'

    def test_single_error_in_collection(self):
        """Тест: один тип ошибки в коллекции"""
        # Игнорируем ZeroDivisionError
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / 0
        except Exception:
            self.fail("ZeroDivisionError должен быть проигнорирован")

        # TypeError не игнорируется
        with self.assertRaises(TypeError):
            with BlockErrors({ZeroDivisionError}):
                a = 1 / '0'

    def test_subclass_error(self):
        """Тест: дочерние классы ошибок"""

        class MyCustomError(Exception):
            pass

        class MySpecificError(MyCustomError):
            pass

        # Игнорируем родительский класс
        try:
            with BlockErrors({MyCustomError}):
                raise MySpecificError("Это дочернее исключение")
        except Exception:
            self.fail("Дочернее исключение должно быть проигнорировано")

        # Игнорируем только дочерний класс
        with self.assertRaises(MyCustomError):
            with BlockErrors({MySpecificError}):
                raise MyCustomError("Это родительское исключение")

    def test_error_in_enter_or_exit(self):
        """Тест: ошибка в методах __enter__ или __exit__"""

        class ErrorInEnter:
            def __enter__(self):
                raise ValueError("Ошибка в __enter__")

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        # Ошибка в __enter__ не должна игнорироваться
        with self.assertRaises(ValueError):
            with BlockErrors({TypeError}):
                with ErrorInEnter():
                    pass


if __name__ == '__main__':
    unittest.main()