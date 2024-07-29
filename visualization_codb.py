import pandas as pd
import plotly.express as px
import plotly.io as pio

# Assuming df is your DataFrame

# Data Cleaning
df.dropna(subset=['leadStatus'], inplace=True)

# Stacked Bar Chart for leadStatus
fig = px.bar(df, 
             x='leadStatus', 
             color='leadStatus', 
             title='Lead Status Distribution',
             labels={'leadStatus': 'Lead Status'},
             template='plotly_white',
             text_auto=True)

fig.update_layout(
    barmode='stack',
    bargap=0.2,
    bargroupgap=0.1,
    title_font_size=20,
    title_font_color='black',
    title_x=0.5,
    xaxis=dict(title='Lead Status', title_font_size=16),
    yaxis=dict(title='Count', title_font_size=16),
    legend=dict(title='Lead Status', title_font_size=12),
    plot_bgcolor='white',
    showlegend=True
)

fig.update_traces(marker=dict(line=dict(width=1, color='black')))

pio.write_html(fig, file='first_visualization.html')
