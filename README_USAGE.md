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

3. **Run Andy**

   ```bash
   python main.py
   ```

## 💬 How to Use Andy

### Commands Available

- `load <filepath>` - Load a CSV file for analysis
- `help` - Show available commands
- `exit` - End your session with Andy

### Example Session

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
├── main.py                 # Main application with UI loop
├── src/
│   ├── models/
│   │   └── pandas_agent.py # Andy's core analysis engine
│   ├── tools/
│   │   └── charts_and_graphs.py # Visualization tools
│   └── prompts/
│       └── system_message.py    # Andy's personality
├── data/
│   └── sample_sales_data.csv    # Sample data for testing
└── requirements.txt        # Dependencies
```

## 🔧 Technical Details

- **AI Model**: Claude Sonnet 4 via Anthropic API
- **Data Analysis**: Pandas + LangChain Experimental
- **Visualizations**: Plotly (interactive charts)
- **Memory**: LangChain ConversationBufferWindowMemory
- **UI**: Simple command-line interface

## 🎨 Andy's Capabilities

- **Data Analysis**: Comprehensive pandas-based analysis
- **Visualizations**: Interactive Plotly charts (time series, bar, pie, scatter plots)
- **Chart Saving**: All charts automatically saved to `data/processed/` folder
- **Memory**: Contextual conversation memory
- **Personality**: Enthusiastic, spreadsheet-obsessed analyst
- **File Support**: CSV files (extensible to other formats)

Have fun analyzing data with Andy! 📊✨
