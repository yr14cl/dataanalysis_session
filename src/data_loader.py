import pandas as pd

def load_sample_data(path):
  df= pd.read_csv(path)
  df['create_at']= pd.to_datetime(df['created_at'],errors = 'coerce')
  return df
  
def split_data_by_timestamp_presence(df):
    df_with_time = df[df['created_at'].notna()].copy()
    df_without_time = df[df['created_at'].isna()].copy()
    return df_with_time, df_without_time
