# start third party packages
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import InlineKeyboardButton,  InlineKeyboardMarkup, KeyboardButton, Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.utils.request import Request
from bot.helpers import Basket
# end third party packages

# start my packages
from bot.models import BotUser, Meal, Menu
from bot.management.commands.utils import get_BotUser, Message, ButtonText, get_meal, group_username, ContextData
# end my packages

def comment():
    # def products(self, update: Update, context: CallbackContext):
    #     query = update.callback_query
    #     query.answer()
    #     query.delete_message()
    #     keyboard = InlineKeyboardMarkup([[
    #             InlineKeyboardButton("➕ оставить заявку", callback_data=application),
    #             InlineKeyboardButton("🔙 Назад", callback_data=home)
    #     ]])
            
        
    #     file = open(str(settings.STATIC_ROOT) +"\\Прайс NPB от 03.01.22.pdf", 'rb')
    #     query.message.reply_document(document=file, reply_markup=keyboard)

    # def social(self, update: Update, context: CallbackContext):
    #     query = update.callback_query
    #     query.answer()
    #     query.delete_message()
    #     keyboard = InlineKeyboardMarkup([[
    #             InlineKeyboardButton("Фейсбук", url="https://m.facebook.com/npbplast/"),
    #             InlineKeyboardButton("Инстаграм", url="https://instagram.com/npb_plast?utm_medium=copy_link"),
    #             InlineKeyboardButton("Телеграм", callback_data="https://t.me/npb_plast"),
    #         ],
    #         [
    #             InlineKeyboardButton("🔙 Назад", callback_data=home)
    #         ]
    #     ])
    #     query.message.reply_html("наши соть сети".title()+" 🌐", reply_markup=keyboard)


    # def application(self, update: Update, context: CallbackContext):
    #     query = update.callback_query
    #     query.answer(text=f'Спасибо за отправку заявки! ✅', show_alert=True)
    #     user_id = query.from_user.id
    #     user = get_BotUser(user_id)
    #     print(str(user))
    #     context.bot.send_message(chat_id=group_username, parse_mode="html", 
    #                 text='<b>{}</b>\n<b>👤Имя:</b> {}\n<b>📞Номер телефона:</b> {} '
    #                 .format('политиленвыйе трубы 🛠'.title(), user.get_full_name, user.phone))

    pass

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    if user.is_active:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(Message.MENU_MSG, callback_data=ContextData.MENU)
            ],
            [
                InlineKeyboardButton(Message.ABOUT_MSG, callback_data=ContextData.ABOUT),
                InlineKeyboardButton(Message.KORZINKA_MSG, callback_data=ContextData.KORZINKA)
            ],
            
        ])
        update.message.reply_html(Message.HOME_MSG, reply_markup=keyboard)
        return 4
    update.message.reply_html("Введите ваше имя")
    return 1

def first_name(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    user.first_name = update.message.text
    user.save()
    update.message.reply_html("Введите вашу фамилию")
    return 2

def last_name(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    user.last_name = update.message.text
    user.save()

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton('Поделиться контактом', request_contact=True)]],
                                            resize_keyboard=True)
    update.message.reply_html("Отправьте свой номер телефона", reply_markup=reply_markup)
    return 3

def phonenumber(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = get_BotUser(user_id)
    user.phone = update.message.contact.phone_number
    user.is_active = True
    user.save()
    keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(Message.MENU_MSG, callback_data=ContextData.MENU)
            ],
            [
                InlineKeyboardButton(Message.ABOUT_MSG, callback_data=ContextData.ABOUT),
                InlineKeyboardButton(Message.KORZINKA_MSG, callback_data=ContextData.KORZINKA)
            ],
            
        ])
    update.message.reply_html(Message.HOME_MSG, reply_markup=keyboard)
    return 4

