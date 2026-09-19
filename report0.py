#!/usr/bin/env python3

model = str('DeepSeek')
tokens = 1000
money = 5
result = float(tokens) * 10 / 100
print(model + ' ' + 'потратил' + ' '  + str(tokens) + 'токенов')
print('Количество затраченных токенов от всего объемы:' + str(result) + '%')
print(f'Твоя модель {model}, твое колво токенов {tokens}, это стоит {money}')
