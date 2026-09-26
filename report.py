#!/usr/bin/env python3
with open('/home/naolshevskiy/learning/ai-course/llm-cost-cli/data/llm_log.csv', 'r') as f:
    lines = f.readlines()
counts = {}
skipping = 0
line_count = sum(1 for line in lines)

for line in lines:
     try:
        spisok = line.split(",")
        if len(spisok) != 5:
            print(f"DEBUG: строка не прошла по длине: {line.strip()}")
            skipping += 1
            continue
        model = spisok[1].lower()
        if not model:
            print(f"DEBUG: нет названия модели: {line.strip()}")
            continue
        tokens = int(spisok[2])
        call = int(spisok[3])
        money = float(spisok[4])
     except (ValueError, IndexError):
         print(f"DEBUG: строка не прошла по типу: {line.strip()}")
         skipping += 1
         continue

     counts.setdefault(model, {'tokens': 0, "call": 0, "money": 0})
     counts[model]['tokens'] += tokens
     counts[model]['call'] += call
     counts[model]['money'] += money

report = sorted(counts.items(), key = lambda x: x[1]['money'], reverse = True)

full_summ = round(sum(counts[model]['money'] for model in counts), 6)

print("Топ моделей по стоимости:")
for model, data in report:
       print(f"{model}: {data['money']} $")


print(f'\nИТОГИ:\nПрочитано:{line_count}\nПропущено:{skipping}\nСумма:{full_summ}')
