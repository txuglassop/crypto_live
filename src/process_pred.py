import pandas as pd

from telegram import send_signal_msg
from frontend import update

def log_pred(symbol, interval, pred:int, kline):
    csv = symbol + '_' + interval + '.csv'
    path = './logs/' + csv
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['time','open','high','low','close','change', 'pred'])

    new_obs = pd.DataFrame([{
        'time':int(kline['t']),
        'open': float(kline['o']),
        'high':float(kline['h']),
        'low':float(kline['l']),
        'close':float(kline['c']),
        'change': float(kline['c']) / float(kline['o']) - 1,
        'pred':pred
    }])

    df = pd.concat([df, new_obs], ignore_index=True)
    df.to_csv(path, index=False)


def process_pred(symbol, interval, pred: int, kline):
    signal = ''
    if pred == 0:
        # predicted down, so sell
        signal = 'SELL'
    elif pred == 2:
        signal = 'BUY'

    if signal:
        send_signal_msg(symbol, interval, signal, kline['o'])

    log_pred(symbol, interval, pred, kline)
    update(symbol, interval, pred)

