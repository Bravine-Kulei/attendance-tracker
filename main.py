import streamlit as st
from data_manager import DataManager
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="STEM Educator Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()

# Sidebar with navigation instructions
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/teacher.png", width=100)
    st.title("Navigation")
    st.info("""
    👆 Use the pages above to:
    - 📚 Manage your classes
    - 🏫 Add/edit schools
    - 📅 View your calendar
    - 💰 Track finances
    """)

# Main dashboard
st.title("🎓 STEM Educator Dashboard")
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
    }
</style>
""", unsafe_allow_html=True)

# Weekly Overview Section
st.subheader("📊 Weekly Overview")
weekly_classes, weekly_earnings = st.session_state.data_manager.get_weekly_stats()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Classes This Week",
        weekly_classes,
        help="Total number of classes scheduled for this week"
    )

with col2:
    st.metric(
        "Weekly Earnings",
        f"ksh.{weekly_earnings:,.2f}",
        help="Total earnings from all classes this week"
    )

with col3:
    # Calculate average earnings per class
    avg_earnings = weekly_earnings / weekly_classes if weekly_classes > 0 else 0
    st.metric(
        "Average per Class",
        f"ksh.{avg_earnings:,.2f}",
        help="Average earnings per class this week"
    )

# Recent Activity
st.subheader("📚 Recent Activity")
classes_df = st.session_state.data_manager.load_classes()

if not classes_df.empty:
    # Convert date to datetime
    classes_df['date'] = pd.to_datetime(classes_df['date'])

    # Last 7 days statistics
    today = datetime.now()
    last_week = today - timedelta(days=7)
    recent_classes = classes_df[classes_df['date'] >= last_week]

    # Create activity chart
    fig = px.bar(
        recent_classes,
        x='date',
        y='price',
        color='class_type',
        title='Last 7 Days Activity',
        labels={'price': 'Earnings (ksh.)', 'date': 'Date', 'class_type': 'Class Type'},
        color_discrete_map={'Demo': '#FFA500', 'Standard': '#2E8B57'}
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=0, r=0, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Recent classes table
    st.subheader("📋 Recent Classes")
    recent_df = classes_df.sort_values('date', ascending=False).head(5)
    recent_df['date'] = recent_df['date'].dt.strftime('%Y-%m-%d')
    st.dataframe(
        recent_df[['date', 'time', 'class_type', 'duration', 'price']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("👋 Welcome! Start by adding your first class in the Class Management page.")

# Quick tips
with st.expander("💡 Quick Tips"):
    st.markdown("""
    - **Demo Classes** are fixed at ksh.400
    - **Standard Classes** are charged at ksh.750 per hour
    - Use the **Calendar View** to plan your schedule
    - Track your earnings in the **Financial Reports**
    """)