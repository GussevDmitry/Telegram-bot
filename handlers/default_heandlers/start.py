from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Greeting the user
    :param message: message from user (help start command)
    """
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.full_name}!")
