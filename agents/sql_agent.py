# agents/sql_agent.py
# SQL Agent — converts natural language to SQL and queries RetailIQDW

import pyodbc
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

# ── 1. Connect to SQL Server ─────────────────────────────────────────────────
def get_connection():
    return pyodbc.connect(
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=BHAVIKA\SQLEXPRESS;"
        r"DATABASE=RetailIQDW;"
        r"Trusted_Connection=yes;"
        r"Connection Timeout=60;"
    )
# ── 2. Schema info for the LLM ───────────────────────────────────────────────
SCHEMA_INFO = """
You are a SQL expert working with a retail data warehouse called RetailIQDW.

Tables available:
- fact_sales (sales_key, order_id, customer_id, product_id, region_id, date_id, quantity, price, discount, total_sales)
- dim_customer (customer_id, customer_segment)
- dim_product (product_id, product, category)
- dim_region (region_id, region)
- dim_date (date_id, order_date, year, month, quarter, day)

Rules:

- This is Microsoft SQL Server — use TOP N instead of LIMIT
- Always JOIN fact_sales with dimension tables using the appropriate ID columns
- Use SUM(total_sales) for revenue calculations
- Use COUNT(order_id) for order counts
- Never use LIMIT — always use SELECT TOP N
- Return only the SQL query, nothing else, no explanation, no markdown
"""
# ── 3. LLM setup ─────────────────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# ── 4. Generate SQL from question ─────────────────────────────────────────────
def generate_sql(question: str) -> str:
    prompt = f"{SCHEMA_INFO}\n\nQuestion: {question}\n\nSQL Query:"
    response = llm.invoke([HumanMessage(content=prompt)])
    sql = response.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

# ── 5. Execute SQL ────────────────────────────────────────────────────────────
def execute_sql(sql: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return columns, rows

# ── 6. Main agent function ────────────────────────────────────────────────────
def sql_agent(question: str):
    print(f"\nQuestion: {question}")
    print("Generating SQL...")
    sql = generate_sql(question)
    print(f"Generated SQL:\n{sql}")
    print("\nExecuting...")
    columns, rows = execute_sql(sql)
    print("\nResults:")
    print(" | ".join(columns))
    print("-" * 60)
    for row in rows:
        print(" | ".join(str(val) for val in row))
    return sql, columns, rows

# ── 7. Test ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sql_agent("What are the top 5 products by total revenue?")