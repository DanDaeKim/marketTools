import pandas as pd

def simple_vectorized_backtest(data: pd.DataFrame,
                               price_col: str = 'Adj Close',
                               signal_col: str = 'signal',
                               initial_capital: float = 10000.0) -> pd.DataFrame:
    """
    A simple vectorized backtester that calculates returns based on daily signals.
    
    :param data: DataFrame with at least [price_col, signal_col]. The 'signal' column 
                 indicates the position (0 or 1) for each day.
    :param price_col: The column name for the asset's price (used to compute daily returns).
    :param signal_col: The column name that holds the signal (0 or 1).
    :param initial_capital: Starting capital for the strategy.
    :return: A DataFrame with additional columns:
             - 'daily_returns'
             - 'strategy_returns'
             - 'cumulative_strategy_returns'
             - 'cumulative_buy_and_hold'
    """
    df = data.copy()
    
    # 1. Compute daily returns
    df['daily_returns'] = df[price_col].pct_change().fillna(0)
    
    # 2. Shift the signal so that today's returns are captured by yesterday's signal
    #    (i.e., you get the signal at the close, then apply it on the next day).
    df['position'] = df[signal_col].shift(1).fillna(0)
    
    # 3. Strategy returns = daily_returns * position
    df['strategy_returns'] = df['daily_returns'] * df['position']
    
    # 4. Calculate cumulative returns
    df['cumulative_strategy_returns'] = (1 + df['strategy_returns']).cumprod() * initial_capital
    df['cumulative_buy_and_hold'] = (1 + df['daily_returns']).cumprod() * initial_capital
    
    return df
