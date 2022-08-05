from flask import Flask
import config_run
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

app = Flask(__name__)
app.config.from_pyfile("config_run.py")

#bot = telegram.Bot(token = TOKEN)
updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

start_handler = CommendHandler('start', start)  #Объединяем функцию и обработчик
dispatcher.add(start_handler)  #Добавляем обработчик в диспетчер

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# говорим обработчику `MessageHandler`, если увидишь текстовое 
# сообщение (фильтр `Filters.text`)  и это будет не команда 
# (фильтр ~Filters.command), то вызови функцию `echo()`
dispatcher.add(echo_handler) #теперь бот будет слушать все сообщения чата

updater.pulling()  #Слушай сервера Telegram

def start(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="LALALALa") 
  # `bot.send_message` это метод Telegram API
    # `update.effective_chat.id` - определяем `id` чата, 
    # откуда прилетело сообщение 

def echo(update, context):
  pass

@app.route ("/")
def hello_func():
  return "Hello gay"


if __name__ == "__main__":
  app.run()
