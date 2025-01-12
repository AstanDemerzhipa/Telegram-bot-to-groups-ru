import telebot # библиотека telebot
from config import token # импорт токена

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(func=lambda message: True)
def handler_message(message):
    if "https://" in message.text:  
        chat_id = message.chat.id  # ID чата
        user_id = message.from_user.id  
        
        # Получаем статус пользователя
        user_status = bot.get_chat_member(chat_id, user_id).status
        
        
        if user_status not in ['administrator', 'creator']:
            bot.ban_chat_member(chat_id, user_id)  # Бан пользователя
            username = message.from_user.username or "неизвестный пользователь"  # Защита от отсутствия username
            bot.reply_to(message, f"Пользователь @{username} нарушил правила группы и был забанен.")
        else:
            bot.reply_to(message, "Ссылки отправил администратор. Бан не применён.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'Я принял нового пользователя!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

bot.infinity_polling()
   
