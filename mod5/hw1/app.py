"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт. Напишите функцию,
которая на вход принимает порт и запускает по нему сервер. Если порт будет занят,
она должна найти процесс по этому порту, завершить его и попытаться запустить сервер ещё раз.
"""
from typing import List

from flask import Flask
import shlex
import subprocess
import os
import signal

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    if not isinstance(port, int):
        raise ValueError

    pids: List[int] = []
    try:
        # ПОиск процессов на указанном порту
        # lsof -i :port -t (флаг -t выводит только PID)
        command_str = f"lsof -i :{port} -t"
        command = shlex.split(command_str)
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0 and result.stdout.strip():
            # Разбирает вывод, который содержит пиды (каждый на новой строке)
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        pid = int(line.strip())
                        pids.append(pid)
                    except ValueError:
                        continue


    except FileNotFoundError:
        print("Warning: lsof command not found. Make sure it's installed.")
    except Exception as e:
        print(f"Error getting PIDs: {e}")
    return pids


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт
    @param port: порт
    """
    pids: List[int] = get_pids(port)
    if not pids:
        print(f"Port {port} is free")
        return

    print(f"Found processes occupying port {port}: {pids}")

    for pid in pids:
        try:
            # Сначала пробуем мягко завершить процесс (SIGTERM)
            print(f"Terminating process {pid} with SIGTERM...")
            os.kill(pid, signal.SIGTERM)

            # Даем процессу время на завершение
            import time
            time.sleep(1)

            # завершился ли процесс?
            try:
                os.kill(pid, 0)  # существует ли процесс
                # Если процесс все еще существует, использует SIGKILL
                print(f"Process {pid} still running, using SIGKILL...")
                os.kill(pid, signal.SIGKILL)
            except OSError:
                # Процесс уже завершен
                print(f"Process {pid} terminated successfully")

        except ProcessLookupError:
            print(f"Process {pid} not found")
        except PermissionError:
            print(f"Permission denied to terminate process {pid}. Try running with sudo.")
        except Exception as e:
            print(f"Error terminating process {pid}: {e}")


def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: порт
    """
    free_port(port)

    #Проверка порта
    pids = get_pids(port)
    if pids:
        print(f"Port {port} occupied: {pids}")
        return

    print(f"Staring server on port {port}")
    app.run(port=port, debug=True)

    @app.route('/')
    def hell():
        return "Drugoy server rabotaet"


if __name__ == '__main__':
    run(5000)
