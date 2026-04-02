"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""
import sys


def get_mean_size(ls_output: str) -> float:
    """
    Вычисляет средний размер файла из вывода команды ls -l.

    Args:
        ls_output: Строка с выводом ls -l.

    Returns:
        Средний размер файла в байтах.
    """
    lines = ls_output.strip().split('\n')
    total_size = 0
    file_count = 0

    # Пропуск 1й строки
    for line in lines[1:]:
        if not line:
            continue
        parts = line.split()
        # В выводе ls -l размер файла — это 5-й столбец (индекс 4)
        if len(parts) > 4:
            try:
                size = int(parts[4])
                total_size += size
                file_count += 1
            except ValueError:
                # Если не число - пропуск
                continue

    if file_count == 0:
        return 0.0
    return total_size / file_count


if __name__ == '__main__':
    # данные из стандартного ввода
    data = sys.stdin.read()
    if data:
        mean_size = get_mean_size(data)
        print(f"{mean_size:.2f}")  # Вывод с двумя знаками после запятой
    else:
        print("Нет входных данных.")