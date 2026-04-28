import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Social Media Impact on Students' Digital Life")

df = pd.read_csv("social_media_impact_on_life.csv") 

st.subheader("Data preview")
st.write(df.head())

# Example: usage vs academic performance
st.subheader("Average daily usage by academic impact")
usage_perf = df.groupby("Affects_Academic_Performance")["Avg_Daily_Usage_Hours"].mean().reset_index()
fig1 = px.bar(usage_perf,
              x="Affects_Academic_Performance",
              y="Avg_Daily_Usage_Hours",
              labels={"Avg_Daily_Usage_Hours": "Avg daily usage (hours)",
                      "Affects_Academic_Performance": "Affects academic performance"},
              title="Heavy users more often report academic impact")
st.plotly_chart(fig1)

# Example: usage vs sleep
st.subheader("Daily usage vs sleep hours")
fig2 = px.scatter(df,
                  x="Avg_Daily_Usage_Hours",
                  y="Sleep_Hours_Per_Night",
                  trendline="ols",
                  labels={"Avg_Daily_Usage_Hours": "Daily usage (hours)",
                          "Sleep_Hours_Per_Night": "Sleep hours per night"},
                  title="More screen time linked to less sleep?")
st.plotly_chart(fig2)

