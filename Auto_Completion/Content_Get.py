
import psycopg2


# Set your OpenAI API key here
def read_context(lead_id):
    dbname = "nexa-crm-ai-dev"
    user = "avnadmin"
    password = "Digital!23"
    host = "nagarjuna-crm-dbs.postgres.database.azure.com"
    port = "5432"
    
    try:
        conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
        cur = conn.cursor()
        fetch_query = 'SELECT description FROM public.leads WHERE id=%s'
        cur.execute(fetch_query, (lead_id,))
        fetch_result = cur.fetchone()
        cur.close()
        conn.close()
        
        if fetch_result is None:
            return ""
        return fetch_result[0]
    except Exception as e:
        print(f"Error reading context: {e}")
        return ""
    

class Content_Get:
    def __init__(self, request):
        self.request = request
   
    def whole_sentence(self):
        context = read_context(self.request.lead_id)
        return context
