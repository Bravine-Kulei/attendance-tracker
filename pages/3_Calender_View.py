import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import plotly.express as px
import data_manager as data_manager

st.title("📅 Calendar View")
st.markdown("""
<style>
    .calendar-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


if "data_manager" not in st.session_state:
    st.session_state.data_manager = data_manager.DataManager()

# Date navigation
col1, col2, col3 = st.columns([2,3,2])
with col1:
    today = datetime.now()
    week_offset = st.number_input("Week Offset", min_value=-52, max_value=52, value=0, 
                                 help="Navigate between weeks")

# Calculate date range
start_of_week = today + timedelta(days=-today.weekday(), weeks=week_offset)
dates = [start_of_week + timedelta(days=i) for i in range(7)]

with col2:
    st.markdown(f"### Week of {start_of_week.strftime('%B %d, %Y')}")

# Load classes
classes_df = st.session_state.data_manager.load_classes()
if not classes_df.empty:
    classes_df['date'] = pd.to_datetime(classes_df['date'])
    classes_df['time'] = pd.to_datetime(classes_df['time'], format='%H:%M').dt.time

    # Create time slots
    time_slots = pd.date_range('06:00', '22:00', freq='30min').time

    # Create calendar grid
    fig = go.Figure()

    # Add day columns
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Add time grid
    for i, date in enumerate(dates):
        day_classes = classes_df[classes_df['date'].dt.date == date.date()]

        # Add background for the day column
        fig.add_trace(go.Scatter(
            x=[date.strftime('%Y-%m-%d')] * len(time_slots),
            y=[slot.strftime('%H:%M') for slot in time_slots],
            mode='lines',
            line=dict(color='rgba(200,200,200,0.3)', width=30),
            name=days[i],
            showlegend=False,
            hoverinfo='skip'
        ))

        if not day_classes.empty:
            for _, class_row in day_classes.iterrows():
                color = '#FFA500' if class_row['class_type'] == 'Demo' else '#2E8B57'

                # Calculate class end time
                start_time = datetime.combine(date, class_row['time'])
                end_time = start_time + timedelta(hours=float(class_row['duration']))

                # Add class block
                fig.add_trace(go.Scatter(
                    x=[date.strftime('%Y-%m-%d')],
                    y=[class_row['time'].strftime('%H:%M')],
                    mode='markers+text',
                    marker=dict(
                        symbol='square',
                        size=40,
                        color=color,
                        opacity=0.7
                    ),
                    text=f"{class_row['class_type']}<br>{class_row['time'].strftime('%H:%M')}",
                    textposition="middle center",
                    name=class_row['class_type'],
                    hovertemplate=(
                        f"<b>{class_row['class_type']} Class</b><br>" +
                        f"Time: {class_row['time'].strftime('%H:%M')}<br>" +
                        f"Duration: {class_row['duration']} hours<br>" +
                        f"<extra></extra>"
                    )
                ))

    # Update layout
    fig.update_layout(
        title="Weekly Schedule",
        height=800,
        showlegend=True,
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        xaxis=dict(
            ticktext=days,
            tickvals=[d.strftime('%Y-%m-%d') for d in dates],
            tickangle=0,
            gridcolor='rgba(200,200,200,0.2)',
            showgrid=True,
            fixedrange=True
        ),
        yaxis=dict(
            gridcolor='rgba(200,200,200,0.2)',
            showgrid=True,
            fixedrange=True
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Display calendar
    st.plotly_chart(fig, use_container_width=True)

    # Weekly summary in cards
    st.subheader("📊 Weekly Summary")
    col1, col2, col3, col4 = st.columns(4)

    week_classes = classes_df[
        (classes_df['date'].dt.date >= start_of_week.date()) & 
        (classes_df['date'].dt.date < start_of_week.date() + timedelta(days=7))
    ]

    with col1:
        total_classes = len(week_classes)
        st.metric("Total Classes", total_classes)

    with col2:
        demo_classes = len(week_classes[week_classes['class_type'] == 'Demo'])
        st.metric("Demo Classes", demo_classes)

    with col3:
        standard_classes = len(week_classes[week_classes['class_type'] == 'Standard'])
        st.metric("Standard Classes", standard_classes)

    with col4:
        total_hours = week_classes['duration'].sum()
        st.metric("Total Hours", f"{total_hours:.1f}")

    # Daily distribution
    if not week_classes.empty:
        st.subheader("📈 Daily Class Distribution")
        daily_counts = week_classes.groupby([week_classes['date'].dt.date, 'class_type']).size().unstack(fill_value=0)
        fig_daily = px.bar(daily_counts, 
                          barmode='group',
                          labels={'value': 'Number of Classes', 'date': 'Date'},
                          color_discrete_map={'Demo': '#FFA500', 'Standard': '#2E8B57'})
        fig_daily.update_layout(
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0.9)',
        )
        st.plotly_chart(fig_daily, use_container_width=True)
else:
    st.info("No classes scheduled yet. Add classes in the Class Management page to see them here.")