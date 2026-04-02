"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask

app = Flask(__name__)

# Структура хранения: storage[год][месяц][день] = сумма трат
storage = {}


def parse_date(date_str: str) -> tuple:
    """
    Преобразует строку даты YYYYMMDD в кортеж (год, месяц, день)
    """
    if len(date_str) != 8 or not date_str.isdigit():
        raise ValueError("Неверный формат даты. Используйте YYYYMMDD")

    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])

    if month < 1 or month > 12:
        raise ValueError("Неверный месяц (должен быть от 1 до 12)")
    if day < 1 or day > 31:
        raise ValueError("Неверный день (должен быть от 1 до 31)")

    return year, month, day


@app.route('/add/<date>/<int:number>')
def add_expense(date, number):
    """
    Сохраняет информацию о трате за указанный день.
    Пример: /add/20250101/1000
    """
    try:
        year, month, day = parse_date(date)
    except ValueError as e:
        return f"Ошибка: {str(e)}", 400

    # Используем setdefault для удобного создания вложенных словарей
    storage.setdefault(year, {}).setdefault(month, {}).setdefault(day, 0)
    storage[year][month][day] += number

    return f"Добавлена трата {number} руб. за {date}"


@app.route('/calculate/<int:year>')
def calculate_year(year):
    """
    Возвращает суммарные траты за указанный год.
    Пример: /calculate/2025
    """
    if year not in storage:
        return f"За {year} год трат не найдено.", 404

    total = 0
    for month_data in storage[year].values():
        total += sum(month_data.values())

    return f"Суммарные траты за {year} год: {total} руб."


@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year, month):
    """
    Возвращает суммарные траты за указанные год и месяц.
    Пример: /calculate/2025/1
    """
    if year not in storage or month not in storage[year]:
        return f"За {year}-{month:02d} месяц трат не найдено.", 404

    total = sum(storage[year][month].values())
    return f"Суммарные траты за {year}-{month:02d}: {total} руб."


@app.route('/storage')
def view_storage():
    """Просмотр всех сохранённых трат (для отладки)"""
    if not storage:
        return "Данные отсутствуют"

    result = "<h3>Все сохранённые траты:</h3>"
    for year, months in sorted(storage.items()):
        result += f"<b>{year} год:</b><br>"
        for month, days in sorted(months.items()):
            result += f"&nbsp;&nbsp;Месяц {month:02d}:<br>"
            for day, amount in sorted(days.items()):
                result += f"&nbsp;&nbsp;&nbsp;&nbsp;{day:02d}.{month:02d}.{year}: {amount} руб.<br>"
    return result
if __name__ == "__main__":
    app.run(debug=True)
