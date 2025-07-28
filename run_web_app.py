#!/usr/bin/env python3
"""
Launch script for Andy the Analyst Web App
"""

import subprocess
import sys
import os


def main():
    """Launch the Streamlit web app"""
    print("🚀 Starting Andy the Analyst Web App...")
    print("📊 Opening in your default browser...")
    print("💡 Use Ctrl+C to stop the server")
    print("-" * 50)

    # Ensure we're in the right directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        # Launch Streamlit
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "streamlit_app.py",
                "--server.port",
                "8501",
                "--server.headless",
                "false",
            ]
        )
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Andy the Analyst!")
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        print("💡 Make sure you have streamlit installed: pip install streamlit")


if __name__ == "__main__":
    main()
