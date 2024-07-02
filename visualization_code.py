import plotly.express as px

# 1. Filter the dataframe
df_filtered = df[df.leadStatus.isin(['Opportunity', 'Warm Lead', 'Cold Lead', 'Visited'])]

# 2. Cluster column chart
fig1 = px.bar(df_filtered, x='createdAt', y='leadStatus', title='Cluster Column Chart for leadStatus and createdAt',
              labels={'leadStatus':'Lead Status', 'createdAt':'Created At'}, template='plotly_white')
fig1.write_html("cluster_column_chart.html")
fig1.show()

# 3. Stacked bar chart for techStack and classMode
fig2 = px.bar(df, x='techStack', y='classMode', title='Stacked Bar Chart for techStack and classMode',
              labels={'techStack':'Tech Stack', 'classMode':'Class Mode'}, template='plotly_white', barmode='stack')
fig2.write_html("stacked_bar_chart_techstack_classmode.html")
fig2.show()

# 4. Stacked bar chart for leadStatus and leadSource
fig3 = px.bar(df, x='leadStatus', y='leadSource', title='Stacked Bar Chart for leadStatus and leadSource',
              labels={'leadStatus':'Lead Status', 'leadSource':'Lead Source'}, template='plotly_white', barmode='stack')
fig3.write_html("stacked_bar_chart_leadstatus_leadsource.html")
fig3.show()

# 5. Horizontal bar chart for leadSource
fig4 = px.bar(df, y='leadSource', title='Horizontal Bar Chart for Lead Source',
              labels={'leadSource':'Lead Source'}, template='plotly_white', orientation='h')
fig4.write_html("horizontal_bar_chart.html")
fig4.show()