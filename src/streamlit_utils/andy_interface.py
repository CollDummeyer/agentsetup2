"""
Andy interaction utilities for Streamlit app
"""

import streamlit as st


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
            )  # Last 3 exchanges

        full_question = question + context_prompt

        # Get Andy's response
        result = st.session_state.andy_agent.invoke({"input": full_question})
        response = result.get("output", "🤷‍♂️ Sorry, I couldn't process that question.")

        # Save to memory
        st.session_state.memory.save_context({"input": question}, {"output": response})

        return response

    except Exception as e:
        return f"🚨 Oops! I encountered an error: {str(e)}"


def display_conversation_history():
    """Display the conversation history with proper styling"""
    for message in st.session_state.conversation_history:
        if message["role"] == "andy":
            st.markdown('<div class="andy-chat">', unsafe_allow_html=True)
            st.markdown(f"**🤓 Andy:** {message['content']}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="user-chat">', unsafe_allow_html=True)
            st.markdown(f"**👤 You:** {message['content']}")
            st.markdown("</div>", unsafe_allow_html=True)


def add_to_conversation(role, content):
    """Add a message to the conversation history"""
    from datetime import datetime

    st.session_state.conversation_history.append(
        {"role": role, "content": content, "timestamp": datetime.now()}
    )


def get_quick_actions():
    """Get the list of quick action buttons and their corresponding questions"""
    return [
        ("📈 Show Trends", "Create visualizations showing trends in this data"),
        ("🔍 Find Insights", "What are the most interesting insights in this data?"),
        ("📊 Summary Stats", "Give me a comprehensive statistical summary"),
        ("🎯 Top Values", "Show me the top values in each important column"),
    ]
