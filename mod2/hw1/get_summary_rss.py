"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def get_summary_rss(ps_output_file_path: str) -> str:
    """
    Считывает файл с выводом команды 'ps aux' и возвращает суммарный RSS в человекочитаемом формате.

    Args:
        ps_output_file_path: Путь к файлу с выводом ps aux.

    Returns:
        Строка с суммарным объёмом памяти, например, "555.55 MiB".
    """
    total_rss_kb = 0

    try:
        with open(ps_output_file_path, 'r') as file:
            # Пропуск 1й строки
            lines = file.readlines()[1:]

            for line in lines:
                columns = line.split()
                # Столбец RSS (память) обычно находится на 5-й позиции (индекс 5)
                # в выводе 'ps aux'
                if len(columns) > 5:
                    try:
                        rss = int(columns[5])
                        total_rss_kb += rss
                    except ValueError:
                        # Если значение не число, пропускаем строку
                        continue
    except FileNotFoundError:
        return f"Ошибка: файл '{ps_output_file_path}' не найден."

    # Форматирование в человекочитаемый вид
    # 1 KiB = 1024 B, но RSS в ps aux в KiB, поэтому начинаем с KiB
    size_names = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
    size_index = 0
    size_value = total_rss_kb * 1024  # в байты

    while size_value >= 1024 and size_index < len(size_names) - 1:
        size_value /= 1024.0
        size_index += 1

    # Округление до 2 знаков и выбор единицы измерения
    return f"{size_value:.2f} {size_names[size_index]}"


if __name__ == '__main__':
    path: str = 'output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
