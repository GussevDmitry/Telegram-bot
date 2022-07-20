from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
import requests, os

if __name__ == '__main__':

    # place = input('Enter the place (in eng): ')
    # url = 'https://hotels4.p.rapidapi.com/locations/v2/search'
    # querystring = {"query": f"{place}", "locale": "en_US", "currency": "USD"}
    # headers = {
    #     "X-RapidAPI-Key": f"{os.getenv('RAPID_API_KEY')}",
    #     "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    # }
    #
    # responce = requests.request("GET", url=url, headers=headers, params=querystring)


    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.polling(non_stop=True)
