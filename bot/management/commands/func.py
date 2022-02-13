# start third party packages
from django.conf import settings
from telegram import InlineKeyboardButton,  InlineKeyboardMarkup, InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
from bot.helpers import Data
from django.db import transaction
# end third party packages

# start my packages
from bot.models import Meal, Menu, Order, OrderItem
from bot.management.commands.utils import Message, ButtonText, get_BotUser, get_meal, group_username, ContextData
# end my packages

def home(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.message.delete()
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(ButtonText.MENU_BUTTON_TEXT, callback_data=ContextData.MENU)
        ],
        [
            InlineKeyboardButton(ButtonText.ABOUT_BUTTON_TEXT, callback_data=ContextData.ABOUT),
            InlineKeyboardButton(ButtonText.KORZINKA_BUTTON_TEXT, callback_data=ContextData.KORZINKA)
        ],
        
    ])
    query.message.reply_text(Message.HOME_MSG, reply_markup=keyboard, parse_mode="HTML")
def about(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data=ContextData.HOME)]])
    query.edit_message_text(Message.ABOUT_MSG, reply_markup=keyboard, parse_mode="HTML")

def meals(update: Update, context: CallbackContext):
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

    keyboard.append([InlineKeyboardButton("🔙 Bosh menyuga qaytish ", callback_data=ContextData.HOME)])
    keyboard.append([InlineKeyboardButton("🔙 Orqaga ", callback_data=ContextData.MENU)])
    query.message.reply_text(Message.HOME_MSG, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

def amount(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

def addBasket(update: Update, context: CallbackContext):    
    query = update.callback_query
    query.answer(text=f'Savatga qo\'shildi ✅', show_alert=True)
    user = get_BotUser(tg_id=query.from_user.id)
    if user:
        pk=int(query.data.split('/')[-1])
        orderItem = OrderItem.objects.get_or_create(user=user, meal_id=pk)[0]
        data = Data(tg_id=query.from_user.id, product_id=pk)
        orderItem.quantitation += data.getOrCreateObject().get('data').get('amount')
        orderItem.save()
    meal(update, context)    
    
def meal(update: Update, context: CallbackContext, setOne:bool=True):
    query = update.callback_query
    query.answer()

    pk = int(query.data.split('/')[-1])
    data = Data(tg_id=query.from_user.id, product_id=pk)
    if setOne:
        data.setOne()
    amount = data.getOrCreateObject().get('data').get('amount')
    meals_data = "menu/" + query.data.split('/')[1]
    meal = get_meal(id=pk)
    addbasketdata = f"addBasket/{query.data.split('/')[1]}/{pk}"
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("-", callback_data=f"decr/{query.data.split('/')[1]}/{pk}"),
            InlineKeyboardButton(f"{amount}", callback_data="amount"),
            InlineKeyboardButton("+", callback_data=f"incr/{query.data.split('/')[1]}/{pk}"),
        ],
        [
            InlineKeyboardButton("Savatga qo'shish", callback_data=addbasketdata)
        ],
        [
            InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='menu'),
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data=meals_data)
        ],
        [
            InlineKeyboardButton("🔙 Bosh menyuga qaytish", callback_data=ContextData.HOME),
        ]
    ])
    image = open(str(settings.MEDIA_ROOT)+f"\\{meal.image}", 'rb')
    print(setOne)
    if setOne:
        query.message.delete()
        query.message.reply_photo(
            photo=image,
            caption=f"""<b>{meal.name}</b>\n\n{meal.description}\n<b>Narxi:</b>{meal.price * amount} so'm""", 
            parse_mode="HTML",
            reply_markup=keyboard
        )
    else:
        query.edit_message_media(
            media=InputMediaPhoto(
                media=image,
                caption=f"""<b>{meal.name}</b>\n\n{meal.description}\n<b>Narxi:</b>{meal.price * amount} so'm""", 
                parse_mode="HTML"
            ),
            reply_markup=keyboard
        )

