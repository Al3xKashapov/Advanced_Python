"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

from flask import Flask, request
import subprocess
import shlex
from typing import List

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    """
    Возвращает результат выполнения команды ps с переданными аргументами.

    Примеры запросов:
    - /ps?arg=aux
    - /ps?arg=a&arg=u&arg=x
    - /ps?arg=ef
    """
    try:
        # Получаем список аргументов из запроса
        args: List[str] = request.args.getlist('arg')

        # Проверяем, что аргументы переданы
        if not args:
            return """<pre>
No arguments provided. 
Usage examples:
- /ps?arg=aux
- /ps?arg=a&arg=u&arg=x
- /ps?arg=ef
</pre>""", 400

        # Экранируем каждый аргумент для безопасности
        # Это предотвращает инъекции команд
        safe_args = [shlex.quote(arg) for arg in args]

        # Формируем команду ps с экранированными аргументами
        # Команда: ps arg1 arg2 arg3 ...
        command_str = f"ps {' '.join(safe_args)}"
        command = shlex.split(command_str)

        # Выполняем команду
        result = subprocess.run(command, capture_output=True, text=True)

        # Проверяем результат выполнения
        if result.returncode == 0:
            # Возвращаем результат в теге <pre> для красивого форматирования
            if result.stdout:
                return f"<pre>{result.stdout}</pre>"
            else:
                return "<pre>Command executed successfully but produced no output.</pre>"
        else:
            # Возвращаем ошибку, если команда не выполнилась
            error_msg = result.stderr if result.stderr else "Unknown error occurred"
            return f"<pre>Error executing ps command: {error_msg}</pre>", 500

    except Exception as e:
        return f"<pre>Error: {str(e)}</pre>", 500


if __name__ == "__main__":
    app.run(debug=True)