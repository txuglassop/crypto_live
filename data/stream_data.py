import websocket
import datetime

def on_message(ws, message):
    print()
    print(str(datetime.datetime.now()) + ": ")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print("### closed ###" + close_msg)

def streamKline(currency, interval):
    socket = f'wss://stream.binance.com:9443/ws/{currency}@kline_{interval}'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

streamKline('btcusdt', '15m')


# wss://stream.binance.com:9443/ws/<symbol>@kline_<interval>

# payload format:
#  
#  {
#   "e": "kline",         // Event type
#   "E": 1672515782136,   // Event time
#   "s": "BNBBTC",        // Symbol
#   "k": {
#     "t": 1672515780000, // Kline start time
#     "T": 1672515839999, // Kline close time
#     "s": "BNBBTC",      // Symbol
#     "i": "1m",          // Interval
#     "f": 100,           // First trade ID
#     "L": 200,           // Last trade ID
#     "o": "0.0010",      // Open price
#     "c": "0.0020",      // Close price
#     "h": "0.0025",      // High price
#     "l": "0.0015",      // Low price
#     "v": "1000",        // Base asset volume
#     "n": 100,           // Number of trades
#     "x": false,         // Is this kline closed?
#     "q": "1.0000",      // Quote asset volume
#     "V": "500",         // Taker buy base asset volume
#     "Q": "0.500",       // Taker buy quote asset volume
#     "B": "123456"       // Ignore
#   }
# }