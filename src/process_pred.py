from telegram import send_signal_msg



### have to redo this to allow different signal process methods

def process_pred(symbol, interval, pred: int, price: float):
    signal = ''
    if pred == 0:
        # predicted down, so sell
        signal = 'SELL'
    elif pred == 2:
        signal = 'BUY'

    if signal:
        send_signal_msg(symbol, interval, signal, price)


