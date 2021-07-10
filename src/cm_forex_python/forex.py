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