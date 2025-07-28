# 🤓 Andy the Analyst - Usage Guide

Welcome to Andy the Analyst! Your friendly, spreadsheet-obsessed data analysis companion.

## 🚀 Quick Start

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**
   Create a `.env` file with your Anthropic API key:

   ```python:
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. **Choose Your Interface**

   **🌐 Web Interface (Recommended):**
   ```bash
   python run_web_app.py
   # OR
   streamlit run streamlit_app.py
   ```

   **💻 Command Line Interface:**
   ```bash
   python main.py
   ```

## 💬 How to Use Andy

### 🌐 Web Interface Features
- **File Upload**: Drag & drop CSV or Excel files
- **Instant Preview**: See your data immediately
- **Andy's First Impression**: Automatic initial analysis and questions
- **Interactive Chat**: Continuous conversation with memory
- **Quick Actions**: One-click analysis buttons
- **Visual Interface**: Beautiful, user-friendly design

### 💻 Command Line Features
- `load <filepath>` - Load a CSV file for analysis
- `help` - Show available commands
- `exit` - End your session with Andy
- Continuous loop conversation
- Memory within session

### Example Web Session
1. **Upload your file** using the sidebar
2. **Andy's reaction**: "Holy mackerel! This looks like sales data..."
3. **Andy asks**: "What time period interests you most?"
4. **You respond**: "Show me monthly trends"
5. **Andy creates** beautiful interactive charts
6. **Continue chatting** with context memory

### Example CLI Session

```python:
👤 You: load data/sample_sales_data.csv
🤓 Andy: Fantastic! I've got your data loaded and ready to go!

👤 You: What are the top selling categories?
🤓 Andy: [Andy analyzes and creates visualizations]

👤 You: Show me sales trends over time
🤓 Andy: [Andy creates time series charts]

👤 You: exit
🤓 Andy: Thanks for letting me analyze with you!
```

## 🧠 Memory Features

Andy remembers your conversation within each session:

- Recalls previous questions and context
- Builds on earlier analysis
- Maintains conversation flow
- Remembers data insights from earlier in the session

## 📊 Sample Data

Try Andy with the included sample data:

```python
load data/sample_sales_data.csv
```

## 💾 Chart Storage

All charts and visualizations Andy creates are automatically saved as interactive HTML files to:
```
/Users/colleendummeyer/Desktop/ANDY_THE_ANALYST/agentsetup2/data/processed/
```

Chart files are named with:
- Chart type (time_series, bar, pie, scatter)
- Descriptive title (cleaned and shortened)
- Timestamp for uniqueness
- Example: `time_series_Sales_Trends_20241225_143052.html`

## 🎯 Example Questions to Ask Andy

- "Analyze the sales patterns and create visualizations"
- "What are the top performing products?"
- "Show me regional sales distribution"
- "Create a time series chart of sales over time"
- "Which categories generate the most revenue?"
- "Find any interesting trends or outliers"

## 📁 File Structure

```md:
agentsetup2/
├── streamlit_app.py        # 🌐 Web interface (recommended)
├── run_web_app.py          # Web app launcher script
├── main.py                 # 💻 Command line interface
├── src/
│   ├── models/
│   │   └── pandas_agent.py # Andy's core analysis engine
│   ├── tools/
│   │   └── charts_and_graphs.py # Visualization tools
│   └── prompts/
│       └── system_message.py    # Andy's personality
├── data/
│   ├── sample_sales_data.csv    # Sample data for testing
│   └── processed/          # Auto-saved charts location
└── requirements.txt        # Dependencies
```

## 🔧 Technical Details

- **AI Model**: Claude Sonnet 4 via Anthropic API
- **Data Analysis**: Pandas + LangChain Experimental
- **Visualizations**: Plotly (interactive charts)
- **Memory**: LangChain ConversationBufferWindowMemory
- **Web UI**: Streamlit (modern, interactive interface)
- **CLI**: Simple command-line interface
- **File Support**: CSV, Excel (.xlsx, .xls)

## 🎨 Andy's Capabilities

- **Data Analysis**: Comprehensive pandas-based analysis
- **Visualizations**: Interactive Plotly charts (time series, bar, pie, scatter plots)
- **Chart Saving**: All charts automatically saved to `data/processed/` folder
- **Memory**: Contextual conversation memory
- **Personality**: Enthusiastic, spreadsheet-obsessed analyst
- **File Support**: CSV and Excel files (.csv, .xlsx, .xls)
- **Web Interface**: Modern, user-friendly Streamlit frontend
- **Initial Analysis**: Andy automatically reviews and summarizes your data

Have fun analyzing data with Andy! 📊✨
