import streamlit as st
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain.memory import ConversationBufferWindowMemory
from src.models.pandas_agent import create_andy_the_analyst
import plotly.express as px
import plotly.graph_objects as go

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🤓 Andy the Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
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
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "andy_agent" not in st.session_state:
    st.session_state.andy_agent = None
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "current_df" not in st.session_state:
    st.session_state.current_df = None
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=10, return_messages=True)
if "initial_analysis_done" not in st.session_state:
    st.session_state.initial_analysis_done = False


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


def ask_andy(question):
    """Ask Andy a question and get response with memory"""
    if not st.session_state.data_loaded:
        return (
            "🤔 I need some data to analyze first! Please upload a CSV or Excel file."
        )

    try:
        # Get conversation history for context
        history = st.session_state.memory.load_memory_variables({})

        # Add context from memory if available
        context_prompt = ""
        if history.get("history"):
            context_prompt = "\n\nPrevious conversation context:\n" + str(
                history["history"][-6:]
            )

        full_question = question + context_prompt

        # Get Andy's response
        result = st.session_state.andy_agent.invoke({"input": full_question})
        response = result.get("output", "🤷‍♂️ Sorry, I couldn't process that question.")

        # Save to memory
        st.session_state.memory.save_context({"input": question}, {"output": response})

        return response

    except Exception as e:
        return f"🚨 Oops! I encountered an error: {str(e)}"


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


# Main App Layout
st.markdown('<h1 class="main-header">🤓 Andy the Analyst</h1>', unsafe_allow_html=True)

st.markdown(
    """
<div style="text-align: center; margin-bottom: 2rem;">
    <h3>Your Friendly Neighborhood Data Analysis Assistant! 📊✨</h3>
    <p><em>Upload your data and let Andy find the insights!</em></p>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar for file upload and controls
with st.sidebar:
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

        # Sample data option
        if st.button("🎯 Try with Sample Sales Data", type="secondary"):
            sample_path = "data/sample_sales_data.csv"
            if os.path.exists(sample_path):
                try:
                    df = pd.read_csv(sample_path)
                    st.session_state.current_df = df
                    st.session_state.andy_agent = create_andy_the_analyst(df)
                    st.session_state.data_loaded = True
                    st.session_state.initial_analysis_done = False
                    st.session_state.conversation_history = []
                    st.success("✅ Sample data loaded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error loading sample data: {str(e)}")
            else:
                st.error("❌ Sample data file not found")

else:
    # Data is loaded - show the analysis interface
    df = st.session_state.current_df

    # Data preview section
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

    # Andy's initial analysis
    if not st.session_state.initial_analysis_done:
        st.header("🤓 Andy's Initial Analysis")

        with st.spinner("Andy is analyzing your data..."):
            initial_prompt = get_initial_analysis(df)
            initial_response = ask_andy(initial_prompt)

            st.markdown('<div class="andy-chat">', unsafe_allow_html=True)
            st.markdown(f"**🤓 Andy:** {initial_response}")
            st.markdown("</div>", unsafe_allow_html=True)

            # Add to conversation history
            st.session_state.conversation_history.append(
                {
                    "role": "andy",
                    "content": initial_response,
                    "timestamp": datetime.now(),
                }
            )

            st.session_state.initial_analysis_done = True

    # Chat interface
    st.header("💬 Chat with Andy")

    # Display conversation history
    for message in st.session_state.conversation_history:
        if message["role"] == "andy":
            st.markdown('<div class="andy-chat">', unsafe_allow_html=True)
            st.markdown(f"**🤓 Andy:** {message['content']}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="user-chat">', unsafe_allow_html=True)
            st.markdown(f"**👤 You:** {message['content']}")
            st.markdown("</div>", unsafe_allow_html=True)

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
                st.session_state.conversation_history.append(
                    {
                        "role": "user",
                        "content": user_question,
                        "timestamp": datetime.now(),
                    }
                )

                # Get Andy's response
                with st.spinner("Andy is thinking..."):
                    response = ask_andy(user_question)

                    # Add Andy's response to history
                    st.session_state.conversation_history.append(
                        {
                            "role": "andy",
                            "content": response,
                            "timestamp": datetime.now(),
                        }
                    )

                st.rerun()

    # Quick action buttons
    st.header("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)

    quick_actions = [
        ("📈 Show Trends", "Create visualizations showing trends in this data"),
        ("🔍 Find Insights", "What are the most interesting insights in this data?"),
        ("📊 Summary Stats", "Give me a comprehensive statistical summary"),
        ("🎯 Top Values", "Show me the top values in each important column"),
    ]

    for i, (button_text, question) in enumerate(quick_actions):
        with [col1, col2, col3, col4][i]:
            if st.button(button_text, key=f"quick_{i}"):
                # Add to conversation
                st.session_state.conversation_history.append(
                    {"role": "user", "content": question, "timestamp": datetime.now()}
                )

                with st.spinner("Andy is analyzing..."):
                    response = ask_andy(question)
                    st.session_state.conversation_history.append(
                        {
                            "role": "andy",
                            "content": response,
                            "timestamp": datetime.now(),
                        }
                    )

                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🤓 Andy the Analyst | Powered by Claude Sonnet 4 & LangChain | Charts saved to data/processed/ 📊</p>
</div>
""",
    unsafe_allow_html=True,
)
