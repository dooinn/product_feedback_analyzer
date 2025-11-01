import streamlit as st
import plotly.express as px

def show_dashboard(df):
    st.subheader("📊 Sentiment × Category Dashboard")

    st.markdown("### 🔍 Filters")
    categories = sorted(df["Category"].unique())
    sentiments = sorted(df["Sentiment"].unique())

    col1, col2 = st.columns(2)
    with col1:
        selected_categories = st.multiselect("Filter by Category", options=categories, default=categories)
    with col2:
        selected_sentiments = st.multiselect("Filter by Sentiment", options=sentiments, default=sentiments)

    filtered_df = df[df["Category"].isin(selected_categories) & df["Sentiment"].isin(selected_sentiments)]
    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
        return

    # KPI metrics
    st.markdown("### 📈 Key Performance Indicators")
    total_comments = len(filtered_df)
    positive_pct = (filtered_df["Sentiment"].eq("POSITIVE").sum() / total_comments) * 100
    negative_pct = (filtered_df["Sentiment"].eq("NEGATIVE").sum() / total_comments) * 100
    dominant_category = filtered_df["Category"].value_counts().idxmax()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("💬 Total Comments", f"{total_comments}")
    kpi2.metric("😊 % Positive", f"{positive_pct:.1f}%")
    kpi3.metric("😞 % Negative", f"{negative_pct:.1f}%")
    kpi4.metric("🏆 Top Category", dominant_category)

    # Stacked bar chart
    grouped = (
        filtered_df.groupby(["Category", "Sentiment"])
        .size()
        .reset_index(name="Count")
        .sort_values("Category")
    )
    fig = px.bar(
        grouped,
        x="Category",
        y="Count",
        color="Sentiment",
        text="Count",
        barmode="stack",
        color_discrete_map={"POSITIVE": "#4CAF50", "NEGATIVE": "#F44336"},
        title="Stacked Sentiment Distribution by Category",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Comment table
    st.dataframe(filtered_df[["comment", "Category", "Sentiment"]], use_container_width=True)

    # Download button
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download filtered results as CSV",
        data=csv,
        file_name="analyzed_comments_filtered.csv",
        mime="text/csv",
    )
