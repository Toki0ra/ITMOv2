# Практика 5. OpenSpec в brownfield

Ветка: `practice_05`.

## Что сделано

1. Установлен OpenSpec `1.14.1` и инициализирован проект: `openspec init --profile core --tools opencode --language ru`.
2. Полный цикл фичи `add-word-frequencies` в существующем проекте: explore → propose → review → apply → verify → sync → archive.
3. В `openspec/config.yaml` добавлено правило для design: «Объясни взаимодействие диаграммой Mermaid», проверено на draft `my-next-feature`.
4. ДЗ 5: фича Word Frequency Explorer через второй SDD-фреймворк GitHub Spec Kit и согласование двух команд (UI + логика) в `dz/`.

## Результаты

- `openspec validate --specs`: 1 passed, 0 failed.
- Архив изменения: `openspec/changes/archive/2026-11-02-add-word-frequencies/`.
- Тесты `practices/practice_04`: 10 OK.
- ДЗ: `practices/practice_05/dz` — 19 тестов OK.

Подробности и доказательства — в [REPORT.md](REPORT.md).

## ДЗ

```bash
cd practices/practice_05/dz
make test
make run   # http://127.0.0.1:8067
```
