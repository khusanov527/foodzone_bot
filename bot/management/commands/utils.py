from bot.models import BotUser, Meal

class Message:
    HOME_MSG = "Yetkazib berish Toshkent shahrida soat 09:00 dan 23:00 gacha ishlaydi"
    ABOUT_MSG = "π‘ <b>Mazalli hotdoglar , sevimli burgerlar π\nKafolatlanngan ta'm va tez yetkazib berish π\nβοΈ 95 476 14 97\nβοΈ71 276 14 97</b>"
    KORZINKA_MSG = "π₯ <b>Savat:</b>\n\n"
    MENU_MSG = "π <b>FastFood buyurtma berish</b>"
    MEAL_MSG = "FastFood"

class ButtonText:
    HOME_BUTTON_TEXT = "Bosh sahifa"
    ABOUT_BUTTON_TEXT = "π‘ Biz haqimizda"
    KORZINKA_BUTTON_TEXT = "π₯ Savat"
    MENU_BUTTON_TEXT = "π Menyu"
    MEAL_BUTTON_TEXT = "FastFoodπ"

class ContextData:    
    ABOUT = "about"
    HOME = "home"
    KORZINKA = "basket"
    MENU = "menu"
    MEAL = "meal"

ContextData = ContextData()
ButtonText = ButtonText()
Message = Message()
group_username="@nbpplast"


def get_BotUser(tg_id) -> BotUser:
    
    return BotUser.objects.get_or_create(tg_id=tg_id)[0]

def get_meal(id):
    try:
        return Meal.objects.get(id=id)
    except Meal.DoesNotExist:
        return None
