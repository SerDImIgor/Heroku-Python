# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
# Set-ExecutionPolicy Unrestricted
# Set-ExecutionPolicy Restricted
# https://linuxtut.com/en/25db0c9c2ecd319218df/

# https://www.youtube.com/watch?v=x8hVoalU0MA
# https://www.youtube.com/watch?v=x8hVoalU0MA
# web: gunicorn hello:app --log-file -
from flask import Flask, request, abort
import json
import requests


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,ImageMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Oqqf+97b4kHAW8NDNjZmtMmbJBIJ3ZRfC5JuLKyMVyd7Hjp1HB2qE0KJ+6fjP+I1mFMxSf3OqgqQ/zReW0fHio/AoCCa8El5BOS20bfZHlsvwJxaYuZxYc9pS1LnJL7OAut3Vh88zbQcmMMHhiO0qAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a8707fa6a9223d88af1fc2f076e75169')


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
    msg = str(event.message.text).lower()
    dic={
        'cat':{'preview':'https://i.ibb.co/Hqnjqpc/cat.jpg','original':'https://i.ibb.co/ZxW0x1Q/cat.jpg' }, 
        'dog':{'preview':'https://i.ibb.co/PMsNChL/dog.jpg','original':'https://i.ibb.co/KDcXyqP/dog.jpg' },
        'hipo':{'preview':'https://i.ibb.co/BVZWpj5/hipo.jpg','original':'https://i.ibb.co/DDCcJkH/hipo.jpg' },
        'mhady':{'preview':'https://i.ibb.co/y8MFDHj/mhady.jpg','original':'https://i.ibb.co/LCqdMV7/mhady.jpg' }, 
        'sebuc':{'preview':'https://i.ibb.co/g7Rfsgh/sebuc.jpg','original':'https://i.ibb.co/1nmPH2j/sebuc.jpg'},
        }
    label='cat'
    if msg=='cat':
        label = 'cat'
    elif msg=='dog':
        label='dog'
    elif msg=='hipo':
        label='hipo'
    elif msg=='mhady':
        label='mhady'
    elif msg=='sebuc':
        label='sebuc'
    record = dic[label]
    try:
        line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url = record['original'],
            preview_image_url = record['preview'])
            )
    except Exception as e:
        app.logger.error('This is an ERROR log record.'+ str(e) )


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    img = event.message.content
    headers = {"Authorization": "Bearer ya29.A0ARrdaM9LozIotoVF_XnMTZda0ZatDeZS7uCaDVGVXdK2CZpSstK6MbZl6-ZQ8j1CqJgqORtEqt0PvMyZt3lWucW4XTi9J5Q9b5BjzoMtoufWHiaeMpe4Wpk1XFN1Z26JYCbmHmoaZqrl6dWc7SdqUo1Jfcfe"}
    para = {
        "name": "simple_1.jpg",
        "parents": ["1pwPcAW-6coZYxP2BJ8pkwcPpy2hv50aJ"]
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': img
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )



if __name__ == "__main__":
    app.run()

