import pandas as pd

def rsi_mean_reversion_signals(data: pd.DataFrame,
                               rsi_col: str = 'rsi',
                               lower_threshold: float = 30.0,
                               upper_threshold: float = 70.0) -> pd.Series:
    """
    Generate trading signals based on RSI mean reversion logic.
    Signal convention:
      - 1 = go long
      - 0 = hold (or flat, if not in position)
     (This version doesn't implement short selling for simplicity.)
    
    :param data: DataFrame containing at least one column: data[rsi_col].
    :param rsi_col: The column name where RSI is stored.
    :param lower_threshold: RSI below which we buy.
    :param upper_threshold: RSI above which we exit any long.
    :return: A pandas Series with the signal (1=long, 0=flat).
    """
    signals = pd.Series(0, index=data.index)
    
    # If RSI < 30 => set signal = 1
    buy_condition = data[rsi_col] < lower_threshold
    signals[buy_condition] = 1
    
    # If RSI > 70 => set signal = 0 (force exit)
    # We'll interpret that as "no position." 
    # Since by default signals = 0, we only need to ensure we clear any prior buy signal
    # on rows where RSI > 70.
    sell_condition = data[rsi_col] > upper_threshold
    signals[sell_condition] = 0
    
    return signals
