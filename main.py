import requests
import time

from config import BOT_TOKEN, CHANNEL_ID
from handlers.comands import process_updates


POLL_INTERVAL = 1
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"


def main():
    offset = 0
    while True:
        try:
            offset = process_updates(offset)
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
