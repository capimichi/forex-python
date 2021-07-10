def calculate_top_shadow(df, open_col = 'open', close_col = 'close', low_col = 'low', high_col = 'high'):
    return df.apply(lambda x : (df[high_col] - df[open_col]) if (df[open_col] > df[close_col]) else (df[high_col] - df[close_col]))
