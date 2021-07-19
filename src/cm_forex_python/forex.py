import pandas as pd
import numpy as np

def calculate_top_shadow(df, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
    return df.apply(lambda x : (x[high_col] - x[open_col]) if (x[open_col] > x[close_col]) else (x[high_col] - x[close_col]), axis = 1)

def calculate_bottom_shadow(df, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
    return df.apply(lambda x : (x[close_col] - x[low_col]) if (x[open_col] > x[close_col]) else (x[open_col] - x[low_col]), axis = 1)

def calculate_body(df, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
    return df.apply(lambda x : (x[open_col] - x[close_col]) if (x[open_col] > x[close_col]) else (x[close_col] - x[open_col]), axis = 1)

def calculate_direction(df, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
    return df.apply(lambda x : -1 if (x[open_col] > x[close_col]) else (1 if(x[open_col] < x[close_col]) else 0), axis = 1)

def calculate_max_increment(df, step, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
  max_increment = abs(df.shift(step)[open_col] - df.rolling(step)[high_col].max())
  max_increment = max_increment.shift(step * -1)
  return max_increment

def calculate_max_decrement(df, step, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
  max_increment = abs(df.shift(step)[open_col] - df.rolling(step)[low_col].min())
  max_increment = max_increment.shift(step * -1)
  return max_increment


def check_for_order(df, step, take_profit_pips, stop_loss_pips, pip_size=0.0001, open_col='open', close_col='close',
                    low_col='low', high_col='high'):
    orders = []
    df_size = len(df.index)

    for i in range(0, df_size):
        order = 0
        current_row = df.iloc[i]
        close = current_row[close_col]

        check_rows = df.iloc[min(i + 1, df_size):min(i + step, df_size)]
        reached_sl_long = False
        reached_sl_short = False
        for check_row_index in range(0, len(check_rows.index)):
            check_row = check_rows.iloc[check_row_index]
            check_row_high_pips = (check_row[high_col] - close) / pip_size
            check_row_low_pips = (close - check_row[low_col]) / pip_size

            if (check_row_high_pips >= stop_loss_pips):
                reached_sl_short = True
            if (check_row_low_pips <= (stop_loss_pips * -1)):
                reached_sl_long = True

            if (not reached_sl_long and (order == 0)):
                if (check_row_high_pips >= take_profit_pips):
                    order = 1
            if (not reached_sl_short and (order == 0)):
                if (check_row_low_pips <= (take_profit_pips * -1)):
                    order = -1
        orders.append(order)
    return orders


def count_support_resistance(df, step, support_resistance=0, pip_size=0.0001, pip_threshold=5, compare_columns=None,
                             open_col='open', close_col='close', low_col='low', high_col='high'):
    if (compare_columns == None):
        compare_columns = [open_col, close_col, high_col, low_col]

    pip_threshold_value = pip_size * pip_threshold

    counts = []

    for i in range(0, len(df.index)):
        rows = df.iloc[max(0, i - step):i]
        count = 0
        close = df.iloc[i].close

        differences = pd.DataFrame(columns=compare_columns)

        for compare_column in compare_columns:
            differences[compare_column] = rows[compare_column].apply(lambda x: abs(close - x))

        differences = differences.min(axis=1)

        matches = differences.apply(lambda x: 1 if (x < pip_threshold_value) else 0)

        counts.append(matches.sum())
    return counts

def calculate_macd(df, fast_period = 12, slow_period = 26, signal = 9, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
  exp1 = df[close_col].ewm(span=fast_period, adjust=False).mean()
  exp2 = df[close_col].ewm(span=slow_period, adjust=False).mean()
  macd = exp1 - exp2
  return macd

def calculate_macd_signal(df, fast_period = 12, slow_period = 26, signal = 9, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
  macd = calculate_macd(df, fast_period, slow_period, signal, open_col, close_col, low_col, high_col)
  exp3 = macd.ewm(span=9, adjust=False).mean()
  return exp3

def check_macd_buy_sell(df, fast_period = 12, slow_period = 26, signal = 9, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
    macd = calculate_macd(df, fast_period, slow_period, signal, open_col, close_col, low_col, high_col)
    signal = calculate_macd_signal(df, fast_period, slow_period, signal, open_col, close_col, low_col, high_col)

    buy_sells = [0]

    for i in range(1, len(macd)):
        cur_macd = macd[i]
        cur_signal = signal[i]

        past_macd = macd[i - 1]
        past_signal = signal[i - 1]

        buy_sell = 0
        if ((past_macd < past_signal) and (cur_macd > cur_signal)):
            buy_sell = 1
        if ((past_macd > past_signal) and (cur_macd < cur_signal)):
            buy_sell = -1
        buy_sells.append(buy_sell)

    return buy_sells

def calculate_ema(df, days, smoothing = 2, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
    prices = df[close_col]
    ema = np.zeros(days - 1).tolist()
    ema.append(sum(prices[:days]) / days)
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    return ema