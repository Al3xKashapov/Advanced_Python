# Найденные ошибки в классе Person

## Ошибка 1: Отсутствует импорт datetime

**Исправление**: добавить `import datetime` в начало файла

## Ошибка 2: Неправильный расчёт возраста

**Было**: `return self.yob - now.year`
**Стало**: `return now.year - self.yob`

## Ошибка 3: set_name не меняет имя

**Было**: `self.name = self.name`
**Стало**: `self.name = name`

## Ошибка 4: set_address использует сравнение вместо присваивания

**Было**: `self.address == address`
**Стало**: `self.address = address`

## Ошибка 5: is_homeless использует несуществующую переменную

**Было**: `return address is None`
**Стало**: `return self.address == '' or self.address is None`