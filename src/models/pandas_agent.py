from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_anthropic import ChatAnthropic
from src.tools.charts_and_graphs import (
    create_time_series_chart,
    create_categorical_chart,
    create_scatter_plot,
)
from src.prompts.system_message import ANDY_SYSTEM_PROMPT
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")


def create_andy_the_analyst(df):
    """Create Andy with enhanced capabilities and personality"""

    # Additional visualization tools for Andy's arsenal
    extra_tools = [
        create_time_series_chart,
        create_categorical_chart,
        create_scatter_plot,
    ]

    # Create the agent with custom system prompt and extra tools
    agent_executor = create_pandas_dataframe_agent(
        llm=ChatAnthropic(
            model="claude-sonnet-4-20250514",
            api_key=anthropic_api_key,
            temperature=0.0,
        ),
        df=df,
        agent_type="tool-calling",
        verbose=True,  # Set to True to see Andy's thinking process
        allow_dangerous_code=True,
        extra_tools=extra_tools,
        prefix=ANDY_SYSTEM_PROMPT,  # This adds Andy's personality
        number_of_head_rows=10,  # Show more data in prompt
        max_iterations=20,  # Allow more iterations for complex analysis
    )

    return agent_executor


def ask_andy(df, question):
    """Ask Andy the Analyst a question about your data"""
    andy = create_andy_the_analyst(df)
    result = andy.invoke({"input": question})
    return result["output"]


# Example usage (commented out):
# df = pd.read_csv("your_data.csv")
# andy_says = ask_andy(df, "Analyze my data!")
# print(andy_says)
