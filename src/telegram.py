"""
Telegram bot is used to send notifications about trade entry/exits
"""
import sys, os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from user_info import USER, API, TELEGRAM

TOKEN = TELEGRAM['TOKEN']
CHAT_ID = TELEGRAM['CHAT_ID']


def send_message(message: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"

    requests.get(url)

def fetch_time():
    tz = ZoneInfo(USER['TIMEZONE'])
    c = datetime.now(tz=tz)
    current_time = c.strftime('%d/%m/%Y, %H:%M:%S')

    return current_time


def send_exit_msg(symbol: str, interval: str):
    time = fetch_time()

    message = f"""
{symbol}_{interval} STREAM HAS ENDED @ {time}
"""
    send_message(message)

def send_signal_msg(symbol: str, interval: str, signal: str, price: float):
    time = fetch_time()

    message = f"""
{signal}  :  {symbol}_{interval}  @  {price} :: {time}
"""
    send_message(message)

    