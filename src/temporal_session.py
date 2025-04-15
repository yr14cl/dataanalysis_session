import pandas as pd

def filter_valid_events(df, min_timestamps=2):
    df = df.copy()
    event_counts = df.groupby('event_id')['created_at'].count()
    valid_event_ids = event_counts[event_counts >= min_timestamps].index
    df = df[df['event_id'].isin(valid_event_ids)].copy()
    df = df.sort_values(by=['event_id', 'created_at'])
    return df

def assign_sessions_with_gap_and_maxspan(df, max_gap_seconds=2700, max_session_span_seconds=7200):
    df = df.copy()
    df['session_id'] = 0
    last_event = None
    session_counter = 0
    session_start_time = None
    last_time = None

    for idx, row in df.iterrows():
        current_event = row['event_id']
        current_time = row['created_at']

        if current_event != last_event:
            session_counter = 0
            session_start_time = current_time
        else:
            gap = (current_time - last_time).total_seconds()
            span = (current_time - session_start_time).total_seconds()
            if gap > max_gap_seconds or span > max_session_span_seconds:
                session_counter += 1
                session_start_time = current_time

        df.at[idx, 'session_id'] = session_counter
        last_event = current_event
        last_time = current_time

    return df

def compute_session_durations(df):
    session_df = df.groupby(['event_id', 'session_id']).agg(
        session_start=('created_at', 'min'),
        session_end=('created_at', 'max'),
        count=('created_at', 'count')
    ).reset_index()
    session_df['session_duration'] = (session_df['session_end'] - session_df['session_start']).dt.total_seconds()
    session_df = session_df[session_df['session_duration'] > 0]
    return session_df

def normalize_session_ids(session_df):
    normalized_ids = []
    for _, group in session_df.groupby('event_id'):
        valid = group[group['session_duration'] > 0].copy().sort_values(by='session_start')
        valid['normalized_session_id'] = range(1, len(valid) + 1)
        normalized_ids.append(valid)
    return pd.concat(normalized_ids)
