# INTERNATIONAL DEBT ANALYSIS DASHBOARD

import streamlit as st
import plotly.express as px
import pandas as pd
from db_connection import get_connection

st.set_page_config(
    page_title="International Debt Analysis",
    layout="wide"
)

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0F172A;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.3);
}

/* Headers */
h1, h2, h3 {
    color: #38BDF8;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* Expander */
.streamlit-expanderHeader {
    font-weight: bold;
    color: #38BDF8;
}

</style>
""", unsafe_allow_html=True)

st.title("🌍 International Debt Analysis")

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Choose Analysis",
    [
        "Overview",
        "Country Analysis",
        "Indicator Analysis",
        "Advanced Analysis"
    ]
)

# OVERVIEW PAGE

if page == "Overview":

    st.header("📊 Executive Overview")

    try:
        conn = get_connection()

        # Dashboard KPIs
        total_countries = pd.read_sql("""
            SELECT COUNT(DISTINCT country_name) AS value
            FROM vw_country_debt
        """, conn).iloc[0, 0]

        total_indicators = pd.read_sql("""
            SELECT COUNT(DISTINCT series_name) AS value
            FROM vw_country_debt
        """, conn).iloc[0, 0]

        total_records = pd.read_sql("""
            SELECT COUNT(*) AS value
            FROM vw_country_debt
        """, conn).iloc[0, 0]

        total_debt = pd.read_sql("""
            SELECT ROUND(SUM(debt_value)::numeric,2) AS value
            FROM vw_country_debt
        """, conn).iloc[0, 0]

        st.subheader("🌍 Global Debt")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🌍 Countries", total_countries)
        col2.metric("📈 Indicators", total_indicators)
        col3.metric("📄 Records", total_records)
        col4.metric("💰 Global Debt", f"{total_debt:,.0f}")

        st.markdown("---")

        # Query 9
        stats = pd.read_sql("""
            SELECT
                ROUND(MIN(debt_value)::numeric,2) AS min_debt,
                ROUND(MAX(debt_value)::numeric,2) AS max_debt,
                ROUND(AVG(debt_value)::numeric,2) AS avg_debt
            FROM vw_country_debt
        """, conn)

        st.subheader("📊 Debt Statistics")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Minimum Debt",
            f"{stats['min_debt'][0]:,.0f}"
        )

        c2.metric(
            "Maximum Debt",
            f"{stats['max_debt'][0]:,.0f}"
        )

        c3.metric(
            "Average Debt",
            f"{stats['avg_debt'][0]:,.0f}"
        )

        st.markdown("---")

        st.subheader("🏆 Top 10 Countries by Total Debt")

        # Query 12
        top_countries = pd.read_sql("""
            SELECT
                country_name,
                ROUND(SUM(debt_value)::numeric, 2) AS total_debt
            FROM vw_country_debt
            GROUP BY country_name
            ORDER BY total_debt DESC
            LIMIT 10;
        """, conn)

        fig = px.bar(
            top_countries.sort_values("total_debt"),
            x="total_debt",
            y="country_name",
            orientation="h",
            title ="Top 10 Countries by Total Debt"
        )
        fig.update_layout(
            yaxis_title="Country",
            xaxis_title="Total Debt (USD)"
        )

        col1, col2 = st.columns([3,1])

        with col1:
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📌 Key Insights")

            st.info(f"🌍 Countries: {total_countries}")

            st.info(f"📈 Indicators: {total_indicators}")

            st.info(f"📄 Records: {total_records}")

        tab1, tab2, tab3 = st.tabs(
            ["Countries", "Indicators", "Top 20 Country Records"]
        )

        # Query 4  
        with st.expander("📄 First 10 Records"):

            first10_df = pd.read_sql("""
                SELECT *
                FROM vw_country_debt
                LIMIT 10
            """, conn)

            st.dataframe(first10_df)

        # Query 1
        with tab1:

            countries_df = pd.read_sql("""
                SELECT DISTINCT country_name
                FROM vw_country_debt
                ORDER BY country_name
            """, conn)

            st.dataframe(countries_df)

        # Query 6
        with tab2:

            indicators_df = pd.read_sql("""
                SELECT DISTINCT series_name
                FROM vw_country_debt
                ORDER BY series_name
            """, conn)

            st.dataframe(indicators_df)

         # Query 7
        with tab3:

            records_df = pd.read_sql("""
                SELECT
                    country_name,
                    COUNT(*) AS total_records
                FROM vw_country_debt
                GROUP BY country_name
                ORDER BY total_records DESC
                LIMIT 20
            """, conn)

            st.dataframe(records_df)

         # Query 8
        with st.expander("💰 Debt Greater Than 1 Billion USD"):

            debt_billion_df = pd.read_sql("""
                SELECT *
                FROM vw_country_debt
                WHERE debt_value > 1000000000
                LIMIT 100
            """, conn)

            st.dataframe(debt_billion_df)

        conn.close()

    except Exception as e:
        st.error(f"Database Connection Error: {e}")

# COUNTRY ANALYSIS PAGE

elif page == "Country Analysis":

    st.header("🌍 Country Analysis")

    conn = get_connection()

    # Load countries for user selection
    countries = pd.read_sql("""
        SELECT DISTINCT country_name
        FROM vw_country_debt
        ORDER BY country_name
    """, conn)

    selected_country = st.selectbox(
        "Select Country",
        countries["country_name"]
    )

    # Query 11
    country_debt = pd.read_sql(f"""
        SELECT
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        WHERE country_name = '{selected_country}'
    """, conn)

    st.metric(
        "Total Debt",
        f"{country_debt.iloc[0,0]:,.0f}"
    )

    # Query 17
    indicator_data = pd.read_sql(f"""
        SELECT
            series_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        WHERE country_name = '{selected_country}'
        GROUP BY series_name
        ORDER BY total_debt DESC
        LIMIT 10
    """, conn)

    fig = px.bar(
        indicator_data.sort_values("total_debt"),
        x="total_debt",
        y="series_name",
        orientation="h",
        title=f"Top Indicators - {selected_country}"
    )

    fig.update_layout(
        yaxis_title="Indicator",
        xaxis_title="Total Debt (USD)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Debt trend across years for selected country
    st.subheader(f"📈 Debt Trend - {selected_country}")

    trend_data = pd.read_sql(f"""
        SELECT
            year,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        WHERE country_name = '{selected_country}'
        GROUP BY year
        ORDER BY year
    """, conn)

    fig2 = px.line(
        trend_data,
        x="year",
        y="total_debt",
        markers=True,
        title=f"Debt Trend for {selected_country}"
    )

    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Debt"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    #Query 30
    st.subheader(f"🏆 Dominant Indicator - {selected_country}")

    dominant_indicator = pd.read_sql(f"""
        SELECT *
        FROM
        (
            SELECT
                country_name,
                series_name,
                ROUND(SUM(debt_value)::numeric,2) AS total_debt,
                RANK() OVER(
                    PARTITION BY country_name
                    ORDER BY SUM(debt_value) DESC
                ) AS rank_no
            FROM vw_country_debt
            WHERE country_name = '{selected_country}'
            GROUP BY country_name, series_name
        ) t
        WHERE rank_no = 1
    """, conn)

    if not dominant_indicator.empty:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Dominant Indicator",
                dominant_indicator.iloc[0]["series_name"]
            )

        with col2:
            st.metric(
                "Debt Amount",
                f"{dominant_indicator.iloc[0]['total_debt']:,.0f}"
            )
    
    
    # Query 27
    st.subheader(f"📈 Cumulative Debt Trend - {selected_country}")

    cumulative_data = pd.read_sql(f"""
        SELECT
            year,
            SUM(debt_value) AS yearly_debt,
            SUM(SUM(debt_value))
            OVER(
                ORDER BY year
            ) AS cumulative_debt
        FROM vw_country_debt
        WHERE country_name = '{selected_country}'
        GROUP BY year
        ORDER BY year
    """, conn)

    fig_cum = px.line(
        cumulative_data,
        x="year",
        y="cumulative_debt",
        markers=True,
        title=f"Cumulative Debt - {selected_country}"
    )

    fig_cum.update_layout(
        xaxis_title="Year",
        yaxis_title="Cumulative Debt"
    )

    st.plotly_chart(
        fig_cum,
        use_container_width=True
    )

    # Query 13
    st.subheader("📊 Top 10 Countries by Average Debt")

    avg_country_debt = pd.read_sql("""
        SELECT
            country_name,
            ROUND(AVG(debt_value)::numeric,2) AS avg_debt
        FROM vw_country_debt
        GROUP BY country_name
        ORDER BY avg_debt DESC
        LIMIT 10
    """, conn)

    fig_avg = px.bar(
        avg_country_debt.sort_values("avg_debt"),
        x="avg_debt",
        y="country_name",
        orientation="h",
        title="Top 10 Countries by Average Debt"
    )

    fig_avg.update_layout(
        xaxis_title="Average Debt",
        yaxis_title="Country"
    )

    st.plotly_chart(
        fig_avg,
        use_container_width=True
    )

    # Query 18
    st.subheader("📈 Countries with Most Indicators")

    indicator_count = pd.read_sql("""
        SELECT
            country_name,
            COUNT(DISTINCT series_name) AS total_indicators
        FROM vw_country_debt
        GROUP BY country_name
        ORDER BY total_indicators DESC
        LIMIT 15
    """, conn)

    fig_indicator = px.bar(
        indicator_count.sort_values("total_indicators"),
        x="total_indicators",
        y="country_name",
        orientation="h",
        title="Countries by Number of Indicators"
    )

    fig_indicator.update_layout(
        xaxis_title="Number of Indicators",
        yaxis_title="Country"
    )

    st.plotly_chart(
        fig_indicator,
        use_container_width=True
    )

    # Query 11
    st.subheader("💰 Top 10 Countries by Total Debt")

    top_debt_countries = pd.read_sql("""
        SELECT
            country_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        GROUP BY country_name
        ORDER BY total_debt DESC
        LIMIT 10
    """, conn)

    st.dataframe(
        top_debt_countries,
        use_container_width=True
    )

    # Query 19
    st.subheader("📊 Countries Above Global Average Debt")

    above_avg_df = pd.read_sql("""
        SELECT
            country_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        GROUP BY country_name
        HAVING SUM(debt_value) >
        (
            SELECT AVG(country_total)
            FROM
            (
                SELECT SUM(debt_value) AS country_total
                FROM vw_country_debt
                GROUP BY country_name
            ) x
        )
        ORDER BY total_debt DESC
    """, conn)

    st.dataframe(
        above_avg_df,
        use_container_width=True
    )


    conn.close()

# INDICATOR ANALYSIS PAGE

elif page == "Indicator Analysis":

    # Query 14
    st.header("📈 Indicator Analysis")

    conn = get_connection()

    indicator_data = pd.read_sql("""
        SELECT
            series_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        GROUP BY series_name
        ORDER BY total_debt DESC
        LIMIT 10
    """, conn)

    fig = px.bar(
        indicator_data.sort_values("total_debt"),
        x="total_debt",
        y="series_name",
        orientation="h",
        title="Top 10 Indicators by Total Debt"
    )

    fig.update_layout(
        yaxis_title="Indicator",
        xaxis_title="Total Debt (USD)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📊 Indicators Above Overall Average Debt")

    above_avg_df = pd.read_sql("""
        SELECT
            series_name,
            ROUND(AVG(debt_value)::numeric,2) AS avg_debt
        FROM vw_country_debt
        GROUP BY series_name
        HAVING AVG(debt_value) >
        (
            SELECT AVG(debt_value)
            FROM vw_country_debt
        )
        ORDER BY avg_debt DESC
    """, conn)

    st.dataframe(
        above_avg_df,
        use_container_width=True
    )

    # Query 15

    top_indicator = pd.read_sql("""
        SELECT
            series_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        GROUP BY series_name
        ORDER BY total_debt DESC
        LIMIT 1
    """, conn)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🏆 Highest Debt Indicator",
            top_indicator.iloc[0]["series_name"]
        )

    with col2:
        st.metric(
            "💰 Total Debt",
            f"{top_indicator.iloc[0]['total_debt']:,.0f}"
        )

    st.subheader("🏆 Top 5 Indicators Contributing Most Debt")

    top5_indicators = pd.read_sql("""
        SELECT
            series_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        GROUP BY series_name
        ORDER BY total_debt DESC
        LIMIT 5
    """, conn)

    fig_top5 = px.pie(
        top5_indicators,
        names="series_name",
        values="total_debt",
        title="Top 5 Indicators by Debt Contribution"
    )

    st.plotly_chart(
        fig_top5,
        use_container_width=True
    )
    
    # Query 14
    st.subheader("📋 Indicator Debt Summary")

    indicator_table = pd.read_sql("""
        SELECT
            series_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        GROUP BY series_name
        ORDER BY total_debt DESC
    """, conn)

    st.dataframe(
        indicator_table,
        use_container_width=True
    )

    conn.close()

# ADVANCED ANALYSIS PAGE

elif page == "Advanced Analysis":

    st.header("🚀 Advanced Analysis")

    conn = get_connection()
    
    # Query 22
    contribution_data = pd.read_sql("""
        SELECT
            country_name,
            ROUND(
                SUM(debt_value) * 100.0 /
                (SELECT SUM(debt_value)
                 FROM vw_country_debt),
                2
            ) AS contribution_percentage
        FROM vw_country_debt
        GROUP BY country_name
        ORDER BY contribution_percentage DESC
        LIMIT 10
    """, conn)

    fig = px.pie(
        contribution_data,
        names="country_name",
        values="contribution_percentage",
        title="Top Countries Contribution to Global Debt (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Query 29
    st.subheader("🌎 Countries Contributing More Than 5% of Global Debt")

    top_contributors = pd.read_sql("""
        SELECT
            country_name,
            ROUND(
                SUM(debt_value) * 100.0 /
                (SELECT SUM(debt_value)
                FROM vw_country_debt),
                2
            ) AS contribution_percentage
        FROM vw_country_debt
        GROUP BY country_name
        HAVING
        (
            SUM(debt_value) * 100.0 /
            (SELECT SUM(debt_value)
            FROM vw_country_debt)
        ) > 5
        ORDER BY contribution_percentage DESC
    """, conn)

    st.dataframe(
        top_contributors,
        use_container_width=True
    )

    st.subheader("📉 Country with Lowest Total Debt")

    lowest_debt = pd.read_sql("""
        SELECT
            country_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        GROUP BY country_name
        ORDER BY total_debt ASC
        LIMIT 1
    """, conn)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Country",
            lowest_debt.iloc[0]["country_name"]
        )

    with col2:
        st.metric(
            "Total Debt",
            f"{lowest_debt.iloc[0]['total_debt']:,.0f}"
        )

    # Query 20
    st.subheader("🏅 Country Debt Ranking")

    ranking_data = pd.read_sql("""
        SELECT
            country_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt,
            RANK() OVER(
                ORDER BY SUM(debt_value) DESC
            ) AS debt_rank
        FROM vw_country_debt
        GROUP BY country_name
        LIMIT 20
    """, conn)
    
    fig_rank = px.bar(
        ranking_data.sort_values("total_debt"),
        x="total_debt",
        y="country_name",
        orientation="h",
        color="debt_rank",
        title="Top Ranked Countries by Debt"
    )

    st.plotly_chart(
        fig_rank,
        use_container_width=True
    )
    st.subheader("🏆 Top 3 Countries by Indicator")

    indicators = pd.read_sql("""
        SELECT DISTINCT series_name
        FROM vw_country_debt
        ORDER BY series_name
    """, conn)

    selected_indicator = st.selectbox(
        "Select Indicator",
        indicators["series_name"]
    )

    top3_df = pd.read_sql(f"""
        SELECT
            country_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        WHERE series_name = '{selected_indicator}'
        GROUP BY country_name
        ORDER BY total_debt DESC
        LIMIT 3
    """, conn)

    fig = px.bar(
        top3_df.sort_values("total_debt"),
        x="total_debt",
        y="country_name",
        orientation="h",
        title=f"Top 3 Countries - {selected_indicator}"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Debt Range by Country")

    debt_range = pd.read_sql("""
        SELECT
            country_name,
            ROUND(
                MAX(debt_value) - MIN(debt_value),
                2
            ) AS debt_difference
        FROM vw_country_debt
        GROUP BY country_name
        ORDER BY debt_difference DESC
        LIMIT 15
    """, conn)

    fig_range = px.bar(
        debt_range.sort_values("debt_difference"),
        x="debt_difference",
        y="country_name",
        orientation="h",
        title="Top 15 Countries by Debt Range"
    )

    fig_range.update_layout(
        xaxis_title="Debt Difference",
        yaxis_title="Country"
    )

    st.plotly_chart(
        fig_range,
        use_container_width=True
    )

    st.subheader("🏷️ Country Debt Categories")

    debt_category = pd.read_sql("""
        SELECT
            country_name,
            SUM(debt_value) AS total_debt,
            CASE
                WHEN SUM(debt_value) > 1000000000000
                    THEN 'High Debt'
                WHEN SUM(debt_value) > 100000000000
                    THEN 'Medium Debt'
                ELSE 'Low Debt'
            END AS debt_category
        FROM vw_country_debt
        GROUP BY country_name
    """, conn)

    category_summary = debt_category.groupby(
        "debt_category"
    ).size().reset_index(name="count")

    fig_category = px.pie(
        category_summary,
        names="debt_category",
        values="count",
        title="Countries by Debt Category"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

    st.subheader("📈 Global Debt Trend by Year")

    yearly_data = pd.read_sql("""
        SELECT
            year,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        GROUP BY year
        ORDER BY year
    """, conn)

    fig = px.line(
        yearly_data,
        x="year",
        y="total_debt",
        markers=True,
        title="Global Debt Trend Over Time"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Debt"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("🌍 Country & Indicator Combination Debt")

    combo_df = pd.read_sql("""
        SELECT
            country_name,
            series_name,
            ROUND(SUM(debt_value)::numeric,2) AS total_debt
        FROM vw_country_debt
        GROUP BY country_name, series_name
        ORDER BY total_debt DESC
        LIMIT 20
    """, conn)

    st.dataframe(
        combo_df,
        use_container_width=True
    )
    conn.close()