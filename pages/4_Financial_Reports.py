import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.title("💰 Financial Reports")

# Load classes
classes_df = st.session_state.data_manager.load_classes()
if not classes_df.empty:
    classes_df['date'] = pd.to_datetime(classes_df['date'])

    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", min_value=classes_df['date'].min())
    with col2:
        end_date = st.date_input("End Date", max_value=classes_df['date'].max())

    # Filter data based on date range
    mask = (classes_df['date'].dt.date >= start_date) & (classes_df['date'].dt.date <= end_date)
    filtered_df = classes_df.loc[mask]

    # Financial summary
    st.subheader("Financial Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        total_earnings = filtered_df['price'].sum()
        st.metric("Total Earnings", f"ksh.{total_earnings:,.2f}")

    with col2:
        demo_earnings = filtered_df[filtered_df['class_type'] == 'Demo']['price'].sum()
        st.metric("Demo Class Earnings", f"ksh.{demo_earnings:,.2f}")

    with col3:
        standard_earnings = filtered_df[filtered_df['class_type'] == 'Standard']['price'].sum()
        st.metric("Standard Class Earnings", f"ksh.{standard_earnings:,.2f}")

    # Earnings trend
    st.subheader("Earnings Trend")
    daily_earnings = filtered_df.groupby('date')['price'].sum().reset_index()
    fig = px.line(daily_earnings, x='date', y='price',
                  title='Daily Earnings',
                  labels={'price': 'Earnings (ksh.)', 'date': 'Date'})
    st.plotly_chart(fig, use_container_width=True)

    # Class type distribution
    st.subheader("Class Type Distribution")
    class_type_counts = filtered_df['class_type'].value_counts()
    fig = px.pie(values=class_type_counts.values,
                 names=class_type_counts.index,
                 title='Class Type Distribution')
    st.plotly_chart(fig, use_container_width=True)

    # Detailed financial records
    st.subheader("Detailed Financial Records")
    st.dataframe(filtered_df[['date', 'class_type', 'duration', 'price']], use_container_width=True)

else:
    st.info("No financial data available yet. Add classes to see financial reports.")














