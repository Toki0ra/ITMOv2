# ДЗ 5. Две команды — одна фича (GitHub Spec Kit)

Фича: **Word Frequency Explorer** — экран, на котором пользователь вставляет текст и получает самые частые слова с частотами.

## Второй SDD-фреймворк

Выбран **GitHub Spec Kit**. Его форма воспроизведена в артефактах:

| Артефакт Spec Kit | Файл |
|---|---|
| Constitution | `constitution.md` |
| Spec команды UI | `specs/ui/spec.md` |
| Spec команды логики | `specs/logic/spec.md` |
| План | `plan.md` |
| Задачи | `tasks.md` |
| Контракт | `contracts/api.md` |

Код написан **после** согласования двух спецификаций и контракта.

## Как согласовывались две команды

1. Команда UI описала экран, действия, состояния `idle/loading/success/empty/error` и тексты ошибок.
2. Команда логики описала данные, алгоритм, правила валидации и HTTP-коды.
3. Команды сверили расхождения и зафиксировали общий контракт `contracts/api.md`:
   - запрос `POST /api/analyze` с `{text, limit}`;
   - ответ `{items[], total_words, unique_words}`;
   - единый формат ошибки `{error: {code, message}}`.
4. После согласования реализованы логика, HTTP-слой и UI, затем добавлен сквозной тест.

Итоговая таблица согласования — в `plan.md`.

## Структура

```
dz/
  constitution.md
  specs/ui/spec.md
  specs/logic/spec.md
  contracts/api.md
  plan.md
  tasks.md
  app/wordstats.py      # чистая логика
  app/server.py         # HTTP по контракту
  app/static/index.html # UI и состояния
  tests/test_logic.py
  tests/test_http.py    # HTTP + сквозной контракт
  Makefile
```

## Запуск

```bash
cd practices/practice_05/dz
make test     # 19 тестов
make run      # http://127.0.0.1:8067
```

Если `make` не установлен:

```bash
python -m unittest discover -s tests -v
python -m app.server
```

## Сквозная проверка

Тест `tests/test_http.py::test_end_to_end_contract` воспроизводит сценарий из контракта:

- вход: `"b a b c a b"`, `limit=3`;
- ожидание: `items = [b:3, a:2, c:1]`, `total_words=6`, `unique_words=3`;
- факт: `HTTP 200` и точное совпадение JSON.

Результат: `Ran 19 tests ... OK`.
