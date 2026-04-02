import unittest
from hw2.remote_execution import app


class TestRemoteExecution(unittest.TestCase):
    def setUp(self):
        """Настройка тестового клиента"""
        self.app = app.test_client()
        self.app.testing = True
        app.config["WTF_CSRF_ENABLED"] = False

    def test_valid_code_execution(self):
        """Тест успешного выполнения кода"""
        response = self.app.post('/run_code', data={
            'code': 'print("Hello, World!")',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, World!", response.data.decode())

    def test_timeout_execution(self):
        """Тест превышения тайм-аута"""
        response = self.app.post('/run_code', data={
            'code': 'import time; time.sleep(10); print("Done")',
            'timeout': 2
        })
        self.assertEqual(response.status_code, 408)
        self.assertIn("Execution timeout", response.data.decode())

    def test_invalid_code(self):
        """Тест с некорректным кодом"""
        response = self.app.post('/run_code', data={
            'code': 'print(undefined_variable)',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data.decode().lower())

    def test_empty_code(self):
        """Тест с пустым кодом"""
        response = self.app.post('/run_code', data={
            'code': '',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Code is required", response.data.decode())

    def test_invalid_timeout(self):
        """Тест с некорректным тайм-аутом"""
        # Тайм-аут = 0
        response = self.app.post('/run_code', data={
            'code': 'print("test")',
            'timeout': 0
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("timeout", response.data.decode())

        # Тайм-аут > 30
        response = self.app.post('/run_code', data={
            'code': 'print("test")',
            'timeout': 60
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("timeout", response.data.decode())

        # Отрицательный тайм-аут
        response = self.app.post('/run_code', data={
            'code': 'print("test")',
            'timeout': -5
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("timeout", response.data.decode())

    def test_missing_timeout(self):
        """Тест отсутствия тайм-аута"""
        response = self.app.post('/run_code', data={
            'code': 'print("test")'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Timeout is required", response.data.decode())

    def test_shell_injection_prevention(self):
        """Тест защиты от shell-инъекций"""
        # Попытка выполнить команду shell
        response = self.app.post('/run_code', data={
            'code': 'print("test"); import os; os.system("echo hacked")',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 200)  # Код должен выполниться, но команда не должна сработать

    def test_infinite_loop(self):
        """Тест бесконечного цикла с тайм-аутом"""
        response = self.app.post('/run_code', data={
            'code': 'while True: pass',
            'timeout': 2
        })
        self.assertEqual(response.status_code, 408)
        self.assertIn("Execution timeout", response.data.decode())

    def test_resource_limitation(self):
        """Тест ограничения ресурсов (нельзя создать дочерний процесс)"""
        response = self.app.post('/run_code', data={
            'code': 'import subprocess; subprocess.run(["echo", "test"])',
            'timeout': 5
        })
        # Должен быть либо тайм-аут, либо ошибка из-за ограничения ресурсов
        self.assertIn(response.status_code, [400, 408])

    def test_complex_code(self):
        """Тест сложного кода"""
        response = self.app.post('/run_code', data={
            'code': '''
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
print(f"Factorial of 5 is {factorial(5)}")
''',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Factorial of 5 is 120", response.data.decode())


if __name__ == '__main__':
    unittest.main()
