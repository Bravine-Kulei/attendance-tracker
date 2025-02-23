import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import data_manager as data_manager 

st.set_page_config(page_title="Class Management", page_icon="📚", layout="wide")

if "data_manager" not in st.session_state:
    st.session_state.data_manager = data_manager.DataManager()

# Page header with description
st.title("📚 Class Management")
st.markdown("""
Manage your classes efficiently. Add new classes, view existing ones, and keep track of your schedule.
""")

# Initialize tabs for better organization
tab1, tab2 = st.tabs(["Add New Class", "View Classes"])

with tab1:
    st.subheader("Add New Class")

    with st.form("class_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input(
                "Class Date",
                min_value=datetime.today(),
                help="Select the date for the class"
            )
            time = st.time_input(
                "Class Time",
                help="Select the start time of the class"
            )
            duration = st.number_input(
                "Duration (hours)",
                min_value=0.5,
                max_value=8.0,
                value=1.0,
                step=0.5,
                help="Enter the duration of the class in hours"
            )

        with col2:
            class_type = st.selectbox(
                "Class Type",
                ["Standard", "Demo"],
                help="Demo classes are fixed at ksh.400. Standard classes are ksh.750 per hour"
            )
            schools_df = st.session_state.data_manager.load_schools()
            school_options = schools_df['name'].tolist() if not schools_df.empty else ['No schools added']
            school = st.selectbox(
                "School",
                school_options,
                help="Select the school for this class"
            )
            notes = st.text_area(
                "Notes",
                placeholder="Add any additional notes about the class...",
                height=100
            )

        # Calculate and display preview
        price = st.session_state.data_manager.calculate_class_price(duration, class_type)
        st.info(f"💰 Estimated earnings for this class: ksh.{price:,.2f}")

        submit = st.form_submit_button("Add Class", use_container_width=True)

        if submit:
            if school == 'No schools added':
                st.error("Please add a school first in the School Management page!")
            else:
                school_id = schools_df[schools_df['name'] == school]['school_id'].iloc[0]

                class_data = {
                    'date': date.strftime('%Y-%m-%d'),
                    'time': time.strftime('%H:%M'),
                    'duration': duration,
                    'class_type': class_type,
                    'school_id': school_id,
                    'price': price,
                    'notes': notes
                }

                st.session_state.data_manager.save_class(class_data)
                st.success("✅ Class added successfully!")
                st.balloons()

with tab2:
    st.subheader("Existing Classes")

    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        filter_date = st.date_input(
            "Filter by date",
            value=(datetime.today() - timedelta(days=30), datetime.today()),
            help="Select date range to filter classes"
        )
    with col2:
        filter_type = st.multiselect(
            "Filter by class type",
            ["Standard", "Demo"],
            default=["Standard", "Demo"],
            help="Select class types to display"
        )

    # Load and filter classes
    classes_df = st.session_state.data_manager.load_classes()
    if not classes_df.empty:
        classes_df['date'] = pd.to_datetime(classes_df['date'])
        mask = (
            (classes_df['date'].dt.date >= filter_date[0]) &
            (classes_df['date'].dt.date <= filter_date[1]) &
            (classes_df['class_type'].isin(filter_type))
        )
        filtered_df = classes_df.loc[mask].sort_values('date', ascending=False)

        if not filtered_df.empty:
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "price": st.column_config.NumberColumn(
                        "Price",
                        format="ksh.%.2f"
                    ),
                    "date": st.column_config.DateColumn(
                        "Date",
                        format="YYYY-MM-DD"
                    ),
                    "time": "Time",
                    "duration": "Duration (hours)",
                    "class_type": "Type",
                    "notes": "Notes"
                }
            )

            # Summary statistics
            st.subheader("Summary")
            total_classes = len(filtered_df)
            total_earnings = filtered_df['price'].sum()
            avg_duration = filtered_df['duration'].mean()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Classes", total_classes)
            col2.metric("Total Earnings", f"ksh.{total_earnings:,.2f}")
            col3.metric("Average Duration", f"{avg_duration:.1f} hours")
        else:
            st.info("No classes found for the selected filters.")
    else:
        st.info("No classes recorded yet.")