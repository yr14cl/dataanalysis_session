import pandas as pd

def load_clean_data(path):
  df= pd.read_csv(path)
  df['create_at']= pd.to_datetime(df['created_at'],errots = 'coerce')
  return df
