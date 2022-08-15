from flask import Flask, request, Response
from config_run import *

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

app = Flask(__name__)
viber = Api(BotConfiguration(auth_token=VIBER_TOKEN, name=bot_user_name, avatar='371524012.jpg'))

viber.set_webhook('')

@app.route("/", methods = ['POST'])
def incoming():
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Veber-Content-Signature')):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        viber.send_messages(viber_request.sender.id, [message])

    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [TextMessage(text = "Спасибо")])

    return Response(status=200)

if __name__ == "__main__":
    app.run()


