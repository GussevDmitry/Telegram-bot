from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
from requests.exceptions import ConnectTimeout, ConnectionError

if __name__ == '__main__':

    bot.add_custom_filter(StateFilter(bot))
    try:
        set_default_commands(bot)
        bot.polling(non_stop=True, timeout=15)
    except ConnectTimeout:
        print("Connection to api.telegram.org timed out")
    except ConnectionError:
        print("Connection to api.telegram.org failed")

