from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
from requests.exceptions import ConnectTimeout, ConnectionError
from loguru import logger


def main() -> None:
    """
    Telegram bot starts polling.
    Custom filters are added.
    Handling exceptions on max level
    """
    bot.add_custom_filter(StateFilter(bot))
    try:
        set_default_commands(bot)
        bot.polling(non_stop=True, timeout=15)
    except ConnectTimeout:
        print("Connection to api.telegram.org timed out")
    except ConnectionError:
        print("Connection to api.telegram.org failed")


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print("Something went wrong...")
        logger.add("logging/error.log",
                   format="{time:YYYY-MM-DD at HH:mm:ss} - {level} - {name} - {message}",
                   level="ERROR")
        logger.exception("Uncontrolled exception occured...")
