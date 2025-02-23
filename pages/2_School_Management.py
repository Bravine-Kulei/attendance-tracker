import streamlit as st
import pandas as pd
import data_manager as data_manager 

if "data_manager" not in st.session_state:
    st.session_state.data_manager = data_manager.DataManager()

st.title("🏫 School Management")

# School input form
st.subheader("Add New School")

with st.form("school_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        school_name = st.text_input("School Name")
        address = st.text_area("Address")
        
    with col2:
        contact = st.text_input("Contact Information")
        
    submit = st.form_submit_button("Add School")
    
    if submit:
        if school_name:
            school_data = {
                'school_id': pd.util.hash_pandas_object(pd.Series([school_name])).iloc[0],
                'name': school_name,
                'address': address,
                'contact': contact
            }
            
            st.session_state.data_manager.save_school(school_data)
            st.success("School added successfully!")
        else:
            st.error("School name is required!")

# Display existing schools
st.subheader("Existing Schools")
schools_df = st.session_state.data_manager.load_schools()

if not schools_df.empty:
    st.dataframe(schools_df, use_container_width=True)
else:
    st.info("No schools added yet.")
