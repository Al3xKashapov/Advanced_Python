"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from typing import Collection, Type, Literal, Union
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection) -> None:
        """
        Инициализация контекстного менеджера

        @param errors: коллекция типов исключений, которые нужно игнорировать
        """
        self.errors = errors

    def __enter__(self) -> None:
        """Вход в контекстный менеджер"""
        pass

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        """
        Выход из контекстного менеджера

        @param exc_type: тип исключения
        @param exc_val: значение исключения
        @param exc_tb: traceback исключения
        @return: True если исключение нужно подавить, иначе None
        """
        # Если исключения нет, просто выходим
        if exc_type is None:
            return None

        # Проверяем, нужно ли игнорировать это исключение
        # exc_type может быть дочерним классом от указанных ошибок
        for error_type in self.errors:
            if issubclass(exc_type, error_type):
                return True  # Возвращаем True, чтобы подавить исключение

        # Если исключение не входит в игнорируемые, прокидываем его дальше
        return None