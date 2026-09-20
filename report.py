#!/usr/bin/env python3
num_lines = 10
stroki = []
final = []
with open('/home/naolshevskiy/learning/ai-course/llm-cost-cli/data/llm_log.csv', 'r') as f:
    for line in range(num_lines):
        line = f.readline()
        stroki.append(line)

for i in stroki:
    zapytaia = i.strip().split(",")
    k = " ".join(zapytaia)
    final.append(k)
print(f'Всего записей: {num_lines}\n')

result = final[:3]
for line in result:
    print(line)
