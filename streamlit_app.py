import streamlit as st
import pandas as pd
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Import utility modules
from src.streamlit_utils.session_manager import initialize_session_state
from src.streamlit_utils.ui_components import (
    apply_custom_css,
    display_welcome_section,
    display_data_preview,
    display_footer,
    display_intro_text,
)
from src.streamlit_utils.image_utils import (
    display_andy_title,
    display_andy_main_image,
    display_andy_sidebar_image,
)
from src.streamlit_utils.data_handler import load_data_file, get_initial_analysis
from src.streamlit_utils.andy_interface import (
    ask_andy,
    display_conversation_history,
    add_to_conversation,
    get_quick_actions,
)

# Page configuration
st.set_page_config(
    page_title="🤓 Andy the Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom styling
apply_custom_css()

# Initialize session state
initialize_session_state()

# Main App Layout
display_andy_main_image()
display_andy_title()
display_intro_text()

# Sidebar for file upload and controls
with st.sidebar:
    display_andy_sidebar_image()
    st.header("📁 Data Upload")

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Upload your data file and Andy will analyze it for you!",
    )

    if uploaded_file is not None:
        if st.button("🚀 Load Data", type="primary"):
            with st.spinner("Loading data..."):
                df = load_data_file(uploaded_file)
                if df is not None:
                    st.success(
                        f"✅ Data loaded! {df.shape[0]} rows, {df.shape[1]} columns"
                    )
                    st.rerun()

    # Display data info if loaded
    if st.session_state.data_loaded:
        st.header("📊 Dataset Info")
        df = st.session_state.current_df
        st.write(f"**Rows:** {df.shape[0]}")
        st.write(f"**Columns:** {df.shape[1]}")
        st.write(f"**File:** {uploaded_file.name if uploaded_file else 'Unknown'}")

        # Show column types
        with st.expander("Column Details"):
            for col, dtype in df.dtypes.items():
                st.write(f"**{col}:** {dtype}")

# Main content area
if not st.session_state.data_loaded:
    # Welcome screen when no data is loaded
    display_welcome_section()

    # Sample data option
    if st.button("🎯 Try with Sample Sales Data", type="secondary"):
        sample_path = "data/sample_sales_data.csv"
        try:
            df = pd.read_csv(sample_path)
            st.session_state.current_df = df
            from src.models.pandas_agent import create_andy_the_analyst

            st.session_state.andy_agent = create_andy_the_analyst(df)
            st.session_state.data_loaded = True
            st.session_state.initial_analysis_done = False
            st.session_state.conversation_history = []
            st.success("✅ Sample data loaded!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error loading sample data: {str(e)}")

else:
    # Data is loaded - show the analysis interface
    display_data_preview()

    # Andy's initial analysis
    if not st.session_state.initial_analysis_done:
        st.header("🤓 Andy's Initial Analysis")

        with st.spinner("Andy is analyzing your data..."):
            initial_prompt = get_initial_analysis(st.session_state.current_df)
            initial_response = ask_andy(initial_prompt)

            st.markdown('<div class="andy-chat">', unsafe_allow_html=True)
            st.markdown(f"**🤓 Andy:** {initial_response}")
            st.markdown("</div>", unsafe_allow_html=True)

            # Add to conversation history
            add_to_conversation("andy", initial_response)
            st.session_state.initial_analysis_done = True

    # Chat interface
    st.header("💬 Chat with Andy")

    # Display conversation history
    display_conversation_history()

    # User input
    user_question = st.text_input(
        "Ask Andy anything about your data:",
        placeholder="e.g., 'Show me sales trends over time' or 'What are the top categories?'",
        key="user_input",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("💬 Ask Andy", type="primary"):
            if user_question.strip():
                # Add user question to history
                add_to_conversation("user", user_question)

                # Get Andy's response
                with st.spinner("Andy is thinking..."):
                    response = ask_andy(user_question)
                    add_to_conversation("andy", response)

                st.rerun()

    # Quick action buttons
    st.header("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)

    quick_actions = get_quick_actions()

    for i, (button_text, question) in enumerate(quick_actions):
        with [col1, col2, col3, col4][i]:
            if st.button(button_text, key=f"quick_{i}"):
                # Add to conversation
                add_to_conversation("user", question)

                with st.spinner("Andy is analyzing..."):
                    response = ask_andy(question)
                    add_to_conversation("andy", response)

                st.rerun()

# Footer
display_footer()
