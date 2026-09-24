#!/usr/bin/env python3
with open('/home/naolshevskiy/learning/ai-course/llm-cost-cli/data/llm_log.csv', 'r') as f:
    lines = f.readlines()
dict = {}

for line in lines:
    try:
        spisok = line.split(",")
        model = spisok[1].lower()
        tokens = int(spisok[2])
        call = int(spisok[3])
        dict.setdefault(model, {'tokens': 0, "call": 0})
        dict[model]['tokens'] += tokens
        dict[model]['call'] += call
    except:
        pass

top5 = sorted(dict.items(), key=lambda x: x[1]['call'], reverse=True)[:5]

for model, data in top5:
    print(f"«{model}: {data['call']} вызов, {data['tokens']} токенов»")
