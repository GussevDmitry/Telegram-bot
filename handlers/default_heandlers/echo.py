from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(content_type=['text'])
def bot_echo(message: Message):
    bot.send_message(message.from_user.id, "[ИНФО] Для начала работы наберите команду /start. "
                                           "Для получения информации по моим командам, наберите команду /help")
