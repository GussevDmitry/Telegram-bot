from telebot.types import Message
from loader import bot


@bot.message_handler()
def bot_echo(message: Message) -> None:
    bot.send_message(message.from_user.id, "Прежде чем приступить к поиску необходимо авторизоваться. "
                                           "Наберите команду /survey. Для получения информации по моим командам, "
                                           "наберите команду /help.")
