import json
filename = 'basket.json'
with open(filename) as f:
    basket = json.load(f)
for item in basket:
    if item.get('user_id') == 1 and item.get('product_id') == 1:
        print(item)