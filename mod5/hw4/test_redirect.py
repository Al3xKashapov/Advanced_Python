import unittest
import sys
import io
from hw4.redirect import Redirect


class TestRedirect(unittest.TestCase):

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.stdout_capture = io.StringIO()
        self.stderr_capture = io.StringIO()

    def test_redirect_both_streams(self):
        """Тест перенаправления обоих потоков"""
        with Redirect(stdout=self.stdout_capture, stderr=self.stderr_capture):
            print("Hello stdout")
            print("Hello stderr", file=sys.stderr)

        # Проверяем, что вывод попал в файлы
        self.assertEqual(self.stdout_capture.getvalue(), "Hello stdout\n")
        self.assertEqual(self.stderr_capture.getvalue(), "Hello stderr\n")

    def test_redirect_stdout_only(self):
        """Тест перенаправления только stdout"""
        original_stdout = sys.stdout

        with Redirect(stdout=self.stdout_capture):
            print("This goes to file")
            print("This also goes to file")
            # stderr продолжает выводиться в оригинальный stdout
            print("This goes to original stdout", file=sys.stderr)

        # Проверяем stdout
        self.assertEqual(self.stdout_capture.getvalue(), "This goes to file\nThis also goes to file\n")

        # stderr не должен быть перенаправлен
        self.assertEqual(self.stderr_capture.getvalue(), "")

    def test_redirect_stderr_only(self):
        """Тест перенаправления только stderr"""
        with Redirect(stderr=self.stderr_capture):
            print("This goes to original stdout")
            print("This goes to file", file=sys.stderr)

        # Проверяем stderr
        self.assertEqual(self.stderr_capture.getvalue(), "This goes to file\n")

    def test_no_redirect(self):
        """Тест без перенаправления"""
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        with Redirect():
            # Потоки должны остаться неизменными
            self.assertIs(sys.stdout, original_stdout)
            self.assertIs(sys.stderr, original_stderr)

    def test_exception_handling(self):
        """Тест обработки исключений"""
        with Redirect(stderr=self.stderr_capture):
            try:
                raise ValueError("Test exception")
            except ValueError:
                pass

        # Проверяем, что traceback был записан в stderr
        output = self.stderr_capture.getvalue()
        self.assertIn("ValueError", output)
        self.assertIn("Test exception", output)

    def test_nested_redirects(self):
        """Тест вложенных перенаправлений"""
        inner_stdout = io.StringIO()
        outer_stdout = io.StringIO()

        with Redirect(stdout=outer_stdout):
            print("Outer redirect")

            with Redirect(stdout=inner_stdout):
                print("Inner redirect")

            print("Back to outer redirect")

        # Проверяем внешний вывод
        outer_output = outer_stdout.getvalue()
        self.assertIn("Outer redirect", outer_output)
        self.assertIn("Back to outer redirect", outer_output)
        self.assertNotIn("Inner redirect", outer_output)

        # Проверяем внутренний вывод
        inner_output = inner_stdout.getvalue()
        self.assertIn("Inner redirect", inner_output)

    def test_redirect_with_file(self):
        """Тест перенаправления в реальный файл"""
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as stdout_file:
            stdout_filename = stdout_file.name

        try:
            with Redirect(stdout=open(stdout_filename, 'w')):
                print("Line 1")
                print("Line 2")

            # Проверяем содержимое файла
            with open(stdout_filename, 'r') as f:
                content = f.read()
                self.assertEqual(content, "Line 1\nLine 2\n")
        finally:
            # Удаляем временный файл
            if os.path.exists(stdout_filename):
                os.unlink(stdout_filename)

    def test_exception_propagation(self):
        """Тест, что исключения продолжают распространяться после выхода из контекста"""
        with self.assertRaises(ValueError):
            with Redirect(stdout=self.stdout_capture):
                raise ValueError("This exception should propagate")

    def test_flush_on_exit(self):
        """Тест, что буферы сбрасываются при выходе"""
        # Создаем буферизированный поток
        buffered_stdout = io.StringIO()

        with Redirect(stdout=buffered_stdout):
            print("Test message")
            # Сообщение еще может быть в буфере

        # После выхода из контекста буфер должен быть сброшен
        self.assertEqual(buffered_stdout.getvalue(), "Test message\n")

    def test_redirect_without_context_manager(self):
        """Тест использования контекстного менеджера без блока with (неправильное использование)"""
        # Это не типичное использование, но проверим, что не падает
        redirect = Redirect(stdout=self.stdout_capture)
        redirect.__enter__()
        print("Direct output")
        redirect.__exit__(None, None, None)

        self.assertEqual(self.stdout_capture.getvalue(), "Direct output\n")

    def test_complex_output(self):
        """Тест со сложным выводом"""
        with Redirect(stdout=self.stdout_capture, stderr=self.stderr_capture):
            print("Multiple")
            print("lines")
            print("of", "output", sep=", ", end="!\n")
            print("Error message", file=sys.stderr)

        self.assertEqual(self.stdout_capture.getvalue(), "Multiple\nlines\nof, output!\n")
        self.assertEqual(self.stderr_capture.getvalue(), "Error message\n")


if __name__ == '__main__':
    # Запускаем тесты с выводом результатов в консоль
    unittest.main()

    # Альтернативный запуск с сохранением результатов в файл:
    # with open('test_results.txt', 'w') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream, verbosity=2)
    #     unittest.main(testRunner=runner, exit=False)