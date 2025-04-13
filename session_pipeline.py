
from src.data_loader import load_clean_data
from src.temporal_session import reconstruct_temporal_sessions
from src.leiden_session import reconstruct_leiden_sessions
from src.session_analysis import analyze_sessions
import pandas as pd

# 1. loading data
df = load_clean_data("data/sample.csv")

# 2. Temporal session
df_temporal = reconstruct_temporal_sessions(df)

# 3. Leiden session 
df_leiden = reconstruct_leiden_sessions(df)

# 4. merge two session
df_all = pd.concat([df_temporal, df_leiden], ignore_index=True)

# 5. analyse
analyze_sessions(df_all)

