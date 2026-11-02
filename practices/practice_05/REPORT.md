# Отчёт по практике 5. SDD в существующем проекте: OpenSpec в brownfield

Ветка: `practice_05`.
Дата выполнения: 2026-11-02.

## Окружение

| Проверка | Результат |
|---|---|
| `node --version` | `v24.11.1` (требование ≥ 20.19.0 выполнено) |
| `npm install -g @fission-ai/openspec@1.14.1` | установлено |
| `openspec --version` | `1.14.1` |
| `openspec init --profile core --tools opencode --language ru` | созданы `openspec/`, `.opencode/commands/opsx-*`, `.opencode/skills/openspec-*` |
| `openspec list --json` | `{"changes": [], "root": {"path": "...", "source": "nearest"}}` |

## Часть 1. Полный цикл фичи

### Выбранная фича

Добавление `word_frequencies(text)` в существующий модуль `practices/practice_04/app/metrics.py`. Это brownfield-изменение: модуль уже содержит `sum_list` и `wordcount`, их поведение сохраняется.

Границы:

- токены делятся по пробельным символам (`str.split()`);
- ключи приводятся к нижнему регистру через `str.lower()`;
- пунктуация **не** удаляется;
- пустой ввод даёт `{}`;
- не-строка даёт `TypeError`;
- топ-N, стемминг, n-граммы и CLI не входят в изменение.

### Explore

Прочитаны `practices/practice_04/app/metrics.py` и `practices/practice_04/tests/test_metrics.py`. Baseline до изменений:

```text
python -m unittest discover -s tests -v
Ran 4 tests ... OK
```

Команда проверки: `python -m unittest discover -s tests -v` в `practices/practice_04`.

### Propose

Создано изменение `add-word-frequencies`:

```bash
openspec new change "add-word-frequencies"
```

Артефакты:

- `proposal.md` — зачем и что меняется, границы, impact;
- `specs/metrics/spec.md` — 4 требования и 12 сценариев;
- `design.md` — решения: `text.split()`, `str.lower()`, обычный `dict`, проверка типа в начале;
- `tasks.md` — TDD-порядок: сначала падающие тесты, затем реализация.

### Review

Независимый ревьюер (отдельный агент, read-only) нашёл расхождения:

1. «разбиение по пробелам» vs `text.split()` для всех пробельных символов;
2. недостижимая red-фаза из-за порядка задач;
3. не покрыта заявленная граница «пунктуация сохраняется»;
4. не покрыты ложные значения `None`, `False`, `0`, `[]`;
5. требование «без учёта регистра» шире, чем `str.lower()`.

Все пункты исправлены до реализации: уточнена спецификация, добавлены сценарии, задачи переупорядочены под TDD. Повторная проверка:

```text
openspec validate add-word-frequencies --type change --strict --no-interactive
Change 'add-word-frequencies' is valid
```

### Apply

1. Сначала добавлены тесты — они падали:

```text
ImportError: cannot import name 'word_frequencies' from 'app.metrics'
```

2. Затем добавлена реализация в `practices/practice_04/app/metrics.py`.
3. Полный прогон:

```text
Ran 10 tests in 0.001s
OK
```

Старые 4 теста (`sum_list`, `wordcount`) остались зелёными.

### Verify

Независимый проверяющий агент прогнал основной, ошибочный и старый сценарии в формате «ожидание → факт → доказательство». Вердикт: **PASS**. Примеры:

| Сценарий | Ожидание | Факт | Доказательство |
|---|---|---|---|
| `"b a b c a b"` | `b:3, a:2, c:1` | совпало | `test_word_frequencies_repeated` |
| `"  a\tb\n a "` | `a:2, b:1` | совпало | `test_word_frequencies_whitespace` |
| `"cat, cat"` | `cat,:1`, `cat:1` | совпало | `test_word_frequencies_keeps_punctuation` |
| `None`, `False`, `0`, `123`, `[]` | `TypeError` | `TypeError` | `test_word_frequencies_type` |
| `sum_list([1,2,3.5])` | `6.5` | `6.5` | `test_sum_list` |

### Sync / Archive

Main-спецификация создана из delta: `openspec/specs/metrics/spec.md`.

```text
openspec validate --specs --no-interactive
✓ spec/metrics
Totals: 1 passed, 0 failed (1 items)
```

Архивирование:

```text
openspec archive add-word-frequencies --yes --json
archivedAs: 2026-11-02-add-word-frequencies
specsUpdated: false   # main spec уже синхронизирован вручную
```

Итог: `openspec list` → `No active changes found`.

## Часть 2. Настройка OpenSpec под проект

В `openspec/config.yaml` добавлено:

```yaml
rules:
  design:
    - Объясни взаимодействие диаграммой Mermaid.
```

Создан draft `my-next-feature` (функция `top_words` поверх `word_frequencies`, код не реализовывался). Проверка применения правила:

```text
openspec instructions design --change "my-next-feature" --json
rules: Объясни взаимодействие диаграммой Mermaid.
```

