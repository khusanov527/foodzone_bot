import json
from django.conf import settings

# from bot.models import BotUser, Meal
class Basket:
    def __init__(self, tg_id, product_id):
        self.tg_id = tg_id
        self.product_id = product_id
        self.fileAddress = BASE_DIR / 'bot/basket.json'
    # @property
    # def user(self):
    #     try:
    #         return BotUser.objects.select_for_update().get(tg_id=self.tg_id)
    #     except BotUser.DoesNotExist:
    #         return None
    
    # @property
    # def product(self):
    #     try:
    #         return Meal.objects.select_for_update().get(id=self.product_id)
    #     except Meal.DoesNotExist:
    #         return None
    
    @property
    def data(self):
        with open(self.fileAddress) as f:
            return json.load(f)
    def writeJson(self, basket):
        with open(self.fileAddress, 'w') as f:
            json.dump(basket, f)

    def getOrCreateObject(self):
        basket = self.data
        for i in range(len(basket)):
            if basket[i].get('tg_id') == self.tg_id and basket[i].get('product_id') == self.product_id:
                return {'index':i, 'data':basket[i]}
        data = {"tg_id":self.tg_id, "product_id":self.product_id, "amount":1, 'is_basket':False}
        basket.append(data)

        self.writeJson(basket)
        return {'index':len(basket), 'data':data}
    
    def increment(self):
        basket = self.data
        for i in range(len(basket)):
            if basket[i].get('tg_id') == self.tg_id and basket[i].get('product_id') == self.product_id:
                basket[i]['amount'] = basket[i]['amount']+1
        self.writeJson(basket)

    def decrement(self):
        basket = self.data
        for i in range(len(basket)):
            if basket[i].get('tg_id') == self.tg_id and basket[i].get('product_id') == self.product_id:
                if basket[i].get('is_basket') == True:
                    if basket[i]['amount'] == 1:
                        basket[i]['amount'] = basket[i]['amount']-1
                        del basket[i]
                    else:
                        basket[i]['amount'] = basket[i]['amount']-1
                else:
                    if basket[i]['amount'] != 1:
                        basket[i]['amount'] = basket[i]['amount']-1
        self.writeJson(basket)
    