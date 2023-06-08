import telebot
import fdb
import random
from telebot import types
from twilio.rest import Client
from bill import pdf

bot = telebot.TeleBot('6284931281:AAHyTEJZmU8guV0FD8OmOGld80x_-cNJEDw')
con = fdb.connect(dsn='database/THEDATA.GDB', user='SYSDBA', password='masterkey')
cur = con.cursor()
bot.set_webhook()
@bot.message_handler(commands=['start', 'nummer'])

def start(message):
    congratulations = f'Вітаю, {message.from_user.first_name}!\nЯ, Ваш автоматичний консультант КП «Міськводоканал» Мукачівської міської ради, \nспробую допомогти отримати всю необхідну інформацію.'
    bot.send_message(message.chat.id, congratulations, parse_mode='html')
    res = cur.execute("select 1 from bot where user_id = ?", [message.from_user.id]).fetchone()
    if res is not None:
        select_action(message)
    else:
        get_edrpou(message)


def get_edrpou(message):
    edrpou_mess = f'<b>Введіть код ЄДРПОУ вашої організації:</b>'
    edrpou_from_user = bot.send_message(message.chat.id, edrpou_mess, parse_mode='html')
    bot.register_next_step_handler(edrpou_from_user, chek_edrpou)

def chek_edrpou(message):

    edrpou_to_save = message.text
    global id
    result = cur.execute("select id from account where edrpou = ?", [edrpou_to_save]).fetchone()
    if result is not None:
        id = result[0]
    res = cur.execute("select 1 from ACCOUNT where edrpou = ?", [edrpou_to_save]).fetchone()
    if res:
        contact(message)
    else:
        bot.send_message(message.chat.id, "Такого коду ЄДРПОУ немає. Спробуйте ще раз.", parse_mode='html')
        get_edrpou(message)

def contact(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    send_number_button = types.KeyboardButton("📞 Надіслати номер телефону", request_contact=True)
    markup.add(send_number_button)
    bot.send_message(message.chat.id, 'Для подальшої роботи мені необхідно знати Ваш номер телефону. Будь ласка, натисніть кнопку "📞 Надіслати номер телефону". ',reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    number = message.contact.phone_number
    send_pass(message, number)
    cur.execute('UPDATE account SET phonenumber = ? WHERE ID = ?', [number, id])
    con.commit()

def send_pass(message, number):
    recevier = number
    account_sid = "ACbf654c21b83e827ddb7702b9787af07d"
    auth_token = "f48cb31a8023a11a5a91820c02bf54e7"
    client = Client(account_sid, auth_token)
    random_password = str(random.randint(100000, 999999))
    send_password = bot.send_message(message.chat.id, "На ваш номер телефону " + recevier + " надіслано одноразовий пароль. Введіть його тут щоб я зміг перевірити.")
    bot.send_message(message.chat.id, random_password)
    #password_message = client.messages.create(
    #    body=f"Ваш одноразовий пароль для входу: {random_password}",
    #    from_="+13158182333",
    #    to=recevier
    #)
    bot.register_next_step_handler(send_password, chek_pass, random_password, recevier)

def chek_pass(message, random_password, number):
    pass_from_user = message.text
    random_password = random_password
    if pass_from_user == random_password:
        insert_into_bot(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        send_pass_button = types.KeyboardButton(text="Надіслати код повторно")
        markup.add(send_pass_button)
        send_new = bot.send_message(message.chat.id, "Паролі не співпали. Бажаєте щоб я надіслав код повторно?", reply_markup=markup)
        bot.register_next_step_handler(send_new, send_pass_again, number)

@bot.message_handler(commands=['send'])
def send_pass_again(message, number):
    if message.text == "Надіслати код повторно":
        send_pass(message, number)
def insert_into_bot(message):

    res1 = cur.execute('SELECT MAX(id) FROM BOT').fetchone()
    if res1 is not None and res1[0] is not None:
        counter_id = res1[0]+1
    else:
        counter_id = "1"
    cur.execute('INSERT INTO BOT (ID, USER_ID, ACC_ID) VALUES (?, ?, ?)',
                [int(counter_id), str(message.from_user.id), int(id)])
    con.commit()
    select_action(message)
def select_action(message):
    if message.text == "📝 Внести нові показання":
        bot.send_message(message.chat.id, id)
        res = cur.execute("select meter_end from meters where account_id = ?", [id]).fetchone()
        if res is not None:
            meters = res[0]
            bot.send_message(message.chat.id, meters)
            msg_text = "Останні фактичні показання лічильника:" + str(meters) + " Введіть нові показання лічильника (тільки цілу частину числа)"
        lll = bot.send_message(message.chat.id, msg_text)
        bot.register_next_step_handler(lll, insert_meter)
    elif message.text == "✅Отримати акт виконаних робіт":
        act(message)
    elif message.text == "💰Отримати рахунок для оплати":
        bill(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        meter_btn = types.KeyboardButton("📝 Внести нові показання")
        akt_btn = types.KeyboardButton("✅Отримати акт виконаних робіт")
        bill_btn = types.KeyboardButton("💰Отримати рахунок для оплати")
        markup.row(meter_btn)
        markup.row(akt_btn, bill_btn)
        bot.send_message(message.chat.id, "Будь ласка, оберіть чим я можу Вам допомогти!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    select_action(message)
def insert_meter(message):
    meter_reading = int(message.text)
    bot.send_message(message.chat.id, meter_reading)
    cur.execute('UPDATE METERS SET METER_END = ? WHERE ACCOUNT_ID = ?', [meter_reading, id])
    con.commit()
    bot.send_message(message.chat.id, "Показник успішно передано")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    select_action(message)
def bill(message):
    acc_id
    pdf.table()
    bill_doc = open('РАХУНОК.pdf', 'rb')
    bot.send_document(message.chat.id, bill_doc)
    bot.send_message(message.chat.id, "Ваш рахунок для оплати")

def act(message):
    pdf.table()
    act_doc = open('АКТ.pdf', 'rb')
    bot.send_document(message.chat.id, act_doc)
    bot.send_message(message.chat.id, "Ваш акт виконаних робіт")

bot.delete_webhook(drop_pending_updates=True)
bot.polling(none_stop=True)