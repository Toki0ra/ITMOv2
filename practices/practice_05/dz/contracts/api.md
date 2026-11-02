# Общий контракт UI ↔ Logic

Согласован командами 1 и 2 до генерации кода. Любое изменение проходит через обе команды.

## Endpoint

`POST /api/analyze`

Заголовки запроса: `Content-Type: application/json`.

Тело запроса:

| Поле | Тип | Обязательно | Ограничения |
|---|---|---|---|
| `text` | string | да | длина ≤ 10000 символов |
| `limit` | integer | нет | 1..100, по умолчанию 3 |

## Успешный ответ

Статус `200`, `Content-Type: application/json`.

```json
{
  "items": [{"word": "b", "count": 3}, {"word": "a", "count": 2}],
  "total_words": 6,
  "unique_words": 3
}
```

Гарантии:

- `items` отсортирован по убыванию `count`, затем по возрастанию `word`.
- `len(items) <= limit`.
- `total_words >= unique_words >= len(items)`.
- `count >= 1`, `word` — непустая строка в нижнем регистре.

## Ошибка

Статус `4xx`/`5xx`, `Content-Type: application/json`:

```json
{"error": {"code": "invalid_limit", "message": "Количество слов должно быть от 1 до 100"}}
```

| HTTP | code | Когда |
|---:|---|---|
| 400 | `invalid_body` | тело не JSON-объект |
| 400 | `invalid_text` | `text` отсутствует или не строка |
| 400 | `invalid_limit` | `limit` не целое или вне 1..100 |
| 405 | `method_not_allowed` | метод не POST для `/api/analyze` |
| 413 | `text_too_long` | длина `text` > 10000 |
| 404 | `not_found` | неизвестный путь |
| 500 | `internal_error` | непредвиденная ошибка |

## Страница UI

`GET /` → `200`, `text/html; charset=utf-8`, страница с элементами из UI-спеки.

## Сквозной сценарий приёмки

1. Пользователь вводит `"b a b c a b"` и `limit=3`, нажимает «Анализировать».
2. UI отправляет контрактный запрос.
3. Логика возвращает `items=[b:3, a:2, c:1]`, `total_words=6`, `unique_words=3`.
4. UI показывает три строки в этом порядке и статус «Готово».

Сценарий проверяется тестом `tests/test_http.py::test_end_to_end_contract`.
