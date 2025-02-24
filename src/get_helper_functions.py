import importlib
import os
import xgboost as xgb

def get_data_processor(symbol: str, interval: str):
    """
    Returns a data processor to do feature engineering on the given
    symbol and interval. Will return a data processor method to apply
    to the appended `df` if one is found.
    """
    method_name = f"{symbol}_{interval}"

    module = importlib.import_module('process_data')

    data_processor = getattr(module, method_name)

    assert data_processor, f'Could not find a data processor {method_name}'

    if not data_processor:
        raise ValueError(f'No data processor for {symbol}_{interval} could be found')
    
    return data_processor

def get_xgb_model(symbol: str, interval: str) -> xgb.XGBClassifier:
    """ 
    Returns the xgboost model in models/ if one is found.
    """
    model_name = f"{symbol}_{interval}.json"
    directory = "models/"

    filepath = os.path.join(directory, model_name)

    if not os.path.isfile(filepath):
        raise ValueError(f'Cannot find model {symbol}_{interval}.json - please check models/')
    
    model = xgb.XGBClassifier()
    model.load_model(filepath)

    return model







