import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Import our modular code
from indicators import compute_rsi
from strategy import rsi_mean_reversion_signals
from backtest import simple_vectorized_backtest

def main():
    # 1. Load data
    ticker = 'AAPL'
    data = yf.download(ticker, period='3y', interval='1d')  # last 3 years of daily data
    data.dropna(inplace=True)
    
    # 2. Compute RSI (14-day)
    data['rsi'] = compute_rsi(data['Adj Close'], window=14)
    
    # 3. Generate signals
    data['signal'] = rsi_mean_reversion_signals(data, rsi_col='rsi',
                                                lower_threshold=30,
                                                upper_threshold=70)
    
    # 4. Backtest
    results = simple_vectorized_backtest(data, 
                                         price_col='Adj Close',
                                         signal_col='signal',
                                         initial_capital=10000.0)
    
    # 5. Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(results['cumulative_strategy_returns'], label='RSI Strategy')
    plt.plot(results['cumulative_buy_and_hold'], label='Buy & Hold')
    plt.title(f'{ticker} RSI Mean Reversion Backtest')
    plt.legend()
    plt.show()
    
    # Print final values
    final_strategy = results['cumulative_strategy_returns'].iloc[-1]
    final_bh = results['cumulative_buy_and_hold'].iloc[-1]
    print(f"Final Strategy Value: ${final_strategy:,.2f}")
    print(f"Final Buy & Hold Value: ${final_bh:,.2f}")

if __name__ == "__main__":
    main()
