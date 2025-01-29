import os
import requests
import time

from config import BOT_TOKEN, ADMIN_CHAT_ID, CHANNEL_ID
from services.process_path import process_path


def send_telegram_message(text, chat_id=ADMIN_CHAT_ID):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    return response


def send_reply_channel_message(document_path, reply_to_message_id, chat_id=CHANNEL_ID):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    file_name = os.path.basename(document_path)
    with open(document_path, "rb") as file:
        files = {"document": (file_name, file)}
        data = {"chat_id": chat_id, "reply_to_message_id": reply_to_message_id}
        response = requests.post(url, files=files, data=data)

    return response


def send_telegram_photo(photo, chat_id=CHANNEL_ID):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {"chat_id": chat_id}
    files = {"photo": photo}
    response = requests.post(url, data=data, files=files)
    return response.json()["result"]["message_id"]


def process_updates(offset):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 2, "offset": offset}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        for update in data.get("result", []):
            if "message" in update and "text" in update["message"]:
                message = update["message"]
                text = message["text"].strip()
                chat_id = message["chat"]["id"]
                update_id = update["update_id"]
                print(text)
                if text.startswith("/start"):
                    send_telegram_message(
                        chat_id=chat_id, text="Send me a path to books!"
                    )
                else:
                    process_path(text)
                return update_id + 1

        return offset
    return offset
