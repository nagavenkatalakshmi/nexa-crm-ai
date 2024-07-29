import plotly.express as px
import plotly.graph_objects as go

# Clean the data
df = df.dropna()

# Filter the data
filtered_df = df[df['leadStatus'].isin(['Opportunity', 'Warm Lead', 'Cold Lead', 'Visited'])]

# Generate cluster column chart
fig1 = px.bar(filtered_df, x="createdAt", y="leadStatus", color="leadStatus", title="Cluster Column Chart of leadStatus vs createdAt")
fig1.update_layout(template='plotly_white')
fig1.write_html("cluster_column_chart.html")
fig1.show()

# Generate stacked bar chart for techStack and classMode
fig2 = px.bar(df, x="techStack", y="classMode", color='classMode', title="Stacked Bar Chart of techStack vs classMode", barmode='stack')
fig2.update_layout(template='plotly_white')
fig2.write_html("stacked_bar_chart_techstack_classmode.html")
fig2.show()

# Generate stacked bar chart for leadStatus and leadSource
fig3 = px.bar(df, x="leadStatus", y="leadSource", color='leadSource', title="Stacked Bar Chart of leadStatus vs leadSource", barmode='stack')
fig3.update_layout(template='plotly_white')
fig3.write_html("stacked_bar_chart_leadstatus_leadsource.html")
fig3.show()

# Generate horizontal bar chart for leadSource
fig4 = go.Figure(data=[
    go.Bar(name='leadSource', y=df['leadSource'].value_counts().index, x=df['leadSource'].value_counts().values, orientation='h')
])
fig4.update_layout(title_text='Horizontal Bar Chart of leadSource', template='plotly_white')
fig4.write_html("horizontal_bar_chart.html")
fig4.show()