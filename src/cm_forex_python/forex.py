def calculate_top_shadow(df, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
    return df.apply(lambda x : (x[high_col] - x[open_col]) if (x[open_col] > x[close_col]) else (x[high_col] - x[close_col]), axis = 1)
