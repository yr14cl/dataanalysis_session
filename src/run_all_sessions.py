import pandas as pd
from src import (
    load_sample_data,
    split_data_by_timestamp_presence,
    build_bipartite_graph,
    leiden_community_detection,
    map_communities_to_dataframe,
    assign_sessions_with_gap_and_maxspan,
    compute_session_durations,
    normalize_session_ids,
    filter_valid_events
)
import os

df = load_sample_data("data/sample.csv")

df_with_time, df_without_time = split_data_by_timestamp_presence(df)

#  Temporal session reconstruction
df_with_time = filter_valid_events(df_with_time)
df_with_time = df_with_time.sort_values(by=["event_id", "created_at"])
df_temporal = assign_sessions_with_gap_and_maxspan(df_with_time)
df_temporal_duration = compute_session_durations(df_temporal)
df_temporal_duration = normalize_session_ids(df_temporal_duration)

# Leiden session reconstruction
leiden_results = []
for event_id, group in df_without_time.groupby("event_id"):
    if len(group) <= 1:
        continue
    G = build_bipartite_graph(group)
    if G.number_of_edges() == 0:
        continue
    partition = leiden_community_detection(G)
    df_mapped = map_communities_to_dataframe(partition, group, event_id)
    leiden_results.append(df_mapped)

# merge data 
if leiden_results:
    leiden_df = pd.concat(leiden_results)
    df_leiden = df_without_time.copy()
    df_leiden = df_leiden.join(leiden_df, how='left')
else:
    df_leiden = pd.DataFrame()

df_temporal["session_type"] = "temporal"
df_all = pd.concat([df_temporal, df_leiden], ignore_index=True, sort=False)

os.makedirs("outputs", exist_ok=True)
df_temporal.to_csv("outputs/temporal_sessions.csv", index=False)
df_leiden.to_csv("outputs/leiden_sessions.csv", index=False)
df_all.to_csv("outputs/all_sessions.csv", index=False)

print(" Session reconstruction completed.")

