# -*- coding: utf-8 -*-
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
import os
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import time
import random

#Retrieving API tokens
PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ['TOKEN']
NEWS_TOKEN = os.environ['NEWS_TOKEN']
CMC_TOKEN = os.environ['CMC_TOKEN']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    #Send a message when the command /start is invoked.
    context.bot.sendMessage(update.message.chat_id, 'Hi! I am Đoge\n(ᵔᴥᵔ)つ' )
    context.bot.sendMessage(update.message.chat_id, 'Use /help to find out what I can do')

def help(update, context):
    #List all the commands when /help is invoked.
    context.bot.sendMessage(update.message.chat_id, "/price - Get the latest coin price. ex: /price doge\n/stats - Get the latest coin stats. ex: /stats doge\n/news - Get the latest news. Optionally specify coin /news btc")

def price(update, context):
    #Return the latest crypto prices when /price is invoked
    mes = update.message.text.split(" ")
    if len(mes)==1:
        context.bot.sendMessage(chat_id = update.message.chat_id, text = "You need to specify the coin too.\nex: /price doge")
        return True
    test = requests.get("https://api.binance.com/api/v3/ticker/price?symbol={}USDT".format(mes[1].upper()))
    dump = json.loads(test.content)
    d = float(dump['price'].strip("0"))
    message = "1 {} = {}$ ({} AED)".format(mes[1].upper(), '{:,}'.format(d),'{:,}'.format(d*3.65,2))
    context.bot.sendMessage(chat_id = update.message.chat_id, text = message, parse_mode=telegram.ParseMode.HTML)

def news(update, context):
    #Returns the latest news when /news is invoked.
    url = "https://cryptopanic.com/api/v1/posts/?auth_token="+NEWS_TOKEN+"&kind=news"
    mes = update.message.text.split(" ")
    if len(mes) == 1:
        message = "<b>Trending News</b>\n\n"
    elif len(mes) == 2:
        url+= "&filter=rising&currencies=" + mes[1]
        message = "<b>Trending " + mes[1].upper() + " News</b>\n\n"
    elif len(mes) == 3:
        url+= "&currencies=" + mes[1]
        url+= "&filter=" + mes[2]
        message = "<b>" + mes[2].title() + " " + mes[1].upper() + " News</b>\n\n"
    test = requests.get(url)
    dump = json.loads(test.content)
    c=0
    if dump['results']!=[]:
        for i in dump['results']:
            if c>5:
                break
            c+=1
            message+=str(c)+". "+i['title']+"\n"
    else:
        message+="such empty, much wow\n             (＾ᴥ＾)"
    context.bot.sendMessage(chat_id = update.message.chat_id, text = message, parse_mode=telegram.ParseMode.HTML)

def stats(update, context):
    #Returns the latest stats when /stats is invoked.
    mes = update.message.text.split(" ")
    if len(mes)==1:
        context.bot.sendMessage(chat_id = update.message.chat_id, text = "You need to specify the coin too.\nex: /stats doge")
        return True
    ticker = mes[1].upper()
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
      'symbol':ticker
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': CMC_TOKEN,
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      dump = json.loads(response.text)

      data = dump['data'][ticker][0]['quote']['USD']
      slug = dump['data'][ticker][0]['slug'].title()
      rank = dump['data'][ticker][0]['cmc_rank']
      max_supply = dump['data'][ticker][0]['max_supply']
      circulating_supply = dump['data'][ticker][0]['circulating_supply']
      message = "<b>{} ({}) Latest Stats</b>\n<i>Rank: {}</i>\n\n<pre>".format(slug, ticker, str(rank))
      for i in data:
          perc = "$"
          if "percent" in i:
              perc = "%"
          try:
              num = float(data[i])
              message+="{:<11}\t{}\n".format(i.replace("percent_","%").replace("_"," ").title(),'{:,}{}'.format(round(num,2),perc))
          except ValueError:
              pass
      message+="\nSupply:"
      if max_supply is not None:
          message+="\n{:<11}\t{}".format("Max",'{:,} {}'.format(round(max_supply,2),ticker))
      message+="\n{:<5}\t{}".format("Circulating",'{:,} {}'.format(round(circulating_supply,2),ticker))
      message+="</pre>"
      context.bot.sendMessage(chat_id = update.message.chat_id, text = message, parse_mode=telegram.ParseMode.HTML)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Error "%s"', context.error)


def main():
    updater = Updater(TOKEN, use_context=True)


    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("news", news))

  
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('https://dogecoinbot.herokuapp.com/' + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
