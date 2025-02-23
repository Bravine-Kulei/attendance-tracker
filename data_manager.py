import pandas as pd
import os
from datetime import datetime
import streamlit as st

class DataManager:
    def __init__(self):
        # Initialize data files if they don't exist
        self.classes_file = 'classes.csv'
        self.schools_file = 'schools.csv'

        # Define column structures
        self.classes_columns = ['date', 'time', 'duration', 'class_type', 'school_id', 'price', 'notes']
        self.schools_columns = ['school_id', 'name', 'address', 'contact']

        # Initialize files with headers if they don't exist
        if not os.path.exists(self.classes_file):
            self._create_empty_df(self.classes_file, self.classes_columns)

        if not os.path.exists(self.schools_file):
            self._create_empty_df(self.schools_file, self.schools_columns)

    def _create_empty_df(self, file_path, columns):
        """Create an empty DataFrame with specified columns and save it to CSV."""
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

    def load_classes(self):
        """Load classes with error handling."""
        try:
            return pd.read_csv(self.classes_file)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=self.classes_columns)
        except Exception as e:
            st.error(f"Error loading classes: {str(e)}")
            return pd.DataFrame(columns=self.classes_columns)

    def load_schools(self):
        """Load schools with error handling."""
        try:
            return pd.read_csv(self.schools_file)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=self.schools_columns)
        except Exception as e:
            st.error(f"Error loading schools: {str(e)}")
            return pd.DataFrame(columns=self.schools_columns)

    def save_class(self, class_data):
        """Save class with error handling."""
        try:
            classes_df = self.load_classes()
            classes_df = pd.concat([classes_df, pd.DataFrame([class_data])], ignore_index=True)
            classes_df.to_csv(self.classes_file, index=False)
            return True
        except Exception as e:
            st.error(f"Error saving class: {str(e)}")
            return False

    def save_school(self, school_data):
        """Save school with error handling."""
        try:
            schools_df = self.load_schools()
            schools_df = pd.concat([schools_df, pd.DataFrame([school_data])], ignore_index=True)
            schools_df.to_csv(self.schools_file, index=False)
            return True
        except Exception as e:
            st.error(f"Error saving school: {str(e)}")
            return False

    def calculate_class_price(self, duration, class_type):
        """Calculate class price based on type and duration."""
        if class_type == 'Demo':
            return 400
        else:
            return 750 * float(duration)

    def get_weekly_stats(self):
        """Get weekly statistics with error handling."""
        try:
            classes_df = self.load_classes()
            if len(classes_df) == 0:
                return 0, 0  # Return total_classes and total_earnings

            current_week = datetime.now().isocalendar()[1]
            classes_df['date'] = pd.to_datetime(classes_df['date'])
            weekly_classes = classes_df[classes_df['date'].dt.isocalendar().week == current_week]

            total_classes = len(weekly_classes)
            total_earnings = weekly_classes['price'].sum()
            return total_classes, total_earnings
        except Exception as e:
            st.error(f"Error calculating weekly stats: {str(e)}")
            return 0, 0