class Command(BaseCommand):
    help = "Telegram bot"
    def home(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        query.message.delete()

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(Message.MENU_MSG, callback_data=ContextData.MENU)
            ],
            [
                InlineKeyboardButton(Message.ABOUT_MSG, callback_data=ContextData.ABOUT),
                InlineKeyboardButton(Message.KORZINKA_MSG, callback_data=ContextData.KORZINKA)
            ],
            
        ])
        query.message.reply_html(Message.HOME_MSG, reply_markup=keyboard)
    def about(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        query.message.delete()
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data=ContextData.HOME)]])
        query.message.reply_html(Message.ABOUT_MSG, reply_markup=keyboard)
    

    
    def meals(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        query.message.delete()
        print(query.data.split('menu/'))
        menu_id = int(query.data.split('menu/')[1])

        meals = Meal.objects.filter(menu_id=menu_id)
        index = 0
        keyboard = []

        for i in range(len(meals)):
            name = meals[i].name
            data = "menu/"+str(menu_id)+"/"+str(meals[i].id)
            if  i % 2 == 0 and i != 0:
                index += 1
            if i % 2 == 0:
                keyboard.append([InlineKeyboardButton(text=name, callback_data=data)])
            else:
                keyboard[index].append(InlineKeyboardButton(text=name, callback_data=data))

        keyboard.append([InlineKeyboardButton("🔙 Назад в главное меню ", callback_data=ContextData.HOME)])
        keyboard.append([InlineKeyboardButton("🔙 Назад ", callback_data=query.data)])
        query.message.reply_html(Message.HOME_MSG, reply_markup=InlineKeyboardMarkup(keyboard))
    
    def amount(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()


        
    def meal(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        query.message.delete()
        pk = int(query.data.split('/')[-1])
        basket = Basket(tg_id=query.from_user.id, product_id=pk)
        amount = basket.getOrCreateObject()['amount']
        meals_data = "menu/" + query.data.split('/')[1]
        course = get_meal(id=pk)
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("-", callback_data=f"decr/{query.data.split('/')[1]}/{pk}"),
                InlineKeyboardButton(f"{amount}", callback_data="amount"),
                InlineKeyboardButton("+", callback_data=f"incr/{query.data.split('/')[1]}/{pk}"),
            ],
            [
                InlineKeyboardButton("Savatga qo'shish", callback_data='amout')
            ],
            [
                InlineKeyboardButton("🔙 Mенуга қайтиш", callback_data='menu'),
            ],
            [
                InlineKeyboardButton("🔙 Назад", callback_data=meals_data)
            ],
            [
                InlineKeyboardButton("🔙 Бош менуга қайтиш", callback_data=ContextData.HOME),
            ]
        ])
        image = open(str(settings.MEDIA_ROOT)+f"\\{course.image}", 'rb')

        query.message.reply_photo(photo=image, caption=f"""<b>{course.name}</b>\n\n{course.description}""", parse_mode="HTML", 
            reply_markup=keyboard
        )

    def decr(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        basket = Basket(tg_id=query.from_user.id, product_id=pk)
        besket.decrement()
        self.meal(update, context)
    
    def menu(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        if query.data == ContextData.MENU:
            query.message.delete()
            menus = Menu.objects.all()
            keyboard = []
            index = 0
            for i in range(len(menus)):
                name = menus[i].name
                data = "menu/"+str(menus[i].id)
                if  i % 2 == 0 and i != 0:
                    index += 1
                if i % 2 == 0:
                    keyboard.append([InlineKeyboardButton(text=name, callback_data=data)])
                else:
                    keyboard[index].append(InlineKeyboardButton(text=name, callback_data=data))

            keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data=ContextData.HOME)])
            query.message.reply_html(Message.HOME_MSG, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            if len(query.data.split('/')) == 2:
                if query.data.split('/')[0] == 'menu':
                    self.meals(update, context)
                elif query.data.split('/')[0] == 'decr':
                    self.decr(update, context)
            else:
                self.meal(update, context)
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
                        CallbackQueryHandler(self.about , pattern=f"^({ContextData.ABOUT})$"),
                        CallbackQueryHandler(self.home, pattern=f"^({ContextData.HOME})$"),
                        CallbackQueryHandler(self.amount, pattern="^(amount)$"),
                        # CallbackQueryHandler(self.menu, pattern=f"^({ContextData.MENU})$"),
                        CallbackQueryHandler(self.menu),
                    ]
        all_handler = ConversationHandler(
            entry_points=entryPoints(),
            states={
                    1: [
                        CommandHandler('start', start),
                        MessageHandler(Filters.text, first_name),
                    ],
                    2: [
                        CommandHandler('start', start),
                        MessageHandler(Filters.text, last_name)
                    ],
                    3: [
                        CommandHandler('start', start),
                        MessageHandler(Filters.contact, phonenumber)
                    ],
                    4: entryPoints(),

            },
            fallbacks=[]
        )

        updater.dispatcher.add_handler(all_handler)
        updater.start_polling()
        updater.idle()