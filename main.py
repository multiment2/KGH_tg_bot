from flask import Flask
from config_run import *
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import Dispatcher, ConversationHandler

app = Flask(__name__)
app.config.from_pyfile("config_run.py")

#bot = telegram.Bot(token = TOKEN)
updater = Updater(token=TOKEN, use_context=True)


dispatcher = updater.dispatcher


def create_list_day(name,text): #Заполняем словарь (ключ - имя пользователя, значение - тест сообщения) на отправку
	global msg_list_for_day
	msg_list_for_day.setdefault(name, []).append(text) #Если ключа нет, то создаем новый ключ со значением путого списка
		
	print(msg_list_for_day)


def get_msg(update, context):
	''' 
	Проверяем наличие заданных слов по списку. Если есть - добаляем в список на отсылку.
	'''
	global substring_list
	text = update.message.text
	name = update.message.from_user.username
	for i in substring_list:
		if i in text:
			create_list_day(name,text)
		

def sniffer_start(update, context):
	'''
	Запускаем сниффер.
	'''
	global group_chat_id
	group_chat_id = update.effective_chat.id
	context.bot.send_message(group_chat_id, text=str(group_chat_id))
	#MessageHandler(Filters.text & (~Filters.command), get_msg)
	return SNIFF


def get_list_day(update, context):
	global msg_list_for_day
	chat_id = update.effective_chat.id

	for name in msg_list_for_day:
		context.bot.send_message(chat_id, str(msg_list_for_day)) #Список преобразовать в JSON


def stop_sniffer(update, context):
	'''
	Останавливаем бота.
	'''
	global group_chat_id
	global msg_list_for_day
	context.bot.send_message(group_chat_id, text = "Не слежу")
	group_chat_id = 0
	msg_list_for_day.clear()
	return ConversationHandler.END


conv_handler = ConversationHandler(entry_points=[CommandHandler('sniff', sniffer_start)],
									states = {
										SNIFF: [MessageHandler(Filters.text & (~Filters.command), get_msg)],
									},
									fallbacks = [CommandHandler('stopsniff', stop_sniffer)])

get_list_handler = CommandHandler("get_list", get_list_day)
dispatcher.add_handler(get_list_handler)

dispatcher.add_handler(conv_handler)

#stop_sniff_handler = CommandHandler('stopsniff', stop_sniffer)
#dispatcher.add_handler(stop_sniff_handler)
#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# говорим обработчику `MessageHandler`, если увидишь текстовое
# сообщение (фильтр `Filters.text`)  и это будет не команда
# (фильтр ~Filters.command), то вызови функцию `echo()`
#dispatcher.add_handler(echo_handler) #теперь бот будет слушать все сообщения чата

updater.start_polling()  #Слушай сервера Telegram





@app.route ("/")
def hello_func():
	return str(msg_list_for_day)


if __name__ == "__main__":
	app.run()
