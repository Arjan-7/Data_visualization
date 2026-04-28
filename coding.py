import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI, Digital Platforms & Students' Lives",
    layout="wide"
)

# ---------------- TITLE & INTRO ----------------
st.title("Impact of AI‑Driven Digital Platforms on Students' Academic & Personal Life")

st.markdown("""
This dashboard explores how **AI‑driven digital platforms and social media** relate to students'
demographics, usage behaviour, and their reported **academic performance, sleep, mental health, and overall life impact**.
""")

st.markdown("""
**Data source:** Kaggle – *"Social Media Impact on Life"* dataset (student survey on digital platform usage).  
_All charts and visuals in this dashboard are generated directly from a custom **Streamlit** application
built with Python, using this Kaggle dataset._
""")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("social_media_impact_on_life.csv")

df = load_data()

# NEW: total records in whole dataset
st.markdown(f"**Total students in dataset:** {len(df)}")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")
st.sidebar.markdown("Use these filters to focus on specific student groups.")

academic_levels = st.sidebar.multiselect(
    "Academic level",
    options=sorted(df["Academic_Level"].dropna().unique()),
    default=sorted(df["Academic_Level"].dropna().unique())
)

genders = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

countries = st.sidebar.multiselect(
    "Country",
    options=sorted(df["Country"].dropna().unique()),
    default=[]  # user must choose at least one
)

usage_range = st.sidebar.slider(
    "Daily usage range (hours)",
    float(df["Avg_Daily_Usage_Hours"].min()),
    float(df["Avg_Daily_Usage_Hours"].max()),
    (float(df["Avg_Daily_Usage_Hours"].min()),
     float(df["Avg_Daily_Usage_Hours"].max()))
)

if len(countries) == 0:
    st.warning("Select at least one country from the sidebar to see the charts.")
    st.stop()

# Apply filters
filtered_df = df[
    df["Academic_Level"].isin(academic_levels)
    & df["Gender"].isin(genders)
    & df["Country"].isin(countries)
    & df["Avg_Daily_Usage_Hours"].between(usage_range[0], usage_range[1])
]

st.subheader("Filtered data preview")
st.write(filtered_df.head())
st.markdown(f"**Total students after filters:** {len(filtered_df)}")

if filtered_df.empty:
    st.info("No data for the selected filters. Please adjust filters and try again.")
    st.stop()

# =========================================================
# 1. DEMOGRAPHICS
# =========================================================
st.markdown("## 1. Who are the students using AI‑driven platforms?")
st.markdown("""
These charts show the **demographic profile** and **most used platforms** of the selected students.
""")

col1, col2, col3 = st.columns(3)

with col1:
    gender_counts = filtered_df["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    fig_gender = px.bar(
        gender_counts,
        x="Gender",
        y="Count",
        title="Students by gender",
        text="Count"
    )
    fig_gender.update_traces(textposition="outside")
    st.plotly_chart(fig_gender, use_container_width=True)

with col2:
    level_counts = filtered_df["Academic_Level"].value_counts().reset_index()
    level_counts.columns = ["Academic_Level", "Count"]
    fig_level = px.bar(
        level_counts,
        x="Academic_Level",
        y="Count",
        title="Students by academic level",
        text="Count"
    )
    fig_level.update_traces(textposition="outside")
    st.plotly_chart(fig_level, use_container_width=True)

with col3:
    platform_counts = filtered_df["Most_Used_Platform"].value_counts().reset_index()
    platform_counts.columns = ["Most_Used_Platform", "Count"]
    fig_platform = px.bar(
        platform_counts,
        x="Most_Used_Platform",
        y="Count",
        title="Most used digital / social platforms",
        text="Count"
    )
    fig_platform.update_traces(textposition="outside")
    st.plotly_chart(fig_platform, use_container_width=True)

st.markdown("""
**Key insight (demographics):**  
Students from different genders and academic levels use a variety of AI‑driven platforms daily, with
a few platforms (like Instagram / YouTube / TikTok) dominating their digital life.

**Conclusion:**  
AI‑powered recommendation systems on these popular platforms have a large influence on how students
spend their time online.
""")

# =========================================================
# 2. USAGE BEHAVIOUR
# =========================================================
st.markdown("## 2. How much time do students spend on these platforms?")
st.markdown("""
Here we focus on **daily usage hours** and how usage differs by platform.
""")

col4, col5 = st.columns(2)

with col4:
    fig_usage_hist = px.histogram(
        filtered_df,
        x="Avg_Daily_Usage_Hours",
        nbins=10,
        title="Distribution of daily usage (hours)",
        labels={"Avg_Daily_Usage_Hours": "Avg daily usage (hours)"}
    )
    st.plotly_chart(fig_usage_hist, use_container_width=True)

with col5:
    usage_by_platform = (
        filtered_df
        .groupby("Most_Used_Platform")["Avg_Daily_Usage_Hours"]
        .mean()
        .reset_index()
        .sort_values("Avg_Daily_Usage_Hours", ascending=False)
    )
    fig_usage_platform = px.bar(
        usage_by_platform,
        x="Most_Used_Platform",
        y="Avg_Daily_Usage_Hours",
        title="Average daily usage by platform",
        labels={"Avg_Daily_Usage_Hours": "Avg hours per day"},
        text="Avg_Daily_Usage_Hours"
    )
    fig_usage_platform.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    st.plotly_chart(fig_usage_platform, use_container_width=True)

st.markdown("""
**Key insight (usage behaviour):**  
Many students spend several hours per day on digital platforms, and some heavy users exceed a few
hours of usage daily.

**Conclusion:**  
High daily usage gives AI algorithms more data and more chances to keep students engaged, which can
start to compete with study, sleep, and offline activities.
""")

