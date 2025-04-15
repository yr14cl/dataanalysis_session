# streamlit.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


@st.cache_data
def load_data():
    df =pd.read_csv("outputs/all_sessions.csv") 
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    return df

# Figure 1: Distribution of the number of questions answered per session

def plot_session_answer_distribution(df):
    st.subheader("1. Number of answers per session")

    df_clean = df[df['session_id'].notna()]
    session_types = df_clean['session_type'].dropna().unique().tolist()
    session_types.insert(0, 'total')
    selected_type = st.selectbox("Select session type", session_types)

    filtered_df = df_clean if selected_type == 'total' else df_clean[df_clean['session_type'] == selected_type]

    session_counts = filtered_df.groupby('session_id').size().reset_index(name='answer_count')

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=session_counts, x='answer_count', ax=ax, color='skyblue')

    ax.set_title(f"Distribution of number of answers per session ({selected_type})")
    ax.set_xlabel("Number of answers per session")
    ax.set_ylabel("Number of sessions")

    st.pyplot(fig)


# Figure 2: Number of sessions each student participated in per month 
def plot_sessions_per_student_month(df):
    st.subheader("2. Number of sessions per student per month")
    df = df[df['session_id'].notna()].copy()
    df['year_month'] = df['created_at'].dt.to_period('M')
    sessions_per_student_month = df.groupby(['participant_id', 'year_month'])['session_id'].nunique().reset_index(name='session_count')
    monthly_distribution = sessions_per_student_month['session_count'].value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(monthly_distribution.index, monthly_distribution.values)
    total_monthly = monthly_distribution.sum()
    for bar in bars:
        height = bar.get_height()
        percent = f"{(height / total_monthly) * 100:.1f}%"
        ax2.text(bar.get_x() + bar.get_width()/2, height, percent, ha='center', va='bottom', fontsize=7)
    ax2.set_xlabel("Sessions per student per month")
    ax2.set_ylabel("Number of student-months")
    ax2.set_title("Distribution: Sessions per Student per Month")
    st.pyplot(fig2)

