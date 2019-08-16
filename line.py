#LINE聊天機器人
#flask架設伺服器或網站
#flask架設規模較小，django規模較大
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('FNsM9L8athPD76AwtTprDyKAbyxA8jL2FbZyIzdjIkNPluoZKXoYq18few+jj0ylVDEMX9tYNhVuPYoQd1bWcq60oXk5uH7BjQU/rcGMBS53p5vNvRGYPctwWQDJ0vtVhPsvK2Wa5XS2Y9bOuWi0EQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e1b38a26e2d3a9e038b0d8c87cde296c')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()