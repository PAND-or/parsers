import requests
import pprint
import json
req = requests.get("http://min-prices.aviasales.ru/calendar_preload?origin=LED&destination=NCE&one_way=true")

data = json.loads(req.text)
pprint.pprint(data)
print(data['best_prices'][0])
















