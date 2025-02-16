"""
Telegram bot is used to send notifications about trade entry/exits
"""
import sys, os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from user_info import USER, API, TELEGRAM

TOKEN = TELEGRAM['TOKEN']
CHAT_ID = TELEGRAM['CHAT_ID']

import requests

message = 'hello world'
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"

requests.get(url)