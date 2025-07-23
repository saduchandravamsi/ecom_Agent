# ecommerce_agent.py
# Requires .env with:
# MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
# and OLLAMA_BASE_URL (e.g., http://localhost:11434)
# ecommerce_agent.py
# ecommerce_agent.py
# Requires .env with:
# MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
# and OLLAMA_BASE_URL (e.g., http://localhost:11434)
import os
import re
import urllib.parse
import mysql.connector
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Debug: Print environment variables
print("MYSQL_HOST:", os.getenv('MYSQL_HOST'))
print("MYSQL_PORT:", os.getenv('MYSQL_PORT'))
print("MYSQL_USER:", os.getenv('MYSQL_USER'))
print("MYSQL_PASSWORD:", os.getenv('MYSQL_PASSWORD'))
print("MYSQL_DATABASE:", os.getenv('MYSQL_DATABASE'))

# Optional: Direct MySQL connection test (for troubleshooting)
def test_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password='vamsi@124216',  # Replace with your raw password for testing only
            database=os.getenv('MYSQL_DATABASE')
        )
        print("✅ Successfully connected to MySQL (direct test)")
        conn.close()
    except Exception as e:
        print("❌ MySQL direct connection failed:", e)

print("\nTesting direct MySQL connection...")
test_mysql_connection()

# Safely build the DB URI (URL-encode password)
encoded_password = urllib.parse.quote_plus(os.getenv('MYSQL_PASSWORD'))
DB_URI = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{encoded_password}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
print("\nDB URI (SQLAlchemy/LangChain):", DB_URI)

# Connect to the database with SQLAlchemy/LangChain
try:
    db = SQLDatabase.from_uri(DB_URI)
    print("✅ Successfully connected to MySQL via SQLAlchemy/LangChain!")
except Exception as e:
    print("❌ SQLAlchemy/LangChain connection failed:", e)
    exit(1)

# Set up Ollama LLM (use the model name exactly as shown in 'ollama list')
llm = OllamaLLM(
    base_url=os.getenv('OLLAMA_BASE_URL'),
    model="llama3.1:8b",  # Must match your local Ollama library!
    temperature=0.1
)

# --- SQL Query Generation Prompt ---
CUSTOM_PROMPT = """You are a highly skilled SQL developer analyzing e-commerce data.
You MUST respond ONLY with plain, valid, executable SQL, NOTHING ELSE.
No explanations, no prefixes, no "SELECT", no "SQLQuery:", no commentary, no markdown.
Your output must be ready to run in MySQL as-is.

If you need to filter or group by dates, use STR_TO_DATE(date, '%d\\%m\\%Y') for correct parsing.

Relevant tables and columns:

{table_info}

Answer the following question using only the tables and columns above.
Do not qualify column names with table names unless required to resolve ambiguity.

Question: {input}

(top_k sample rows available if needed: {top_k})

Your output MUST be exact SQL, with no extra text or commentary.
"""

prompt = PromptTemplate.from_template(CUSTOM_PROMPT)

# Build the query chain with your custom prompt
query_chain = create_sql_query_chain(llm, db, prompt=prompt)

# Utility to clean up raw SQL (removes LLM's extra text/instructions)
def sanitize_sql(raw_output):
    # Remove everything up to and including the first SELECT, INSERT, etc.
    sql = re.sub(r'^.*?(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|DROP)\b', r'\1', raw_output, flags=re.IGNORECASE | re.DOTALL)
    # Remove any remaining non-SQL text before the query
    sql = re.sub(r'^.*?\b(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|DROP)\b', r'\1', sql, flags=re.IGNORECASE | re.DOTALL)
    return sql.strip()

# --- Semantic Humanization ---
def humanize_answer(question, sql, result):
    """Asks the LLM to turn SQL results into a friendly, natural answer."""
    if not result or (isinstance(result, (list, tuple)) and not result):
        return "Sorry, I couldn't find an answer to that question."
    humanize_prompt = """You are a skilled data analyst presenting results to business users in plain language.

Given:
- **User's question:** {question}
- **SQL ran:** {sql}
- **SQL answer:** {result}

Write 1-2 sentences explaining the answer in clear, simple, friendly language.
Do NOT mention SQL, tables, code, or the query.
If the result is a list of products (e.g., ["1", "2"]), format them as "The eligible products are 1 and 2."
If the result is multiple rows or numbers (e.g., [[12.5], [13.7]]), summarize or list them as appropriate.
If the result is unclear, say "I couldn't extract a clear answer."
"""
    prompt = humanize_prompt.format(
        question=question,
        sql=sql,
        result=str(result)
    )
    return llm.invoke(prompt).strip()

