import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Data Explorer", layout="wide")

st.title("📊 Self-Service Interactive Data Explorer")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = df.select_dtypes(include=["object"]).columns

    st.sidebar.header("Filters")

    selected_num = st.sidebar.selectbox("Select Numeric Column", numeric_cols)
    selected_cat = st.sidebar.selectbox("Select Category Column", cat_cols)

    if selected_cat:
        category_values = st.sidebar.multiselect(
            "Filter Categories",
            df[selected_cat].unique(),
            default=df[selected_cat].unique()
        )
        df = df[df[selected_cat].isin(category_values)]

    st.subheader("KPI Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Count", df[selected_num].count())
    col2.metric("Mean", round(df[selected_num].mean(), 2))
    col3.metric("Max", df[selected_num].max())

    fig = px.histogram(df, x=selected_num, color=selected_cat)
    st.plotly_chart(fig, use_container_width=True)