# Figure 3: Top 10% Student Session Distribution
def plot_top10_student_monthly(df):
    st.subheader("3. Top 10% Student Session Distribution (PM Request)")
    df_top10 = df[df['session_id'].notna()].copy()
    df_top10['year_month'] = df_top10['created_at'].dt.to_period('M').astype(str)
    monthly = df_top10.groupby(['year_month', 'participant_id'])['session_id'].nunique().reset_index(name='session_count')
    month_options = sorted(monthly['year_month'].unique())
    selected_month = st.selectbox("Select month", month_options)
    month_df = monthly[monthly['year_month'] == selected_month].sort_values(by='session_count', ascending=False)
    top_n = max(int(len(month_df) * 0.1), 1)
    top10_df = month_df.head(top_n)
    st.markdown(f"**Top {top_n} students in {selected_month}**")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top10_df, x='participant_id', y='session_count', ax=ax, palette='Blues_r')
    ax.set_title(f"Top 10% Students by Session Count - {selected_month}")
    ax.set_xlabel("Participant ID")
    ax.set_ylabel("Session Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.dataframe(top10_df.reset_index(drop=True))
    st.markdown("Definition of Top 10% Most Active Students: The top X% of students with the highest number of sessions participated in, within that month. Instead of using a statistical quantile threshold (e.g., session_count ≥ 90th percentile), we rank all students within each month by their number of sessions, and then select the top 10% by count.")

# Figure 3.1: Top 10% vs All monthly average session trends
def plot_top10_vs_all_trend(df):
    st.subheader("3.1 Monthly Session Trend per User")
    df = df[df['session_id'].notna()].copy()
    df['year_month'] = df['created_at'].dt.to_period('M')
    session_types = df['session_type'].dropna().unique().tolist()
    session_types.insert(0, 'total')
    selected_type = st.selectbox("Select session type to analyze", session_types)
    if selected_type != 'total':
        df = df[df['session_type'] == selected_type]
    top10_checkbox = st.checkbox("Only show top 10% most active students per month")
    show_sessions = st.toggle("Show total sessions instead of total users", value=False)
    monthly_user_sessions = df.groupby(['year_month', 'participant_id'])['session_id'].nunique().reset_index(name='session_count')
    if top10_checkbox:
        def filter_top10_by_rank(group):
            if len(group) < 10:
                return group
            group_sorted = group.sort_values(by='session_count', ascending=False)
            top_n = max(int(len(group_sorted) * 0.1), 1)
            return group_sorted.head(top_n)
        monthly_user_sessions = monthly_user_sessions.groupby('year_month', group_keys=False).apply(filter_top10_by_rank).reset_index(drop=True)
    monthly_avg = monthly_user_sessions.groupby('year_month').agg(
        total_users=('participant_id', 'nunique'),
        avg_sessions_per_user=('session_count', 'mean')
    ).reset_index()
    monthly_sessions = df.groupby('year_month')['session_id'].nunique().reset_index(name='total_sessions')
    trend_df = pd.merge(monthly_avg, monthly_sessions, on='year_month', how='left')
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(trend_df['year_month'].astype(str), trend_df['avg_sessions_per_user'], marker='o', color='tab:blue', label='Avg Sessions/User')
    ax1.set_ylabel("Avg Sessions per User", color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax2 = ax1.twinx()
    bar_y = trend_df['total_sessions'] if show_sessions else trend_df['total_users']
    bar_label = "Total Sessions" if show_sessions else "Total Users"
    ax2.bar(trend_df['year_month'].astype(str), bar_y, alpha=0.3, color='gray', label=bar_label)
    ax2.set_ylabel(bar_label, color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')
    title_suffix = "Top 10%" if top10_checkbox else "All"
    plt.title(f"Monthly Avg Sessions/User ({title_suffix}) - {selected_type}")
    fig.tight_layout()
    st.pyplot(fig)

# Figure 3.2 and 3.3: Top10 vs All Bar Chart and Histogram
def plot_top10_comparison_histogram(df):
    st.subheader("3.2 Compare Top 10% vs All Users - Avg Sessions per Month")
    df = df[df['session_id'].notna()].copy()
    df['year_month'] = df['created_at'].dt.to_period('M')
    monthly_user_sessions = df.groupby(['year_month', 'participant_id'])['session_id'].nunique().reset_index(name='session_count')
    results = []
    for ym, group in monthly_user_sessions.groupby('year_month'):
        if len(group) < 5:
            continue
        group_sorted = group.sort_values(by='session_count', ascending=False)
        top_n = max(int(len(group_sorted) * 0.1), 1)
        top10 = group_sorted.head(top_n)
        results.append({
            'year_month': str(ym),
            'avg_all': group['session_count'].mean(),
            'avg_top10': top10['session_count'].mean(),
            'top10_count': top10.shape[0],
            'total_count': group.shape[0]
        })
    compare_df = pd.DataFrame(results)
    fig, ax = plt.subplots(figsize=(10, 6))
    x = compare_df['year_month']
    ax.plot(x, compare_df['avg_all'], marker='o', label='All Users')
    ax.plot(x, compare_df['avg_top10'], marker='s', label='Top 10% Users')
    ax.set_ylabel("Avg Session Count")
    ax.set_xlabel("Month")
    ax.set_title("Top 10% vs All Users - Avg Sessions per Month")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.dataframe(compare_df)

    st.subheader("3.3 Session Count Distribution per Student")
    df['year_month'] = df['created_at'].dt.to_period('M').astype(str)
    student_monthly_sessions = df.groupby(['year_month', 'participant_id'])['session_id'].nunique().reset_index(name='session_count')
    selected_month = st.selectbox("Select a month to view histogram", sorted(student_monthly_sessions['year_month'].unique()))
    filtered_month_df = student_monthly_sessions[student_monthly_sessions['year_month'] == selected_month]
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.histplot(filtered_month_df['session_count'], bins=20, kde=False, ax=ax2)
    ax2.set_title(f"Session Count Distribution - {selected_month}")
    ax2.set_xlabel("Session Count per Student")
    ax2.set_ylabel("Number of Students")
    st.pyplot(fig2)


def main():
    st.title("Session Distribution Explorer")
    df = load_data()
    plot_session_answer_distribution(df)
    plot_sessions_per_student_month(df)
    plot_top10_student_monthly(df)
    plot_top10_vs_all_trend(df)
    plot_top10_comparison_histogram(df)

if __name__ == "__main__":
    main()
