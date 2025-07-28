import os
import pandas as pd
from dotenv import load_dotenv
from langchain.memory import ConversationBufferWindowMemory
from src.models.pandas_agent import create_andy_the_analyst
import sys
from pathlib import Path

# Load environment variables
load_dotenv()


class AndySession:
    """Andy the Analyst session manager with memory"""

    def __init__(self):
        self.memory = ConversationBufferWindowMemory(
            k=10,  # Remember last 10 exchanges
            return_messages=True,
        )
        self.current_df = None
        self.andy_agent = None
        self.data_loaded = False

    def load_data(self, file_path: str) -> bool:
        """Load CSV data for analysis"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                return False

            self.current_df = pd.read_csv(file_path)
            self.andy_agent = create_andy_the_analyst(self.current_df)
            self.data_loaded = True

            print(f"✅ Data loaded successfully!")
            print(f"📊 Dataset shape: {self.current_df.shape}")
            print(f"📝 Columns: {', '.join(self.current_df.columns.tolist())}")
            return True

        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return False

    def ask_andy(self, question: str) -> str:
        """Ask Andy a question with memory context"""
        if not self.data_loaded:
            return "🤔 I need some data to analyze first! Please load a CSV file using the 'load' command."

        try:
            # Get conversation history for context
            history = self.memory.load_memory_variables({})

            # Add context from memory if available
            context_prompt = ""
            if history.get("history"):
                context_prompt = "\n\nPrevious conversation context:\n" + str(
                    history["history"][-6:]
                )  # Last 3 exchanges

            full_question = question + context_prompt

            # Get Andy's response
            result = self.andy_agent.invoke({"input": full_question})
            response = result.get(
                "output", "🤷‍♂️ Sorry, I couldn't process that question."
            )

            # Save to memory
            self.memory.save_context({"input": question}, {"output": response})

            return response

        except Exception as e:
            return f"🚨 Oops! I encountered an error: {str(e)}"


def print_welcome():
    """Print welcome message"""
    print("🤓" + "=" * 60 + "🤓")
    print("     🎉 WELCOME TO ANDY THE ANALYST! 🎉")
    print("=" * 64)
    print("👋 Hey there! I'm Andy, your friendly neighborhood data analyst!")
    print("I'm absolutely obsessed with spreadsheets, charts, and finding")
    print("amazing insights in your data! 📊✨")
    print()
    print("💡 COMMANDS:")
    print("  • 'load <filepath>' - Load a CSV file for analysis")
    print("  • 'help' - Show available commands")
    print("  • 'exit' - Say goodbye (I'll miss you! 😢)")
    print("  • Ask me anything about your data once loaded!")
    print()
    print("🚀 Let's dive into some data magic together!")
    print("=" * 64)


def print_help():
    """Print help information"""
    print("\n📋 ANDY'S HELP MENU:")
    print("=" * 40)
    print("🔸 load <filepath>     - Load a CSV file")
    print("                       Example: load data.csv")
    print("🔸 help               - Show this help menu")
    print("🔸 exit               - End our session")
    print("🔸 <question>         - Ask me anything about your data!")
    print()
    print("💡 Example questions:")
    print("   • 'Analyze my spending patterns'")
    print("   • 'Create a chart showing trends over time'")
    print("   • 'What are the top categories by amount?'")
    print("   • 'Show me any interesting insights!'")
    print("=" * 40)


def main():
    """Main application loop"""
    print_welcome()

    # Initialize Andy session
    session = AndySession()

    print("\n🤔 How can I help you today?")

    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()

            # Handle empty input
            if not user_input:
                continue

            # Handle exit
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                print("\n🤓 Andy: Thanks for letting me analyze with you!")
                print("📊 Remember, there's always more insights to discover!")
                print("👋 See you next time! Keep those spreadsheets organized! ✨")
                break

            # Handle help
            elif user_input.lower() == "help":
                print_help()
                continue

            # Handle load command
            elif user_input.lower().startswith("load "):
                filepath = user_input[5:].strip()
                if filepath:
                    print(f"\n🔄 Loading data from: {filepath}")
                    success = session.load_data(filepath)
                    if success:
                        print(
                            "\n🤓 Andy: Fantastic! I've got your data loaded and ready to go!"
                        )
                        print(
                            "🎯 Ask me anything - I'm excited to dig into this dataset!"
                        )
                else:
                    print("❌ Please specify a file path. Example: load data.csv")
                continue

            # Handle regular questions
            else:
                print("\n🤓 Andy: Let me analyze that for you...")
                response = session.ask_andy(user_input)
                print(f"\n🤓 Andy: {response}")

        except KeyboardInterrupt:
            print("\n\n🤓 Andy: Caught you trying to escape! 😄")
            print("👋 Thanks for the analysis session. Until next time!")
            break
        except Exception as e:
            print(f"\n🚨 Unexpected error: {str(e)}")
            print("🤓 Andy: Don't worry, I'm still here to help!")


if __name__ == "__main__":
    main()
