import importlib

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