def decr(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    pk = int(query.data.split('/')[-1])
    data = Data(tg_id=query.from_user.id, product_id=pk)
    data.decrement()
    meal(update, context, setOne=False)

def incr(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    pk = int(query.data.split('/')[-1])
    data = Data(tg_id=query.from_user.id, product_id=pk)
    data.increment()
    meal(update, context, setOne=False)

def menu(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == ContextData.MENU:
        query.answer()
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
        query.message.reply_text(Message.MENU_MSG, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    else:
        data = query.data.split('/')[0]
        if len(query.data.split('/')) == 2:
            if data == 'menu':
                meals(update, context)
            elif data == 'b-decr':
                b_decr(update, context)
            elif data == 'b-incr':
                b_incr(update, context)
            elif data == 'd-basket':
                b_delete(update, context)

        else:
            if data == 'decr':
                decr(update, context)
            elif data == 'incr':
                incr(update, context)
            elif data == 'addBasket':
                addBasket(update, context)
            else:
                meal(update, context)

def b_decr(update: Update, context: CallbackContext):
    print("b-decr")
    query = update.callback_query
    query.answer()
    pk = int(query.data.split('/')[-1])
    user = get_BotUser(tg_id=query.from_user.id)
    orderItem = OrderItem.objects.filter(user=user, is_ordered=False, meal_id=pk).last()
    if orderItem.quantitation > 1:
        orderItem.quantitation = orderItem.quantitation - 1
        orderItem.save()
    else:
        orderItem.delete()
    baskets(update, context)

def b_incr(update: Update, context: CallbackContext):
    print("b-incr")
    query = update.callback_query
    query.answer()
    pk = int(query.data.split('/')[-1])
    user = get_BotUser(tg_id=query.from_user.id)
    orderItem = OrderItem.objects.filter(user=user, is_ordered=False, meal_id=pk).last()
    orderItem.quantitation = orderItem.quantitation + 1
    orderItem.save()
    baskets(update, context)

def b_delete(update: Update, context: CallbackContext):
    print('b-delete')
    query = update.callback_query
    query.answer()
    pk = int(query.data.split('/')[-1])
    user = get_BotUser(tg_id=query.from_user.id)
    orderItem = OrderItem.objects.filter(user=user, is_ordered=False, meal_id=pk).last()
    orderItem.delete()
    baskets(update, context)

def baskets(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = get_BotUser(tg_id=query.from_user.id)
    orderItems = OrderItem.objects.filter(user=user, is_ordered=False)
    text = f"{Message.KORZINKA_MSG}"
    keyboard = []
    if orderItems:
        i = 0
        for orderItem in orderItems:
            i+=1
            text += f"<b>{i}. {orderItem.meal.name}</b>\n  {orderItem.quantitation} x {orderItem.meal.price} = <b>{orderItem.total_price} so'm</b>\n"
            keyboard.append([
                InlineKeyboardButton(f"❌ {orderItem.meal.name}", callback_data=f"d-basket/{orderItem.meal.id}")
            ])
            keyboard.append([
                InlineKeyboardButton('-', callback_data=f"b-decr/{orderItem.meal.id}"),
                InlineKeyboardButton(f'{orderItem.quantitation}', callback_data="basket"),
                InlineKeyboardButton('+', callback_data=f"b-incr/{orderItem.meal.id}"),
            ])
        keyboard.append([
            InlineKeyboardButton(f"Buyurtma berish", callback_data="order")
        ])
    else:
        text += "<i>Hozirda savatda hech narsa yo'q</i>"
    keyboard.append([
        InlineKeyboardButton(f"Bosh menyuga qaytish", callback_data=ContextData.HOME)
    ])
    query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

def sendLocation(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.message.reply_html(
        text="Manzilingizni yuboring",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Manzilni yuborish', request_location=True)]], resize_keyboard=True)
    )

def location(update: Update, context: CallbackContext):
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    current_pos = (message.location.latitude, message.location.longitude)
    user = get_BotUser(
        tg_id=message.from_user.id
    )
    order = Order(
        user=user,
        latitude=current_pos[0],
        longitude=current_pos[1]
    )
    order.save()
    orderItems = OrderItem.objects.filter(user=user, is_ordered=False)
    for orderItem in orderItems:
        orderItem.order = order
        orderItem.is_ordered = True
        orderItem.save()
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Bosh menyuga qaytish", callback_data=ContextData.MENU)
        ],
    ])
    update.message.reply_html("Buyurtmangiz qabul qilindi", reply_markup=keyboard)