К тому же draft применено правило — в `design.md` добавлен раздел `Interaction` с Mermaid-диаграммой. Смысл и границы сохранены, изменена только форма. Фрагмент diff:

```diff
+## Interaction
+
+```mermaid
+flowchart TD
+    A["top_words(text, limit=3)"] --> B{"text is str?"}
+    B -- нет --> E["TypeError"]
+    B -- да --> C{"limit is int and limit > 0?"}
+    C -- нет --> F["ValueError"]
+    C -- да --> D["word_frequencies(text)"]
+    D --> G["items = counts.items()"]
+    G --> H["sorted by (-count, word)"]
+    H --> I["slice [:limit]"]
+    I --> J["list of (word, count)"]
+```
+
 ## Risks / Trade-offs
```

Проверка: `openspec validate my-next-feature --type change --strict --no-interactive` → valid. Правило остаётся в конфиге для будущих изменений.

## ДЗ 5. Две команды — одна фича

Второй SDD-фреймворк: **GitHub Spec Kit** (артефакты `constitution.md`, две `spec.md`, `plan.md`, `tasks.md`).

Фича: **Word Frequency Explorer** — экран для подсчёта частот слов.

### Согласование до кода

- Команда UI (`specs/ui/spec.md`): экран, действия, состояния `idle/loading/success/empty/error`, тексты ошибок, клиентская валидация.
- Команда логики (`specs/logic/spec.md`): данные, алгоритм, сортировка, валидация, HTTP-коды.
- Общий контракт (`contracts/api.md`): `POST /api/analyze`, поля `text`/`limit`, ответ `items/total_words/unique_words`, единый формат ошибки `{error: {code, message}}`, коды `invalid_text`, `invalid_limit`, `invalid_body`, `text_too_long`, `not_found`, `method_not_allowed`, `internal_error`.

Расхождения, снятые при согласовании: кто считает частоты (логика), кто сортирует (логика), формат ошибки (единый), двойная валидация `limit` (UI + логика).

### Реализация

- `app/wordstats.py` — чистая логика `analyze(text, limit)`;
- `app/server.py` — HTTP по контракту;
- `app/static/index.html` — UI и состояния;
- `tests/test_logic.py`, `tests/test_http.py` — юнит и сквозные проверки.

### Сквозная проверка

```text
cd practices/practice_05/dz
python -m unittest discover -s tests -v
Ran 19 tests in 0.608s
OK
```

Ключевой тест `test_end_to_end_contract`: `"b a b c a b"`, `limit=3` → `items=[b:3, a:2, c:1]`, `total_words=6`, `unique_words=3`.

## Сравнение OpenSpec и GitHub Spec Kit

| Критерий | OpenSpec (часть 1) | GitHub Spec Kit (ДЗ 5) |
|---|---|---|
| Единица работы | изменение как отдельный артефакт: proposal → spec → design → tasks | конституция проекта + спека → план → задачи; отдельные спеки на команды |
| Артефакты | change + main spec, design.md, tasks.md, archive | `constitution.md`, `specs/ui/spec.md`, `specs/logic/spec.md`, `plan.md`, `tasks.md`, `contracts/api.md` |
| Жизненный цикл | CLI: создать изменение, проверить, синхронизировать, заархивировать | ручная эмуляция: сначала контракт и спеки, потом plan/tasks, потом код |
| Валидация | `openspec validate --strict` и `--specs` | самопроверка по условиям приёмки и тестам; CLI Spec Kit не использовался |
| Командная работа | один поток изменений; независимый ревьюер-агент | две команды с отдельными спеками и общим контрактом API |
| Brownfield | сильная сторона: встроились в существующий модуль, старые тесты остались зелёными | применим, но требует явно зафиксировать границы и контракт до кода |
| Где использовали | `add-word-frequencies`, draft `my-next-feature` | `practices/practice_05/dz` — Word Frequency Explorer |
| Что дал | дисциплину артефактов, проверяемость и историю изменений | согласование интерфейсов до кода и разделение ответственности команд |
| Ограничения | больше церемоний на маленькой фиче; зависимость от CLI | без CLI легко пропустить валидацию; больше ручной синхронизации |

Вывод: OpenSpec лучше подходит, когда важны аудит, история и строгий жизненный цикл изменения в одном репозитории. GitHub Spec Kit удобнее для параллельной работы нескольких команд, где сначала нужно договориться о контракте, а потом писать код. В нашей работе OpenSpec дал проверяемый след изменения, а Spec Kit — явный контракт UI ↔ Logic и сквозной тест `test_end_to_end_contract`.

## Итоговые артефакты

| Что | Где |
|---|---|
| OpenSpec-конфиг | `openspec/config.yaml` |
| Main-спека | `openspec/specs/metrics/spec.md` |
| Архив изменения | `openspec/changes/archive/2026-11-02-add-word-frequencies/` |
| Draft с Mermaid | `openspec/changes/my-next-feature/` |
| Реализация фичи | `practices/practice_04/app/metrics.py`, `tests/test_metrics.py` |
| ДЗ 5 | `practices/practice_05/dz/` |
