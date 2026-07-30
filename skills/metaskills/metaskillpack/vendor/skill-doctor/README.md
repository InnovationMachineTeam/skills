# skill-doctor

Мета-навык для диагностики, минимального ремонта и подтверждения восстановления агентных навыков.

## Отличие от optimizer

- `skill-doctor` ищет неисправность и восстанавливает last-known-good поведение;
- `skill-optimizer` улучшает уже здоровый навык по измеримой метрике;
- `skill-architect` создаёт новый навык.

## Health-модель

- `UNSAFE` — неконтролируемые полномочия, утечка данных или опасные действия;
- `BROKEN` — основной путь не загружается или не выполняется;
- `DEGRADED` — навык работает с подтверждённым неблокирующим дефектом;
- `HEALTHY` — в проверенном объёме материальный дефект не подтверждён.

## Структура

```text
skill-doctor/
├── SKILL.md
├── agents/openai.yaml
├── prompts/          # общий и восемь диагностических промптов
├── references/       # triage, repair и recovery-методика
├── evals/            # routing- и behavioral-сценарии
└── scripts/          # doctor и сравнение health-отчётов
```

## Диагностика

```bash
python3 scripts/doctor_skill.py path/to/skill
python3 scripts/doctor_skill.py path/to/skill --format json --output health-before.json
```

После разрешённого ремонта:

```bash
python3 scripts/doctor_skill.py path/to/skill --format json --output health-after.json
python3 scripts/compare_health_reports.py health-before.json health-after.json
python3 scripts/check_evals.py evals
```

Статический health-отчёт не заменяет повторное выполнение исходного failing-case. Без него recovery остаётся `UNVERIFIED`.
