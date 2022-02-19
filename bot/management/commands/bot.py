# start third party packages
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import InlineKeyboardButton,  InlineKeyboardMarkup, InputMediaPhoto, KeyboardButton, Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.utils.request import Request
from bot.management.commands.func import about, amount, baskets, ha, home, location, menu, orders, sendLocation, yoq
# end third party packages

# start my packages
from bot.management.commands.utils import get_BotUser, Message, ButtonText, get_meal, group_username, ContextData
# end my packages

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(ButtonText.MENU_BUTTON_TEXT, callback_data=ContextData.MENU)
    ],
    [
        InlineKeyboardButton(ButtonText.ABOUT_BUTTON_TEXT, callback_data=ContextData.ABOUT),
        InlineKeyboardButton(ButtonText.KORZINKA_BUTTON_TEXT, callback_data=ContextData.KORZINKA)
    ],
    [
        InlineKeyboardButton("📜 Buyurtmalar tarixi", callback_data="orders")
    ]
    
])
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    if user.is_active:
        update.message.reply_html(Message.HOME_MSG, reply_markup=keyboard)
        return 4
    update.message.reply_html("Ismingizni kiriting")
    return 1

def first_name(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    user.first_name = update.message.text
    user.save()

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton('📲 Kontaktni jo\'natish', request_contact=True)]],
                                            resize_keyboard=True)
    update.message.reply_html("📲 Telefon nomeringizni yuboring", reply_markup=reply_markup)
    return 3

def phonenumber(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    user.phone = update.message.contact.phone_number
    user.is_active = True
    user.save()
    update.message.reply_html(Message.HOME_MSG, reply_markup=keyboard)
    return 4

class Command(BaseCommand):
    help = "Telegram bot"
    
    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token = settings.TOKEN,
            base_url = settings.PROXY_URL,
        )
        updater = Updater(
            bot=bot,
            use_context= True,

        )

        def entryPoints():
            return [
                        CommandHandler('start', start),
                        CallbackQueryHandler(about , pattern=f"^({ContextData.ABOUT})$"),
                        CallbackQueryHandler(home, pattern=f"^({ContextData.HOME})$"),
                        CallbackQueryHandler(amount, pattern="^(amount)$"),
                        CallbackQueryHandler(baskets, pattern="^(basket)$"),
                        CallbackQueryHandler(sendLocation, pattern="^(order)$"),
                        CallbackQueryHandler(ha, pattern="^(ha)$"),
                        CallbackQueryHandler(yoq, pattern="^(yoq)$"),
                        CallbackQueryHandler(orders, pattern="^(orders)$"),
                        
                        # CallbackQueryHandler(self.menu, pattern=f"^({ContextData.MENU})$"),
                        CallbackQueryHandler(menu),
                    ]
        all_handler = ConversationHandler(
            entry_points=entryPoints(),
            states={
                    1: [
                        CommandHandler('start', start),
                        MessageHandler(Filters.text, first_name),
                    ],
                    3: [
                        CommandHandler('start', start),
                        MessageHandler(Filters.contact, phonenumber)
                    ],
                    4: entryPoints()+[
                        MessageHandler(Filters.location, location),
                    ],

            },
            fallbacks=[]
        )

        updater.dispatcher.add_handler(all_handler)
        updater.start_polling()
        updater.idle()