# =========================================================
# 3. ACADEMIC PERFORMANCE
# =========================================================
st.markdown("## 3. Does usage affect academic performance?")
st.markdown("""
We compare **daily usage hours** between students who say digital platforms **do** vs **do not**
affect their academic performance.
""")

col6, col7 = st.columns(2)

with col6:
    usage_perf = (
        filtered_df
        .groupby("Affects_Academic_Performance")["Avg_Daily_Usage_Hours"]
        .mean()
        .reset_index()
    )
    fig_usage_perf = px.bar(
        usage_perf,
        x="Affects_Academic_Performance",
        y="Avg_Daily_Usage_Hours",
        title="Average usage vs academic performance impact",
        labels={
            "Affects_Academic_Performance": "Affects academic performance?",
            "Avg_Daily_Usage_Hours": "Avg daily usage (hours)"
        },
        text="Avg_Daily_Usage_Hours"
    )
    fig_usage_perf.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    st.plotly_chart(fig_usage_perf, use_container_width=True)

with col7:
    fig_box_perf = px.box(
        filtered_df,
        x="Affects_Academic_Performance",
        y="Avg_Daily_Usage_Hours",
        title="Usage spread by academic impact group",
        labels={
            "Affects_Academic_Performance": "Affects academic performance?",
            "Avg_Daily_Usage_Hours": "Avg daily usage (hours)"
        }
    )
    st.plotly_chart(fig_box_perf, use_container_width=True)

st.markdown("""
**Key insight (academic performance):**  
Students who report that digital platforms affect their academic performance tend to have **higher
average daily usage** and a wider spread of hours than those who report no impact.

**Conclusion:**  
Very heavy use of AI‑driven social and digital platforms is associated with more self‑reported
academic problems, suggesting that time spent online can interfere with focus and study quality.
""")

# =========================================================
# 4. SLEEP & MENTAL HEALTH
# =========================================================
st.markdown("## 4. How is digital life linked to sleep and mental health?")
st.markdown("""
These charts highlight relationships between **usage hours**, **sleep duration**, and **mental health scores**.
""")

col8, col9 = st.columns(2)

with col8:
    fig_sleep = px.scatter(
        filtered_df,
        x="Avg_Daily_Usage_Hours",
        y="Sleep_Hours_Per_Night",
        color="Gender",
        hover_data=["Academic_Level", "Country"],
        labels={
            "Avg_Daily_Usage_Hours": "Avg daily usage (hours)",
            "Sleep_Hours_Per_Night": "Sleep hours per night"
        },
        title="Daily usage vs sleep hours"
    )
    st.plotly_chart(fig_sleep, use_container_width=True)

with col9:
    fig_mh = px.scatter(
        filtered_df,
        x="Avg_Daily_Usage_Hours",
        y="Mental_Health_Score",
        color="Affects_Academic_Performance",
        hover_data=["Academic_Level", "Country"],
        labels={
            "Avg_Daily_Usage_Hours": "Avg daily usage (hours)",
            "Mental_Health_Score": "Mental health score"
        },
        title="Daily usage vs mental health score"
    )
    st.plotly_chart(fig_mh, use_container_width=True)

st.markdown("""
**Key insight (sleep & mental health):**  
As daily usage hours increase, many students show **lower sleep hours per night**, and very high
usage groups often have **worse mental health scores** compared with moderate users.

**Conclusion:**  
Late‑night and excessive use of AI‑curated feeds may reduce sleep and negatively affect students'
emotional well‑being, even though the platforms are designed to be engaging and entertaining.
""")

# =========================================================
# 5. OVERALL IMPACT
# =========================================================
st.markdown("## 5. Students' overall perception of digital impact")

col10, col11 = st.columns(2)

with col10:
    impact_counts = filtered_df["Overall_Impact"].value_counts().reset_index()
    impact_counts.columns = ["Overall_Impact", "Count"]
    fig_impact = px.bar(
        impact_counts,
        x="Overall_Impact",
        y="Count",
        title="Overall impact of digital platforms on life",
        text="Count"
    )
    fig_impact.update_traces(textposition="outside")
    st.plotly_chart(fig_impact, use_container_width=True)

with col11:
    impact_usage = (
        filtered_df
        .groupby("Overall_Impact")["Avg_Daily_Usage_Hours"]
        .mean()
        .reset_index()
    )
    fig_impact_usage = px.bar(
        impact_usage,
        x="Overall_Impact",
        y="Avg_Daily_Usage_Hours",
        title="Average usage by overall impact group",
        labels={"Avg_Daily_Usage_Hours": "Avg daily usage (hours)"},
        text="Avg_Daily_Usage_Hours"
    )
    fig_impact_usage.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    st.plotly_chart(fig_impact_usage, use_container_width=True)

st.markdown("""
**Key insight (overall impact):**  
Students' overall perception of digital platforms ranges from positive to negative, but groups
reporting a **negative overall impact** often show higher average usage.

**Conclusion:**  
AI and digital platforms bring both benefits and drawbacks. Our data suggests that **balance** is
crucial: moderate, mindful use helps students gain value from technology without harming academics,
sleep, or mental health.
""")

# =========================================================
# SUMMARY FOOTER
# =========================================================
st.markdown("---")
st.markdown("""
**Summary:**  
Filters on the left let you focus on specific student groups.  
Use these charts to explain how **AI‑curated digital platforms** relate to students' **study performance,
sleep, mental health, and overall well‑being**.
""")




