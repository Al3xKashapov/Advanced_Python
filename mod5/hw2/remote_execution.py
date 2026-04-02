"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import signal
import subprocess
import shlex
from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)
app.config["WTF_CSRF_ENABLED"] = False
app.config["SECRET_KEY"] = "secret-key-for-testing"


class CodeForm(FlaskForm):
    code = StringField(validators=[
        InputRequired(message="Code is required")
    ])
    timeout = IntegerField(validators=[
        InputRequired(message="Timeout is required"),
        NumberRange(min=1, max=30, message="Timeout must be between 1 and 30 seconds")
    ])


def run_python_code_in_subprocess(code: str, timeout: int):
    """
    Запускает Python код в подпроцессе с ограничением времени и ресурсов

    @param code: код на Python
    @param timeout: тайм-аут в секундах (1-30)
    @return: tuple (output: str, error: str, timed_out: bool)
    """
    # Экранируем код для безопасной передачи в командную строку
    # Заменяем двойные кавычки и другие опасные символы
    safe_code = code.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')

    # Используем prlimit для ограничения ресурсов:
    # --nproc=1:1 - ограничение на количество процессов (нельзя создать дочерние процессы)
    # --nofile=10:10 - ограничение на количество открытых файлов
    # --cpu=N - ограничение по CPU времени (запасной механизм)
    cmd = f'prlimit --nproc=1:1 --nofile=10:10 python -c "{safe_code}"'

    try:
        # Запускаем процесс
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid  # Создаем новую группу процессов для возможности убить все дочерние
        )

        try:
            # Ждем завершения с таймаутом
            stdout, stderr = process.communicate(timeout=timeout)
            return stdout, stderr, False

        except subprocess.TimeoutExpired:
            # Убиваем весь процесс и его дочерние процессы
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.kill()

            # Получаем вывод, который успел накопиться
            stdout, stderr = process.communicate()
            return stdout, stderr, True

    except Exception as e:
        return "", f"Error executing code: {str(e)}", False


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()

    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data

        stdout, stderr, timed_out = run_python_code_in_subprocess(code, timeout)

        if timed_out:
            return f"Execution timeout ({timeout} seconds)\nOutput: {stdout}\nErrors: {stderr}", 408

        if stderr:
            return f"Execution completed with errors:\n{stderr}\nOutput:\n{stdout}", 400

        return f"Execution completed successfully:\n{stdout}", 200

    return f"Invalid input: {form.errors}", 400


if __name__ == '__main__':
    import os

    app.run(debug=True)