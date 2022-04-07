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
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload,MediaIoBaseUpload,MediaIoBaseDownload
from datetime import date
import io
from DBT import DBT

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

folders_id = '1l7f3uJsihn5EpVNZI5KMjuGK19Yn6y1R'

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = str(event.message.text).lower()
    db = DBT(app)
    db.create_table()
    db.deleteBLOB(1)
    status = db.insertBLOB(1,msg)   
    if status==1:
        msg = "Thanks !!! I get parameters your pic"
    else:
        msg = "Cant save parameters your pic. Try again !!"
    
    try:
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=msg))
    except Exception as e:
        app.logger.error('This is an ERROR log record.'+ str(e) )



def get_folder_name():
    today = date.today()
    folder_name = today.strftime('%d_%m_%Y')
    return folder_name

def create_folder(service,folder_id,new_folder_name):
    # создать новую папку
    file_metadata = {
        'name': new_folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    file = service.files().create(body=file_metadata,fields='id').execute()
    return file.get('id')

def get_folder_id(service,folder_id):
    query=f"parents = '{folder_id}'"
    response = service.files().list(q=query).execute()
    folder_today = get_folder_name()
    for fl in response.get('files'):
        if fl['mimeType']=='application/vnd.google-apps.folder':
            if folder_today == fl['name']:
                return fl['id']
    return create_folder(service,folder_id,folder_today)

def save_pic(service,name_file,folder_id,io_bytes):
    
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


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    img = message_content.content
    db = DBT(app)
    name_file = db.readBlobData(1)
    if name_file is not None:
        msg = "Your data is uploaded"
        tm = str(datetime.datetime.now()).replace(' ','_').replace('.','_').replace(':',';')
        v = name_file.split('##')
        name_file = '_'.join(v) + tm
        service = connect_to_google()
        new_folder_id = get_folder_id(service,folders_id)
        save_pic(service,name_file,new_folder_id,io.BytesIO(img))
    else:
        msg = "Cant upload your data"
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
            )
    except Exception as e:
        app.logger.error('This is an ERROR log record.'+ str(e) )


if __name__ == "__main__":
    app.run()

