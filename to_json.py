import json

stroke = []

with open('cenzura.txt', encoding='utf-8') as file:
    for index in file:
        number = index.lower().split('\n')[0]
        if number != '':
            stroke.append(number)

with open('cenzura.json', 'w', encoding='utf-8') as file_one:
    json.dump(stroke, file_one)
