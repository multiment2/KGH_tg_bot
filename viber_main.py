from flask import Flask, request, Response
from config_run import *

import viberbot
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
import logging

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

app = Flask(__name__)
app.config.from_pyfile('config_run.py')

viber = Api(BotConfiguration(
    auth_token = VIBER_TOKEN,
    name = bot_viber_user_name,
    avatar = '371524012.jpg'
))

viber.set_webhook('https://multiment.pythonanywhere.com/')

@app.route("/", methods = ['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        viber.send_messages(viber_request.sender.id, [message])

    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.sender.id, [
            TextMessage(text='Спасибо что с нами!')
        ])

    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


#if __name__ == "__main__":
#    app.run()

