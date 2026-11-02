# Tasks

## 1. Тесты (red)

- [ ] 1.1 Добавить тесты на сортировку, ограничение `limit`, равные частоты и пустой текст. Проверка: новые тесты падают до реализации.
- [ ] 1.2 Добавить тесты на `TypeError` для текста и `ValueError` для `limit <= 0` и `1.5`. Проверка: тесты падают до реализации.

## 2. Реализация (green)

- [ ] 2.1 Добавить `top_words(text, limit=3)` в `practices/practice_04/app/metrics.py` поверх `word_frequencies`. Проверка: тесты группы 1 проходят.
- [ ] 2.2 Запустить `python -m unittest discover -s tests -v` в `practices/practice_04`. Проверка: результат `OK`, старые тесты зелёные.

## Workflow follow-up

- Выполнить `/opsx-sync my-next-feature` и `/opsx-archive my-next-feature` после приёмки и реализации.
