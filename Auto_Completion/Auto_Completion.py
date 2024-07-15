from openai import OpenAI
import os
import psycopg2

# Set your OpenAI API key here
def read_context(lead_id):
    dbname = "nexa-crm-ai-dev"
    user = "avnadmin"
    password = "Digital!23"
    host = "nagarjuna-crm-dbs.postgres.database.azure.com"
    port = "5432"
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
    cur = conn.cursor()
    fetch_query = 'SELECT description FROM public.leads WHERE id=%s'
    cur.execute(fetch_query, (lead_id,))
    fetch_result = cur.fetchone()

    if fetch_result is None:
        conn.commit()
        cur.close()
        conn.close()
        return ""

    conn.commit()
    cur.close()
    conn.close()
    print("🚀 ~ fetch_result[0]:", fetch_result[0])
    return fetch_result[0]

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
    content = response.choices[0].message.content
    return content

class Auto_Completion:
    def __init__(self, request):
        self.request = request

    def whole_sentence(self):
        context = read_context(self.request.lead_id)
        next_word = get_completion(self.request.prompt, context)
        return " "+ next_word
