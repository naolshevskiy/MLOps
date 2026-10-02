from pathlib import Path
import logging
import json
import csv
import sys

logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "data" / "llm_log.csv"

class LogParserError(Exception):
    pass

with open(file_path, "r", newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    report = []
    
    for line_number, row in enumerate(reader, start=1):
        try:
            # Проверка 1: пустая строка
            if not row:
                raise LogParserError(f'Пустая строка {line_number}')
            
            # Проверка 2: неверное количество полей
            if len(row) != 5:
                raise LogParserError(f'Неверное количество полей в строке {line_number}: {len(row)}')
            
            # Извлекаем данные по индексам
            data = row[0].strip()
            model = row[1].strip().lower()
            tokens = int(row[2].strip())
            call = int(row[3].strip())
            cost = float(row[4].strip())
            
            # Проверка 3: пустые значения после strip()
            if not data or not model:
                raise LogParserError(f'Пустые данные в строке {line_number}')
            
            report.append({
                'data': data,
                'model': model,
                'tokens': tokens,
                'call': call,
                'cost': cost
            })
            
        except (ValueError, IndexError, LogParserError) as err:
            logging.warning(err)
            continue

# Агрегация по моделям
model_costs = {}
for item in report:
    model_costs.setdefault(item['model'], 0)
    model_costs[item['model']] += item['cost']

# Сортировка по убыванию стоимости
model_cost = sorted(model_costs.items(), key=lambda x: x[1], reverse=True)

# Подсчет общей суммы
total_sum = round(sum(cost for model, cost in model_cost), 6)

# Вывод таблицы в консоль
print("Модель                    | Стоимость")
print("-" * 40)
for model, cost in model_cost:
    print(f"{model:<25} | {cost:.6f}")
print("-" * 40)
print(f"{'ИТОГО':<25} | {total_sum:.6f}")

# Формирование финальной структуры для JSON
final_report = {
    'models': [],
    'total_cost': total_sum
}

for model, cost in model_cost:
    final_report['models'].append({
        'model': model,
        'cost': cost
    })

# Запись в JSON
with open("report.json", "w", encoding='utf-8') as f:
    json.dump(final_report, f, ensure_ascii=False, indent=4)

sys.exit(0)
