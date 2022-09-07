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

def create_list_day(text):
	msg_list_for_day.append(text)

'''
def get_msg_text(update):
	text = update.message.text
	return text
'''

def sniffer_group(update, context):
	'''
	Запускаем сниффер.
	'''
	global group_chat_id
	group_chat_id = update.effective_chat.id
	text = update.message.text
	for i in substring_list:
		if i in text:
			create_list_day(text)
		else:
			pass
	#context.bot.send_message(group_chat_id, text=str(group_chat_id))

def get_list_day(update, context):
	global msg_list_for_day
	chat_id = update.effective_chat.id
	context.bot.send_message(chat_id, str(msg.split('\n') for msg in msg_list_for_day))

def stop_sniffer(update, context):
	'''
	Останавливаем бота.
	'''
	global group_chat_id, msg_list_for_day
	context.bot.send_message(group_chat_id, text = "Не слежу")
	group_chat_id = 0
	msg_list_for_day.clear()



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

updater.start_polling()  #Слушай сервера Telegram





@app.route ("/")
def hello_func():
	return msg_list_for_day


if __name__ == "__main__":
	app.run()
