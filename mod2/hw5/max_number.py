"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


@app.route('/max_number/<path:numbers>')
def max_number(numbers):
    """
    Находит максимальное число из переданных в URL.
    Пример: /max_number/10/2/9/1 -> Максимальное число <i>10</i>
    """
    # Раздел строки по \
    parts = numbers.split('/')
    numbers_list = []

    for part in parts:
        if not part:  # пропуск пустых
            continue

        try:
            # Определение типа
            if '.' in part:
                num = float(part)
            else:
                num = int(part)
            numbers_list.append(num)
        except ValueError:
            # Если не число, -
            continue

    if not numbers_list:
        return "Ошибка: не передано ни одного числа.", 400

    max_num = max(numbers_list)
    return f"Максимальное число: <i>{max_num}</i>"

if __name__ == "__main__":
    app.run(debug=True)
