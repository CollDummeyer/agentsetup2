"""
Data handling utilities for Streamlit app
"""

import streamlit as st
import pandas as pd
from src.models.pandas_agent import create_andy_the_analyst


def load_data_file(uploaded_file):
    """Load uploaded CSV or Excel file"""
    try:
        # Determine file type and load accordingly
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("❌ Please upload a CSV or Excel file (.csv, .xlsx, .xls)")
            return None

        # Update session state
        st.session_state.current_df = df
        st.session_state.andy_agent = create_andy_the_analyst(df)
        st.session_state.data_loaded = True
        st.session_state.initial_analysis_done = False
        st.session_state.conversation_history = []

        return df

    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        return None


def get_initial_analysis(df):
    """Get Andy's initial reaction and analysis of the uploaded data"""

    # Basic data info
    shape_info = f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns"
    column_info = f"Columns: {', '.join(df.columns.tolist())}"

    # Sample data preview
    data_types = df.dtypes.to_dict()
    numeric_cols = [
        col for col, dtype in data_types.items() if pd.api.types.is_numeric_dtype(dtype)
    ]
    date_cols = [
        col
        for col in df.columns
        if any(
            keyword in col.lower()
            for keyword in ["date", "time", "day", "month", "year"]
        )
    ]

    # Create initial analysis prompt
    initial_prompt = f"""
    I just received a new dataset to analyze! Here's what I can see:
    
    📊 DATASET OVERVIEW:
    - {shape_info}
    - {column_info}
    - Numeric columns: {numeric_cols if numeric_cols else "None detected"}
    - Potential date columns: {date_cols if date_cols else "None detected"}
    
    Based on this initial look at the data, please:
    1. Tell me what you think this dataset represents (business type, domain, purpose)
    2. Identify the most interesting columns for analysis
    3. Ask me 2-3 specific questions about what I'd like to analyze or explore
    4. Suggest some initial visualizations that would be helpful
    
    Here's a sample of the data:
    {df.head(3).to_string()}
    
    Be enthusiastic and use your Andy personality! 🤓
    """

    return initial_prompt
