"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask
import subprocess
import shlex

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    """
    Возвращает время работы системы (uptime).
    """

    try:

        result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)

        if result.returncode == 0:
            uptime_str = result.stdout.strip().replace('up ', '', 1)
            return f"Current uptime is {uptime_str}"
        else:
            return "Error getting uptime", 500

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
