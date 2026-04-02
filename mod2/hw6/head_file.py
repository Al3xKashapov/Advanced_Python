"""
Реализуйте endpoint, который показывает превью файла, принимая на вход два параметра: SIZE (int) и RELATIVE_PATH —
и возвращая первые SIZE символов файла по указанному в RELATIVE_PATH пути.

Endpoint должен вернуть страницу с двумя строками.
В первой строке будет содержаться информация о файле: его абсолютный путь и размер файла в символах,
а во второй строке — первые SIZE символов из файла:

<abs_path> <result_size><br>
<result_text>

где abs_path — написанный жирным абсолютный путь до файла;
result_text — первые SIZE символов файла;
result_size — длина result_text в символах.

Перенос строки осуществляется с помощью HTML-тега <br>.

Пример:

docs/simple.txt:
hello world!

/preview/8/docs/simple.txt
/home/user/module_2/docs/simple.txt 8
hello wo

/preview/100/docs/simple.txt
/home/user/module_2/docs/simple.txt 12
hello world!
"""

from flask import Flask
import os

app = Flask(__name__)


@app.route('/preview/<int:size>/<path:relative_path>')
def preview_file(size, relative_path):
    """
    Показывает превью файла.
    Пример: /preview/8/simple.txt
    """
    # абсолютный путь
    abs_path = os.path.abspath(relative_path)

    # существование файла
    if not os.path.exists(abs_path):
        return "Ошибка: файл не найден", 404

    if not os.path.isfile(abs_path):
        return "Ошибка: указанный путь не является файлом", 400

    try:
        # читает только первые size символов
        with open(abs_path, 'r', encoding='utf-8') as f:
            result_text = f.read(size)

        result_size = len(result_text)

        # Вывод с HTML-тегами
        return f"<b>{abs_path}</b> {result_size}<br>{result_text}"

    except PermissionError:
        return "Ошибка: недостаточно прав для чтения файла", 403
    except UnicodeDecodeError:
        return "Ошибка: файл не является текстовым", 400
    except Exception as e:
        return f"Ошибка при чтении файла: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
