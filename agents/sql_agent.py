# agents/sql_agent.py
# SQL Agent — converts natural language to SQL and queries RetailIQDW

import pyodbc
import os
import time
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
        r"Trusted_Connection=yes"
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

General Rules:
- This is Microsoft SQL Server.
- Use TOP N instead of LIMIT.
- Always JOIN fact_sales with dimension tables using the correct ID columns.
- Use SUM(total_sales) for revenue calculations.
- Use COUNT(order_id) for order counts.
- Use AVG(total_sales) for average order value.
- Use AVG(discount) when asked for average discounts.
- Return ONLY the SQL query.
- Do not include explanations.
- Do not include markdown.

SQL Server Rules:
- Never use LIMIT.
- Only use TOP N when the user explicitly asks for top, bottom, highest, lowest, first, or last results.
- Do not generate TOP 100.
- Do not generate TOP 100 PERCENT unless absolutely necessary.

Time Intelligence Rules:
- For monthly trends, GROUP BY year and month.
- For quarterly analysis, GROUP BY year and quarter.
- For yearly analysis, GROUP BY year.
- Never GROUP BY date_id when the question asks for month, quarter, or year level reporting.
- If a question asks for monthly revenue, return one row per month.
- If a question asks for quarterly revenue, return one row per quarter.
- If a question asks for yearly revenue, return one row per year.

Ranking Rules:
- When asked for:
    - top N in each category
    - top N per region
    - top N per customer segment
  use ROW_NUMBER() OVER(PARTITION BY ...).
- Do not use TOP N for grouped rankings.
- Use window functions when ranking inside groups.

Warehouse Relationships:
- fact_sales.product_id -> dim_product.product_id
- fact_sales.customer_id -> dim_customer.customer_id
- fact_sales.region_id -> dim_region.region_id
- fact_sales.date_id -> dim_date.date_id
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

# ── 5. Execute SQL with retry ─────────────────────────────────────────────────
def execute_sql(sql: str):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return columns, rows
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1} failed, retrying in 3 seconds...")
                time.sleep(3)
            else:
                raise e

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
    questions = [
    "Show revenue by month and category.", 
    "Compare revenue between Asia and Europe.", 
    "Which product had the biggest revenue increase over time?", 
    "Show the top 3 customer segments by revenue.", 
    "What was the worst performing quarter?",
      "Show the top 2 products in each region.",
        "Which category performed best in each year?", 
    "What percentage of total revenue comes from electronics?"
]
    for q in questions:
        print("\n" + "="*60)
        sql_agent(q)