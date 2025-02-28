import os
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
import webbrowser
import plotly.express as px

class Standard_Visualization_Service:

    def __init__(self):
        self.engine = create_engine('postgresql://avnadmin:Digital!23@nagarjuna-crm-dbs.postgres.database.azure.com:5432/nexa-crm-prod')
        self.query = 'SELECT "leadSource","techStack","classMode","feeQuoted","nextFollowUp","createdAt","leadStatus","leadStage" FROM public.leads'
        self.df = pd.read_sql(self.query, self.engine)
        columns = ['nextFollowUp', 'createdAt']
        for col in columns:
            self.df[f'{col}_date'] = self.df[col].dt.date
            self.df[f'{col}_time'] = self.df[col].dt.time
            self.df[f'{col}_day'] = self.df[col].dt.day_name()
        print(self.df)
        api_key = open(r"key.txt")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-aidev-AoVsi32RWrQI2o1sJge2T3BlbkFJRjvjp4DmbEcT6weQyxaI"))

    def generate_visualization_code(self, prompt: str):
        messages = [
            {"role": "system", "content": "You are a Visualizations generate tool based on data provided you have to generate relative visualizations."},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content.strip()

    def process_visualization_code(self, prompt: str, file_name='visualization_code.py'):
        visualization_code = self.generate_visualization_code(prompt)
        code_lines = []
        in_code_block = False

        for line in visualization_code.split('\n'):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            elif in_code_block:
                code_lines.append(line)

        # Combine the extracted code lines into a single string
        extracted_code = '\n'.join(code_lines)

        # Save the extracted code to a file
        with open(file_name, 'w') as file:
            file.write(extracted_code)

        # Execute the extracted code in a context where df is defined
        exec(extracted_code, {'df': self.df, 'px': px, 'go': go})
    def open_html_file_one(self, file_path):
        exact_file_1 = webbrowser.open('file://' + os.path.realpath(file_path))
        return exact_file_1

    def open_html_file_two(self, file_path):
        exact_file_2 = webbrowser.open('file://' + os.path.realpath(file_path))
        return exact_file_2

    def open_html_file_three(self, file_path):
        exact_file_3 = webbrowser.open('file://' + os.path.realpath(file_path))
        return exact_file_3

    def open_html_file_four(self, file_path):
        exact_file_4 = webbrowser.open('file://' + os.path.realpath(file_path))
        return exact_file_4

prompt = """
You have a dataset df with columns (Note- don't use any csv we already have database use that database df).
    1. Before visualization make sure data is clean
    2. Give me stacked bar chart for leadStatus and createdAt column using Plotly for dynamic visualization.
    3. Display continous Stacked bar chart for techStack and classMode using Plotly for dynamic visualization.
    4. Create a mosaic plot (using treemap) for leadStatus and leadSource using Plotly for dynamic visualization.
    5. Need a pie chart for techStack to count the number of leads using Plotly for dynamic visualization.
    
Ensure each plot has titles, labels, colors, and borders to enhance clarity and aesthetics. Utilize a white template for the plots.
    Provide only code without comments or instructions.
    display in web browser
    
    Save all these dynamic visualizations as a file or supported format with the following names:
    - stacked_bar_chart_leadstatus_createdAt.html
    - Continous_stacked_bar_chart_techstack_classmode.html
    - Mosaic_plot_leadstatus_leadsource.html
    - pie_chart.html 

Display in web browser. Note: The dataset df is already defined and available for use.
"""


