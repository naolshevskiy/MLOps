#!/usr/bin/env python3
with open('/home/naolshevskiy/learning/ai-course/llm-cost-cli/data/llm_log.csv', 'r') as f:
    lines = f.readlines()

line_count = len(lines)


def parse_line(lines):
    counts = {}
    skippings = 0
    for line in lines:
        try:
            spisok = line.split(",")
            if len(spisok) != 5:
                skippings += 1
                continue
            model = spisok[1].lower()
            if not model:
                skippings += 1
                continue
            tokens = int(spisok[2])
            call = int(spisok[3])
            money = float(spisok[4])
        except (ValueError, IndexError):
            skippings += 1
            continue

        counts.setdefault(model, {'tokens': 0, "call": 0, "money": 0})
        counts[model]['tokens'] += tokens
        counts[model]['call'] += call
        counts[model]['money'] += money

    return counts, skippings

def format_row(counts, line_count, skippings):

    report = sorted(counts.items(), key=lambda x: x[1]['money'], reverse=True)
    full_summ = round(sum(counts[model]['money'] for model in counts), 6)
    report_mass = []
    for model, data in counts.items():
        report_mass.append(f"{model}: {data['money']}")
    report_str = '\n'.join(report_mass)
    result = f'Топ моделей по стоимости:\n{report_str}\n\nИТОГИ:\nПрочитано:{line_count}\nПропущено:{skippings}\nСумма:{full_summ}'
    return result


counts, skippings = parse_line(lines)
print(format_row(counts, line_count, skippings))
