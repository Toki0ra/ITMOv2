# Tasks

## 1. Тесты (red)

- [x] 1.1 Обновить импорт в `practices/practice_04/tests/test_metrics.py` и добавить тесты на повторяющиеся слова, разный регистр, смешанные пробельные символы (`"  a\tb\n a "`), сохранение пунктуации (`"cat, cat"`), пустую строку и строку только из пробелов. Проверка: `python -m unittest discover -s tests -v` в `practices/practice_04` показывает падение новых тестов до реализации.
- [x] 1.2 Добавить тесты на `TypeError` для `None`, `False`, `0`, `123`, `["word"]` и `[]`. Проверка: тесты падают до реализации и покрывают каждое ложное значение отдельно.

## 2. Реализация (green)

- [x] 2.1 Добавить `word_frequencies(text)` в `practices/practice_04/app/metrics.py`: проверка `isinstance(text, str)` в начале, затем `text.split()` без аргументов и `str.lower()` для токенов. Проверка: тесты из группы 1 проходят.
- [x] 2.2 Запустить полный набор `python -m unittest discover -s tests -v` в `practices/practice_04`. Проверка: результат `OK`, все старые тесты (`sum_list`, `wordcount`) по-прежнему зелёные.

## Workflow follow-up

- Выполнить `/opsx-sync add-word-frequencies` и сверить diff спецификации с принятым поведением.
- Выполнить `/opsx-archive add-word-frequencies` после приёмки.
