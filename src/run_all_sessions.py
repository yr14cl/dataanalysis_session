import pandas as pd
from src import (
    load_sample_data,
    split_data_by_timestamp_presence,
    build_bipartite_graph,
    leiden_community_detection,
    map_communities_to_dataframe,
    assign_sessions_with_gap_and_maxspan,
    compute_session_durations,
    normalize_session_ids
)


df = pd.read_csv("data/sample.csv")
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

# temporal
df_with_time = df[df['created_at'].notna()].copy()
df_with_time = df_with_time.sort_values(by=['event_id', 'created_at'])
df_with_time = df_with_time.groupby('event_id').filter(lambda x: len(x) > 1)


df_smart = assign_sessions_with_gap_and_maxspan(df_with_time)
session_df = compute_session_durations(df_smart)
valid_sessions = session_df[session_df['session_duration'] > 0]
session_df = normalize_session_ids(valid_sessions)

# leiden
df_without_time = df[df['created_at'].isna()].copy()
df_without_time = df_without_time.groupby('event_id').filter(lambda x: len(x) > 1)

leiden_results = []
for event_id, group in df_without_time.groupby('event_id'):
    G = build_bipartite_graph(group)
    if G.number_of_edges() == 0:
        continue
    partition = leiden_community_detection(G)
    df_mapped = map_communities_to_dataframe(partition, group, event_id)
    leiden_results.append(df_mapped)

leiden_df = pd.concat(leiden_results)
df_leiden = df_without_time.copy()
df_leiden = df_leiden.join(leiden_df, how='left')

df_leiden.to_csv("outputs/leiden_sessions.csv", index=False)
session_df.to_csv("outputs/temporal_sessions.csv", index=False)
