import asyncio
import websockets
import json

async def candle_stick_data(symbol: str, interval: str):
    symbol = symbol.lower()
    url = f"wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}" 

    async with websockets.connect(url) as sock:
        while True:
            resp = await sock.recv()
            data = json.loads(resp)

            if "k" in data:
                kline = data["k"]
                is_closed = kline["x"] 

                if is_closed:
                    print(type(kline))
                    print(kline)


asyncio.run(candle_stick_data('btcusdt', '1m'))

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