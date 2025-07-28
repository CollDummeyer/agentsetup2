# Custom tools for Andy - Plotly visualization specialists

from langchain_core.tools import tool
import os
from datetime import datetime

# Chart save directory (all charts will be saved here):
# /Users/colleendummeyer/Desktop/ANDY_THE_ANALYST/agentsetup2/data/processed


@tool
def create_time_series_chart(
    df_name: str, date_column: str, value_column: str, title: str = "Time Series"
) -> str:
    """Create an interactive time series chart using Plotly. Use this when you need to show trends over time."""
    code = f"""
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# Ensure date column is datetime
{df_name}['{date_column}'] = pd.to_datetime({df_name}['{date_column}'])

fig = px.line({df_name}, x='{date_column}', y='{value_column}', 
              title='{title}',
              labels={{'{date_column}': 'Date', '{value_column}': 'Value'}})

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='{value_column}',
    hovermode='x unified'
)

# Save the chart
save_dir = "/Users/colleendummeyer/Desktop/ANDY_THE_ANALYST/agentsetup2/data/processed"
os.makedirs(save_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
clean_title = "".join(c for c in "{title}" if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')[:30]
filename = f"time_series_{{clean_title}}_{{timestamp}}.html" if clean_title else f"time_series_{{timestamp}}.html"
filepath = os.path.join(save_dir, filename)
fig.write_html(filepath)

fig.show()
print(f"✨ Time series chart created and saved to: {{filepath}}")
"""
    return f"Created time series chart code. Execute this:\n{code}"


@tool
def create_categorical_chart(
    df_name: str, category_column: str, value_column: str, chart_type: str = "bar"
) -> str:
    """Create categorical charts (bar, pie, treemap) using Plotly. Chart types: 'bar', 'pie', 'treemap'."""

    chart_code = {
        "bar": f"""
fig = px.bar({df_name}, x='{category_column}', y='{value_column}',
             title='Distribution by {category_column}')
fig.update_layout(xaxis_tickangle=-45)
""",
        "pie": f"""
fig = px.pie({df_name}, names='{category_column}', values='{value_column}',
             title='Distribution by {category_column}')
""",
        "treemap": f"""
fig = px.treemap({df_name}, path=['{category_column}'], values='{value_column}',
                 title='Treemap of {category_column}')
""",
    }

    code = f"""
import plotly.express as px
import os
from datetime import datetime

# Group data if needed
chart_data = {df_name}.groupby('{category_column}')['{value_column}'].sum().reset_index()

{chart_code.get(chart_type, chart_code["bar"])}

# Save the chart
save_dir = "/Users/colleendummeyer/Desktop/ANDY_THE_ANALYST/agentsetup2/data/processed"
os.makedirs(save_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
clean_category = "".join(c for c in "{category_column}" if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')[:30]
filename = f"{chart_type}_{{clean_category}}_{{timestamp}}.html"
filepath = os.path.join(save_dir, filename)
fig.write_html(filepath)

fig.show()
print(f"📊 {chart_type.title()} chart created and saved to: {{filepath}}")
"""

    return f"Created {chart_type} chart code. Execute this:\n{code}"


@tool
def create_scatter_plot(
    df_name: str,
    x_column: str,
    y_column: str,
    color_column: str = None,
    title: str = "Scatter Plot",
) -> str:
    """Create an interactive scatter plot to show relationships between variables."""

    color_param = f", color='{color_column}'" if color_column else ""

    code = f"""
import plotly.express as px
import os
from datetime import datetime

fig = px.scatter({df_name}, x='{x_column}', y='{y_column}'{color_param},
                 title='{title}',
                 hover_data=[col for col in {df_name}.columns if col not in ['{x_column}', '{y_column}']])

fig.update_layout(
    xaxis_title='{x_column}',
    yaxis_title='{y_column}'
)

# Save the chart
save_dir = "/Users/colleendummeyer/Desktop/ANDY_THE_ANALYST/agentsetup2/data/processed"
os.makedirs(save_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
clean_title = "".join(c for c in "{title}" if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')[:30]
filename = f"scatter_{{clean_title}}_{{timestamp}}.html" if clean_title else f"scatter_{{timestamp}}.html"
filepath = os.path.join(save_dir, filename)
fig.write_html(filepath)

fig.show()
print(f"🎯 Scatter plot created and saved to: {{filepath}}")
"""

    return f"Created scatter plot code. Execute this:\n{code}"
