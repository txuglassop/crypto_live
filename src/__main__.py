import pandas as pd
import time
import asyncio
import websockets
import json
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from datetime import datetime
from zoneinfo import ZoneInfo
from binance.client import Client

from user_info import API, USER
from check_data import check_data
from get_helper_functions import get_data_processor

from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# get corresponding milliseconds and Client attribute
lookup = {
    '1m': [1_000_000, Client.KLINE_INTERVAL_1MINUTE], # request wont go thru if too small of interval
    '3m': [5_000_000, Client.KLINE_INTERVAL_3MINUTE],
    '15m': [900_000, Client.KLINE_INTERVAL_15MINUTE],
    '30m': [1_800_000, Client.KLINE_INTERVAL_30MINUTE],
    "1h": [3_600_000, Client.KLINE_INTERVAL_1HOUR]
}

def append_data(df: pd.DataFrame, kline: dict):
    new_row = pd.DataFrame([{
        'timestamp': kline['t'],
        'open':kline['o'],
        'high':kline['h'],
        'low':kline['l'],
        'close':kline['c'],
        'volume':kline['v'],
        'base_asset_volume':kline['q'],
        'no_trades':kline['n'],
        'taker_buy_vol':kline['V'],
        'taker_buy_base_asset_vol':kline['Q']
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df = df.apply(lambda col: col.astype(float) if col.dtype == 'object' else col)

    print(df.tail())

    return df

async def stream_data(symbol: str, interval: str, df: pd.DataFrame):
    symbol_ws = symbol.lower()
    url = f"wss://stream.binance.com:9443/ws/{symbol_ws}@kline_{interval}" 

    data_processor = get_data_processor(symbol, interval)

    async with websockets.connect(url) as sock:
        while True:
            resp = await sock.recv()
            data = json.loads(resp)

            if "k" in data:
                kline = data["k"]
                is_closed = kline["x"] 

                if is_closed:
                    print(kline)
                    df = append_data(df, kline)

                    # process data (do any feature engineering)
                    df_final = data_processor(df)

                    print(df_final.tail())

                    # make a prediction

                    # process prediction


def main(symbol, interval):
    print('\n>> ENSURE AMPLE TIME BEFORE STARTING <<\n')
    ms, client_interval = lookup[interval]

    # scrape the last buffer something entries for feature engineering
    # have a healthy buffer, with a fair bit more than what you need
    # as Binance API doesn't like to go back far enough...
    buffer = 200
    client = Client(API['API_KEY'], API['API_SECRET']) 


    end_time = time.time() * 1000
    start_time = end_time - buffer * ms
    start_time = datetime.fromtimestamp(start_time / 1000)
    end_time = datetime.fromtimestamp(end_time / 1000)

    klines = client.get_historical_klines(symbol=symbol, interval=client_interval, start_str=str(start_time), end_str=str(end_time))

    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'Close Time', 'base_asset_volume', 'no_trades', 'taker_buy_vol', 'taker_buy_base_asset_vol', 'Ignore'])
    df.drop(['Close Time', 'Ignore'], axis=1, inplace=True)
    # ensure all float columns are of type float64
    df = df.apply(lambda col: col.astype(float) if col.dtype == 'object' else col)
    df = df.iloc[-buffer:]

    check_data(df)

    cont = str(input('\nContinue? (Press enter)'))

    # drop the last row since this candle is not closed yet
    df = df.iloc[:-1]

    print(df.tail())

    asyncio.run(stream_data(symbol, interval, df))



    

if __name__ == '__main__':
    symbol, interval = sys.argv[1], sys.argv[2]
    symbol = symbol.upper()
    if interval not in lookup.keys():
        raise ValueError(f'Unknown interval {interval}')
    main(symbol, interval)




