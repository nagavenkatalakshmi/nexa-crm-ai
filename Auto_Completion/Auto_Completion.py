from openai import OpenAI
import os
from time import time

    
def get_completion(prompt, context, max_tokens=500):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-aidev-AoVsi32RWrQI2o1sJge2T3BlbkFJRjvjp4DmbEcT6weQyxaI"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an autocompletion tool. Please complete the prompt given below with relevant suggestions based on the reference information provided. Just give me the next sentence without user prompt."},
            {"role": "user", "content": f"Reference Information: {context}\n\nPrompt: {prompt}"}
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].message.content

class Auto_Completion:
    def __init__(self, request):
        self.request = request
   
    def whole_sentence(self):
        start_time1 = time()
        next_word = get_completion(self.request.prompt, self.request.content)
        end_time1 = time()
        response_time1 = end_time1 - start_time1
        print(f"🚀 ~ next_word: {response_time1} :", next_word)
        return " "+ next_word
