from flask import Flask
from config_run import *
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import Dispatcher

app = Flask(__name__)
app.config.from_pyfile("config_run.py")

#bot = telegram.Bot(token = TOKEN)
updater = Updater(token=TOKEN, use_context=True)


dispatcher = updater.dispatcher

def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Я запустился")


def sniffer_group(update, context):
	global group_chat_id
	group_chat_id = update.effective_chat.id
	chat_data = update.get_chat_data()
	context.bot.send_message(group_chat_id, text=str(group_chat_id)+str(chat_data))

def stop_sniffer(update, context):
	global group_chat_id
	context.bot.send_message(group_chat_id, text = "Не слежу")
	group_chat_id = 0


start_handler = CommandHandler('start', start)  #Объединяем функцию и обработчик
dispatcher.add_handler(start_handler)  #Добавляем обработчик в диспетчер

sniffer_handler = CommandHandler('sniff', sniffer_group)
dispatcher.add_handler(sniffer_handler)

stop_sniff_handler = CommandHandler('stopsniff', stop_sniffer)
dispatcher.add_handler(stop_sniff_handler)
#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# говорим обработчику `MessageHandler`, если увидишь текстовое
# сообщение (фильтр `Filters.text`)  и это будет не команда
# (фильтр ~Filters.command), то вызови функцию `echo()`
#dispatcher.add_handler(echo_handler) #теперь бот будет слушать все сообщения чата

#updater.start_polling()  #Слушай сервера Telegram





@app.route ("/")
def hello_func():
	return str(group_chat_id)


if __name__ == "__main__":
	app.run()
