"""
These methods dictate how data is to be processed to make a new prediction or
to be used to train new models.

It MUST take in and return a pd.DataFrame, such that THE LAST ROW is suitable
for a prediction using the model in <fill out the rest>
"""
import pandas as pd
import numpy as np

from feature_engineering import *

def BTCUSDT_1m(df_raw: pd.DataFrame):
    df = df_raw.copy()
    # @params
    up_margin = 0.008
    down_margin = 0.005
    lag_factor = 5

    # first, add the target variable according to num_classes
    add_return(df)
    add_log_return(df)

    #add_jump_categories_3(df, up_margin, down_margin)
    # do jump features manually in case we don't get unique cases in our df
    df['jump_neutral'] = ((df['return'] >= -np.abs(down_margin)) & (df['return'] <= up_margin)).astype(int)
    df['jump_up'] = (df['return'] > up_margin).astype(int)
    
    #df['next_jump'] = df['jump'].shift(-1)
    #df = pd.get_dummies(df, columns=['jump'], prefix='jump', drop_first=True)

    add_atr(df, period=12)
    add_atr(df, period=24)
    add_atr(df, period=24*5) # 120

    add_ema(df, period=5)
    add_ema(df, period=24)
    add_ema(df, period=24*5) # 120

    add_sma(df, window=5)
    add_sma(df, window=24)
    add_sma(df, window=24*5) # 120

    add_vidya(df, window=5)
    add_vidya(df, window=24)
    add_vidya(df, window=24*5) #120

    add_cmo(df, window=5)
    add_cmo(df, window=12)
    add_cmo(df, window=24)
    add_cmo(df, window=120)

    add_cmf(df, window=5)
    add_cmf(df, window=12)
    add_cmf(df, window=24)
    add_cmf(df, window=120)

    df['atr_24_atr_12'] = df['atr_24'] - df['atr_12']
    df['ema_sma_5'] = df['ema_5'] - df['sma_5']
    df['ema_sma_24'] = df['ema_24'] - df['sma_24']
    df['ema_sma_120'] = df['ema_120'] - df['sma_120']
    df['vidya_ema_5'] = df['vidya_5'] - df['ema_5']
    df['vidya_ema_24'] = df['vidya_24'] - df['ema_24']
    df['vidya_ema_120'] = df['vidya_120'] - df['ema_120']


    add_vwap(df)
    add_sma_feature(df, 'vwap', window=7)
    add_sma_feature(df, 'vwap', window=24)

    df['vwap_price'] = (df['high'] + df['low'] + df['close']) / 3 - df['vwap']
    df['return_log_return'] = df['return'] - df['log_return']


    add_sma_feature(df, 'volume', window=7)
    add_sma_feature(df, 'volume', window=24)

    add_dow(df)
    df = pd.get_dummies(df, columns=['day_of_week'], prefix='dow', drop_first=True)

    cols = [
        'open', 'high', 'low', 'close', 'volume', 'return', 'log_return', 'jump_neutral', 'jump_up',
        'atr_12', 'atr_24', 'atr_120', 'ema_5', 'ema_24', 'ema_120', 'sma_5', 'sma_24', 'sma_120', 'vwap',
        'vwap_price', 'return_log_return', 'sma_volume_7', 'sma_volume_24'
    ]

    df = df.dropna()
    for lag in range(1, lag_factor+1):
        for col in cols:
            newcol = np.zeros(df.shape[0]) * np.nan
            newcol[lag:] = df[col].values[:-lag]
            df.insert(len(df.columns), "{0}_{1}".format(col, lag), newcol)

    df = df.dropna()

    return df
