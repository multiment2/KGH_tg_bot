from config_run import *
import requests
import datetime


url = 'https://api.telegram.org/bot<token>/'

def get_updates_json(request):
    response = requests.get(request + 'getUpdates')
    return response.json()

def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):
    params = {'chat_id': chat, 'text' : text}
    response = requests.post(url + 'SendMessage', data=params)
    return response

chat_id = get_chat_id(last_update(get_updates_json(url)))

send_mess(chat_id, 'Ваше сообщение доставлено сюда')

'''
Вариант с классом.
'''
class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}'.format(token)

    def get_updates(self, timeout=30):
        method = 'getUpdates'
        params = {'timeout':timeout}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id':chat_id, 'text':text}
        method = 'SendMessage'
        resp = requests.get(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result)>0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
        
        return last_update