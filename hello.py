# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
# Set-ExecutionPolicy Unrestricted
# Set-ExecutionPolicy Restricted
# https://linuxtut.com/en/25db0c9c2ecd319218df/

# https://www.youtube.com/watch?v=x8hVoalU0MA
# https://www.youtube.com/watch?v=x8hVoalU0MA
# web: gunicorn hello:app --log-file -
# http://datalytics.ru/all/rabotaem-s-api-google-drive-s-pomoschyu-python/
from flask import Flask, request, abort
import json
import numpy as np
from pathlib import Path

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload,MediaIoBaseUpload,MediaIoBaseDownload
import io
from DB import DB 

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

folders_id = {'image' : '1l7f3uJsihn5EpVNZI5KMjuGK19Yn6y1R','tmp':'17Le5G-ytwdyJUFmQ193ZK_QJYHJyWakI'}

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


def connect_to_google():
    SERVICE_ACCOUNT_FILE = 'client.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build(API_NAME,API_VERSION, credentials=credentials)
    return service

def save_pic(name_file,folder_id,io_bytes):
    service = connect_to_google()

    file_types = 'image/jpeg'
    file_meta_data = {
        'name' : name_file,
        'parents': [folder_id]
    }

    media = MediaIoBaseUpload(io_bytes, mimetype=file_types, resumable=True)
    request = service.files().create(
        media_body = media,
        body = file_meta_data
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            app.logger.info("Uploaded %d%%." % int(status.progress() * 100))
    app.logger.info("Upload Complete!")


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = str(event.message.text).lower()
    val = msg.split('##')
    name_file = '_'.join(val)
    db = DB(app)
    db.create_table()
    img = db.readBlobData(1)
    if img is not None:
        save_pic(name_file,folders_id['image'],img)
        msg = "Done!! Let's do it again"
    else:
        msg = "Cant find your pic!! Try again !!!"
    df.deleteBLOB(1)
    try:
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=msg))
    except Exception as e:
        app.logger.error('This is an ERROR log record.'+ str(e) )



@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    img = message_content.content
    db = DB(app)
    db.create_table()
    id_file = db.insertBLOB(1,'tmp',img)
    text_message = 'We uploaded you pic. Send me now parameters.NameShop##Coast##TypeProduct '
    text_message += str(id_file)
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text_message)
            )
    except Exception as e:
        app.logger.error('This is an ERROR log record.'+ str(e) )


if __name__ == "__main__":
    app.run()

