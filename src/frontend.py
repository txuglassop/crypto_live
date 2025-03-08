"""
frontend? did you mean terminal?
"""
import os
import sys
from datetime import datetime


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def start(symbol:str, interval: str):
    os.system('clear')

    t = datetime.now()
    time = t.strftime("%d/%m/%Y, %H:%M:%S")

    print(f'PAIR: {symbol}_{interval}') 
    print(f'Last updated: {time}')
    print(f'Latest prediction: NA')

def update(symbol:str, interval:str, pred:int):
    os.system('clear')

    t = datetime.now()
    time = t.strftime("%d/%m/%Y, %H:%M:%S")

    print(f'PAIR: {symbol}_{interval}') 
    print(f'Last updated: {time}')
    print(f'Latest prediction: {pred}')
