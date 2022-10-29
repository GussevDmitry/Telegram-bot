from telebot.types import Message
from loader import bot


@bot.message_handler()
def bot_echo(message: Message) -> None:
    """
    Echo handler. Answers if command or state is not mentioned in project
    :param message: message from user
    """
    bot.send_message(message.from_user.id, "Прежде чем приступить к поиску необходимо авторизоваться. "
                                           "Наберите команду /survey. Для получения информации по моим командам, "
                                           "наберите команду /help.")
