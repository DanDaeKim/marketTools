import pandas as pd
import numpy as np

def compute_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
    """
    Calculate the RSI for a given price series using a simple moving average.
    For demonstration, we won't do the Wilder's smoothing.
    
    :param prices: A pandas Series of asset prices (e.g. Adj Close).
    :param window: Lookback period for RSI calculation.
    :return: A pandas Series representing the RSI values.
    """
    # 1. Calculate daily returns (price differences)
    delta = prices.diff().fillna(0)
    
    # 2. Separate gains and losses
    gains = np.where(delta > 0, delta, 0.0)
    losses = np.where(delta < 0, -delta, 0.0)
    
    # 3. Calculate average gains and losses using simple moving average
    avg_gain = pd.Series(gains).rolling(window=window).mean()
    avg_loss = pd.Series(losses).rolling(window=window).mean()
    
    # Prevent division by zero
    avg_loss = avg_loss.replace(0, 1e-10)
    
    # 4. Compute RS
    rs = avg_gain / avg_loss
    
    # 5. Convert to RSI
    rsi = 100 - (100 / (1 + rs))
    
    # Align index with original prices
    rsi = pd.Series(rsi, index=prices.index)
    
    return rsi
    # bring back
