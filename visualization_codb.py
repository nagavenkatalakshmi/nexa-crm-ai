import pandas as pd
import plotly.express as px
import plotly.io as pio

# Assuming df is already loaded in the environment
df = df.dropna(subset=['leadSource'])

lead_counts = df['leadSource'].value_counts()

fig = px.pie(lead_counts, values=lead_counts.values, names=lead_counts.index, title='Lead Source Distribution')

fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
fig.update_layout(template='plotly_white', title_x=0.5)

pio.write_html(fig, file='first_visualization.html')
