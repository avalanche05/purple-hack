from backend.app.utils.calculate import process_json
import json

duration = 1
price = 0
resource = 0

with open("тестовое задание.json") as input_file:
    process_json(json.load(input_file), duration, price, resource)
