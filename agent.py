# ecommerce_agent.py
import os
import re
import urllib.parse
import mysql.connector
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate

load_dotenv()

print("MYSQL_HOST:", os.getenv('MYSQL_HOST'))
print("MYSQL_PORT:", os.getenv('MYSQL_PORT'))
print("MYSQL_USER:", os.getenv('MYSQL_USER'))
print("MYSQL_PASSWORD:", os.getenv('MYSQL_PASSWORD'))
print("MYSQL_DATABASE:", os.getenv('MYSQL_DATABASE'))

def test_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password='vamsi@124216',
            database=os.getenv('MYSQL_DATABASE')
        )
        print("✅ Successfully connected to MySQL (direct test)")
        conn.close()
    except Exception as e:
        print("❌ MySQL direct connection failed:", e)

print("\nTesting direct MySQL connection...")
test_mysql_connection()

encoded_password = urllib.parse.quote_plus(os.getenv('MYSQL_PASSWORD'))
DB_URI = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{encoded_password}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
print("\nDB URI (SQLAlchemy/LangChain):", DB_URI)

try:
    db = SQLDatabase.from_uri(DB_URI)
    print("✅ Successfully connected to MySQL via SQLAlchemy/LangChain!")
except Exception as e:
    print("❌ SQLAlchemy/LangChain connection failed:", e)
    exit(1)

llm = OllamaLLM(
    base_url=os.getenv('OLLAMA_BASE_URL'),
    model="llama3.1:8b",
    temperature=0.1
)

CUSTOM_PROMPT = """You are a highly skilled SQL developer analyzing e-commerce data.
You MUST respond ONLY with plain, valid SQL code, NOTHING ELSE.
No explanations, no prefixes, no "SELECT", no "SQLQuery:", no commentary.
Your output must be executable as-is in MySQL.

If you need to filter or group by dates, use STR_TO_DATE(date, '%d\\%m\\%Y') for correct parsing.

The following tables and columns are available:

{table_info}

Answer the following question using the tables above.
Do not qualify column names with table names unless required to resolve ambiguity.

Question: {input}

(top_k rows of example data are available if needed: {top_k})

Your output MUST be exact SQL, with no extra text or commentary.
"""

prompt = PromptTemplate.from_template(CUSTOM_PROMPT)

query_chain = create_sql_query_chain(llm, db, prompt=prompt)

def sanitize_sql(raw_output):
    sql = re.sub(r'^.*?(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|DROP)\b', r'\1', raw_output, flags=re.IGNORECASE | re.DOTALL)
    return sql.strip()

def answer_question(question):
    try:
        print(f"\nQuestion: {question}")
        raw_output = query_chain.invoke({"question": question})
        print("Raw LLM output:", raw_output)
        sql = sanitize_sql(raw_output)
        print("Sanitized SQL:", sql)
        result = db.run(sql)
        return {
            "status": "success",
            "sql": sql,
            "answer": result
        }
    except Exception as e:
        print("Error:", e)
        return {
            "status": "error",
            "error": str(e),
            "question": question
        }

if __name__ == "__main__":
    questions = [
        "What is the total sales across all products?",
        
    ]
    for q in questions:
        response = answer_question(q)
        print("\nResult:", response)
