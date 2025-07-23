AI E-commerce Analytics Agent
A production-ready Python agent that translates natural language questions into SQL, queries your MySQL e-commerce database, and returns business-friendly answers via a Flask web API.
Powered by Llama 3.1:8b (via Ollama) and LangChain.

Features:
Natural language to SQL—ask questions like “What is total sales?” or “Which product had the highest CPC?”
Dynamic schema handling—automatically detects your MySQL tables and columns.
Human-friendly answers—explains results in plain business language.
REST API—easy integration with dashboards, apps, or automation.
Interactive web UI—test your agent right in the browser.
Debugging and timing—see where time is spent in each query.

Quick Start
1. Clone the Repository

    -git clone https://github.com/yourusername/ecommerce-ai-agent.git

   -cd ecommerce-ai-agent

3. Install Required Python Packages
Install the following dependencies in your virtual environment:

   -pip install flask mysql-connector-python sqlalchemy langchain langchain-community langchain-ollama python-dotenv

   Update Ollama and pull your model:
  -ollama pull llama3.1:8b

3. Configure Environment

      Rename .env.example to .env and edit with your credentials:

# MySQL
MYSQL_HOST=localhost

MYSQL_PORT=3306

MYSQL_USER=your_username

MYSQL_PASSWORD=your_password

MYSQL_DATABASE=your_database

# Ollama

OLLAMA_BASE_URL=http://localhost:11434

4. Start the API Server

   -python api_server.py

Open your browser to http://localhost:8000 to use the interactive web form.

API Endpoint: POST /ask with {"question": "your question"}


-----------------------------------------------------------------------------------------------------------------

Directory Structure:

ecommerce-ai-agent/


├── api_server.py        # Flask web/app server

├── ecommerce_agent.py   # Core AI agent logic

├── .env                 # Environment variables

├── README.md            # This file

└── (other files as needed)

Usage

Via Web Browser

Open http://localhost:8000 in your browser, type your question, and see the answer and raw SQL.

Via API (curl, Postman, etc.)

bash
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question": "What is the total sales?"}'


Response example:
json

{

  "status": "success",
  
  "sql": "SELECT SUM(total_sales) FROM ...",
  
  "answer": [[1042567.34]],
  
  "friendly": "The total sales of all products is ₹1,042,567.34.",
  
  "timing": {
    "llm_generate_sql_seconds": 1.2,
    "sql_query_seconds": 0.05,
    "llm_humanize_seconds": 1.1,
    "total_seconds": 2.35
  
  }

}

Technical Overview:
Natural language understanding: Llama 3.1:8b (via Ollama)
Database integration: SQLAlchemy + mysql-connector-python
Prompt engineering: LangChain for dynamic schema injection and strict SQL generation
Web server: Flask for REST API and interactive UI
Environment management: python-dotenv

!!! Required Python Packages !!!
Copy-paste this to install everything:


bash

pip install flask mysql-connector-python sqlalchemy langchain langchain-community langchain-ollama python-dotenv

Packages used:
flask (web server)

mysql-connector-python (MySQL driver)

sqlalchemy (database toolkit)

langchain (LLM orchestration)

langchain-community (SQLDatabase integration)

langchain-ollama (Ollama LLM support)

python-dotenv (environment variables)



