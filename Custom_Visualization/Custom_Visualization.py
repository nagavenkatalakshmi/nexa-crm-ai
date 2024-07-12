from openai import OpenAI
import os
import pandas as pd
from sqlalchemy import create_engine
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse


router = APIRouter()

class VisualizationRequest(BaseModel):
    prompt: str

@router.post("/generate-visualization")
def generate_visualization(request: VisualizationRequest):
    try:
        engine = create_engine('postgresql://avnadmin:Digital!23@nagarjuna-crm-dbs.postgres.database.azure.com:5432/nexa-crm-prod')
        # Query to retrieve data
        query = 'SELECT "leadSource","techStack","classMode","feeQuoted","nextFollowUp","createdAt","leadStatus","leadStage" FROM public.leads'  
        df = pd.read_sql(query, engine)
        # Separate the datetime into date and time
        columns = ['nextFollowUp', 'createdAt']
        for col in columns:
            df[f'{col}_date'] = df[col].dt.date
            df[f'{col}_time'] = df[col].dt.time
            df[f'{col}_day'] = df[col].dt.day_name()
        #print(df)
        # Set the API key and model name for OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-aidev-AoVsi32RWrQI2o1sJge2T3BlbkFJRjvjp4DmbEcT6weQyxaI"))
        # Initialize conversation history (store only customizable prompts)
        customizable_prompts = []
        def generate_visualization_code(customizable_prompt, customizable_prompts):
            # Append new customizable prompt to the conversation history
            customizable_prompts.append(customizable_prompt.strip())  # Step to append new prompt
            # Construct messages from customizable prompts
            messages = [
                {"role": "system", "content": "You are a Visualizations generator tool based on data provided. You have to generate relative visualizations."},
            ]
            for prompt in customizable_prompts:
                messages.append({"role": "user", "content": fixed_prompt_start + prompt + fixed_prompt_end})

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=800,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            return response.choices[0].message.content.strip()
        # Fixed part of the prompt
        fixed_prompt_start = """
        You have a dataset df with columns (Note- don't use any csv we already have database use that database df).
        Before visualization make sure data is clean.
        """
        fixed_prompt_end = """
        we need only dynamic visualizations so for every visualization use plotly
        Display all visualizations with titles, display labels, colors, and add borders. Make the plots attractive with colors and a white template.
        don't show visualizations just Save all these dynamic visualizations as a file or supported format. please save the file with this name first_visualization
        Remember, the conversation history is being maintained, so consider previous interactions for generating responses. Give only the code without instructions and comments, just the Python code.
        dont use show() in code just i want to save visualizations no need to show and don't use auto_open for pio
        """

        # Customizable part of the prompt
        customizable_prompt = """
        1. Compare the techStack and classMode for this give me the visualization
        """
        #print("🚀 ~ request:", request.prompt)
        # Generate the visualization code
        visualization_code = generate_visualization_code(request.prompt, customizable_prompts)
        #print("Generated Code:\n", visualization_code)
        # Log conversation history to verify it includes the correct context
        #print("Customizable Prompts History:\n", customizable_prompts)  # Verify that all prompts are stored
        # Extract only the code part from the generated text
        code_lines = []
        in_code_block = False
        for line in visualization_code.split('\n'):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            elif in_code_block:
                code_lines.append(line)
        # Combine the extracted code lines into a single string
        extracted_code = '\n'.join(code_lines)
        #print("Extracted Code:\n", extracted_code)
        # Ensure all lines are properly terminated
        extracted_code = extracted_code.strip()
        if not extracted_code.endswith("\n"):
            extracted_code += "\n"
        # Save the extracted code to a file (optional)
        with open('visualization_codb.py', 'w') as file:
            file.write(extracted_code)
        # Execute the extracted code
        exec(extracted_code)

        file_name="first_visualization.html"
        data = HTMLResponse(content=open(file_name, 'r', encoding='utf-8').read(), status_code=200)

        return data
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)