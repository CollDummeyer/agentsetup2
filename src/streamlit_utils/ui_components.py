"""
UI components and styling utilities for Streamlit app
"""

import streamlit as st


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown(
        """
    <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .andy-chat {
            background-color: #f0f8ff;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #1f77b4;
            margin: 1rem 0;
        }
        .user-chat {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #666;
            margin: 1rem 0;
        }
        .data-summary {
            background-color: #e8f5e8;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .andy-image {
            max-width: 100%;
            height: auto;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .andy-image svg {
            display: block;
            border-radius: 15px;
        }
        .main-header svg {
            display: inline-block;
            vertical-align: middle;
            margin-right: 10px;
            border-radius: 10px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def display_welcome_section():
    """Display the welcome section when no data is loaded"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### 👋 Welcome to Andy's Analysis Lab!
        
        I'm Andy, and I'm absolutely **obsessed** with spreadsheets and data! 🤓
        
        **Here's what I can do for you:**
        - 📈 Create beautiful interactive charts
        - 🔍 Find patterns and insights in your data  
        - 📊 Analyze trends and relationships
        - 💡 Provide actionable recommendations
        - 🎯 Answer specific questions about your data
        
        **To get started:**
        1. Upload a CSV or Excel file using the sidebar ➡️
        2. I'll give you my initial thoughts on your data
        3. Ask me anything you'd like to analyze!
        
        Let's dive into some data magic together! ✨
        """)


def display_data_preview():
    """Display data preview section with metrics"""
    if not st.session_state.data_loaded:
        return

    df = st.session_state.current_df

    st.header("📋 Your Data")
    with st.expander("📊 Data Preview", expanded=True):
        st.dataframe(df.head(10), use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", df.shape[0])
        with col2:
            st.metric("Total Columns", df.shape[1])
        with col3:
            st.metric(
                "Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB"
            )


def display_footer():
    """Display app footer"""
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🤓 Andy the Analyst | Powered by Claude Sonnet 4 & LangChain | Charts saved to data/processed/ 📊</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_intro_text():
    """Display the main intro text"""
    st.markdown(
        """
    <div style="text-align: center; margin-bottom: 2rem;">
        <h3>Your Friendly Neighborhood Data Analysis Assistant! 📊✨</h3>
        <p><em>Upload your data and let Andy find the insights!</em></p>
    </div>
    """,
        unsafe_allow_html=True,
    )
