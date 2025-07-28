"""
Session state management utilities for Streamlit app
"""

import streamlit as st
from langchain.memory import ConversationBufferWindowMemory


def initialize_session_state():
    """Initialize all session state variables"""
    if "andy_agent" not in st.session_state:
        st.session_state.andy_agent = None

    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False

    if "current_df" not in st.session_state:
        st.session_state.current_df = None

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferWindowMemory(
            k=10, return_messages=True
        )

    if "initial_analysis_done" not in st.session_state:
        st.session_state.initial_analysis_done = False


def reset_session_for_new_data():
    """Reset session state when new data is loaded"""
    st.session_state.data_loaded = False
    st.session_state.initial_analysis_done = False
    st.session_state.conversation_history = []
    st.session_state.andy_agent = None
    st.session_state.current_df = None


def get_session_info():
    """Get current session information for debugging"""
    return {
        "data_loaded": st.session_state.get("data_loaded", False),
        "has_df": st.session_state.get("current_df") is not None,
        "has_agent": st.session_state.get("andy_agent") is not None,
        "conversation_length": len(st.session_state.get("conversation_history", [])),
        "initial_analysis_done": st.session_state.get("initial_analysis_done", False),
    }