# --- Core Agent Logic ---
def answer_question(question):
    """Takes a natural language question, returns SQL, answer, and a friendly summary."""
    try:
        print(f"\nQuestion: {question}")
        raw_output = query_chain.invoke({"question": question})
        print("Raw LLM output:", raw_output)
        sql = sanitize_sql(raw_output)
        print("Sanitized SQL:", sql)
        result = db.run(sql)
        friendly = humanize_answer(question, sql, result)
        return {
            "status": "success",
            "sql": sql,
            "answer": result,
            "friendly": friendly
        }
    except Exception as e:
        print("Error:", e)
        return {
            "status": "error",
            "error": str(e),
            "question": question
        }

# --- Demo/Test Loop (Optional) ---
if __name__ == "__main__":
    questions = [
        "What is the total sales across all products?",
        "Which product had the highest CPC?",
        "Calculate the RoAS (Return on Ad Spend).",
        "List all eligible products.",
        "Show total ad spend by product.",
        "How many units were sold via ads for product P1001?"
    ]
    for q in questions:
        response = answer_question(q)
        print("\nResult:", response)





# import os
# import urllib.parse
# import re
# import mysql.connector
# from dotenv import load_dotenv
# from langchain_ollama import OllamaLLM
# from langchain_community.utilities import SQLDatabase
# from langchain.chains import create_sql_query_chain

# load_dotenv()

# def test_mysql_connection():
#     try:
#         conn = mysql.connector.connect(
#             host=os.getenv('MYSQL_HOST'),
#             user=os.getenv('MYSQL_USER'),
#             password='vamsi@124216',  # literal password for testing
#             database=os.getenv('MYSQL_DATABASE')
#         )
#         print("✅ Successfully connected to MySQL (direct test)")
#         conn.close()
#     except Exception as e:
#         print("❌ MySQL direct connection failed:", e)

# print("Testing direct MySQL connection...")
# test_mysql_connection()

# encoded_password = urllib.parse.quote_plus(os.getenv('MYSQL_PASSWORD'))
# DB_URI = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{encoded_password}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
# print("\nDB URI (SQLAlchemy/LangChain):", DB_URI)

# try:
#     db = SQLDatabase.from_uri(DB_URI)
#     print("✅ Successfully connected to MySQL via SQLAlchemy/LangChain!")
# except Exception as e:
#     print("❌ SQLAlchemy/LangChain connection failed:", e)
#     exit(1)

# llm = OllamaLLM(base_url=os.getenv('OLLAMA_BASE_URL'), model="llama3.1:8b", temperature=0.1)
# query_chain = create_sql_query_chain(llm, db)  # <-- Let LangChain handle the prompt

# def extract_sql(raw_output):
#     sql = re.sub(r'^.*?(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|DROP)\b', r'\1', raw_output, flags=re.IGNORECASE | re.DOTALL)
#     sql = re.sub(r'^.*?\b(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|DROP)\b', r'\1', sql, flags=re.IGNORECASE | re.DOTALL)
#     return sql.strip()

# def answer_question(question):
#     try:
#         raw_output = query_chain.invoke({"question": question})
#         print("Raw LLM output:", raw_output)
#         sql = extract_sql(raw_output)
#         print("Sanitized SQL:", sql)
#         result = db.run(sql)
#         return {"status": "success", "sql": sql, "answer": result}
#     except Exception as e:
#         return {"status": "error", "error": str(e), "question": question}

# if __name__ == "__main__":
#     questions = [
#         "What is the total sales across all products?",
#         "what is the total items where products are   eligible ?",
#         "Show total ad spend by product.",
#         "How many units were sold via ads for product P1001?"
#     ]
#     for q in questions:
#         response = answer_question(q)
#         print(f"\nQuestion: {q}")
#         print("Result:", response)
