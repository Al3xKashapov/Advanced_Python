"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    """
    Функциональный валидатор для проверки длины числа.
    """
    def _number_length(form: FlaskForm, field: Field):
        if field.data is None:
            return

        # Преобразуем число в строку для подсчета цифр
        num_str = str(abs(field.data))
        length = len(num_str)

        if length < min or length > max:
            if message is None:
                raise ValidationError(f"Number length must be between {min} and {max} digits")
            raise ValidationError(message)

    return _number_length


class NumberLength:
    """
    Класс-валидатор для проверки длины числа.
    """

    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        if field.data is None:
            return

        # Преобразуем число в строку для подсчета цифр
        num_str = str(abs(field.data))
        length = len(num_str)

        if length < self.min or length > self.max:
            if self.message is None:
                raise ValidationError(f"Number length must be between {self.min} and {self.max} digits")
            raise ValidationError(self.message)