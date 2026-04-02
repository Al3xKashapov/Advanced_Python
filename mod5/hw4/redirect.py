"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""

import sys
import traceback
from types import TracebackType
from typing import Type, Literal, IO, Optional


class Redirect:
    def __init__(self, stdout: Optional[IO] = None, stderr: Optional[IO] = None) -> None:
        """
        Инициализация контекстного менеджера для перенаправления потоков

        @param stdout: IO объект для перенаправления stdout (например, файл)
        @param stderr: IO объект для перенаправления stderr (например, файл)
        """
        self.stdout = stdout
        self.stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        """Перенаправляем потоки при входе в контекст"""
        # Сохраняем старые потоки
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        # Перенаправляем stdout если указан
        if self.stdout is not None:
            sys.stdout = self.stdout

        # Перенаправляем stderr если указан
        if self.stderr is not None:
            sys.stderr = self.stderr

        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        """
        Восстанавливаем потоки при выходе из контекста

        Если произошло исключение, записываем его в stderr (если он был перенаправлен)
        """
        # Если было исключение и stderr был перенаправлен, записываем traceback
        if exc_type is not None and self.stderr is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb, file=self.stderr)
            self.stderr.flush()

        # Восстанавливаем старые потоки
        if self.old_stdout is not None:
            sys.stdout = self.old_stdout

        if self.old_stderr is not None:
            sys.stderr = self.old_stderr

        # Закрываем файлы, если они были открыты
        if self.stdout is not None and hasattr(self.stdout, 'close'):
            self.stdout.flush()

        if self.stderr is not None and hasattr(self.stderr, 'close'):
            self.stderr.flush()

        # Возвращаем None, чтобы исключение продолжило распространяться
        return None