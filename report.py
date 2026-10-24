from pathlib import Path
import logging
import json
import csv
import sys
import argparse

logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "data" / "llm_log.csv"


class LogParserError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser(description="Парсер логов вызовов LLM-моделей")
    parser.add_argument("--file", "-f", type=str, help="Путь до файла CSV", default=file_path)
    parser.add_argument("--top", "-t", type=int, help="Количество моделей в топе", default=None)
    parser.add_argument("--json", "-j", type=str, help="Путь куда положить JSON", default="report.json")
    args = parser.parse_args()

    with open(args.file, "r", newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        report = []

        for line_number, row in enumerate(reader, start=1):
            try:
                if not row:
                    raise LogParserError(f'Пустая строка {line_number}')

                if len(row) != 5:
                    raise LogParserError(f'Неверное количество полей в строке {line_number}: {len(row)}')

                data = row[0].strip()
                model = row[1].strip().lower()
                tokens = int(row[2].strip())
                call = int(row[3].strip())
                cost = float(row[4].strip())

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
    for model, cost in model_cost[:args.top]:
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
    with open(args.json, "w", encoding='utf-8') as f:
        json.dump(final_report, f, ensure_ascii=False, indent=4)

    sys.exit(0)


if __name__ == "__main__":
    main()
