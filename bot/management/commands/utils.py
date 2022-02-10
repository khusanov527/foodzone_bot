from bot.models import BotUser, Meal

class Message:
    HOME_MSG = "HOME MSG"
    ABOUT_MSG = "ABOUT MSG"
    KORZINKA_MSG = "KORZINKA MSG"
    MENU_MSG = "MENU MSG"
    MEAL_MSG = "MEAL MSG"

class ButtonText:
    HOME_BUTTON_TEXT = "HOME"
    ABOUT_BUTTON_TEXT = "ABOUT"
    KORZINKA_BUTTON_TEXT = "KORZINKA"
    MENU_BUTTON_TEXT = "MENU"
    MEAL_BUTTON_TEXT = "MEAL"

class ContextData:    
    ABOUT = "about"
    HOME = "home"
    KORZINKA = "korzinka"
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
