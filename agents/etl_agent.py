from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

ETL_PROMPT = """
You are the ETL Agent for RetailIQ.

RetailIQ Data Model:

silver_sales
------------
order_id
customer_id
customer_segment
order_date
region
category
product
quantity
price
discount
total_sales

Responsibilities:

- Generate PySpark code
- Create Silver transformations
- Create Gold aggregations
- Build KPI tables

Rules:

- Use RetailIQ column names exactly
- Use total_sales for revenue calculations
- Use silver_sales as the input DataFrame
- Generate PySpark DataFrame code only
- Do not explain code
- Do not generate SQL
- Assume Spark session already exists
- Return code only
"""

def etl_agent(question: str):

    prompt = f"""
{ETL_PROMPT}

Request:

{question}

PySpark Code:
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    code = response.content.strip()

    code = code.replace("```python", "")
    code = code.replace("```", "")
    code = code.strip()

    return code


if __name__ == "__main__":

    questions = [
    "Create a Gold table for revenue by region.",
    "Create a Gold table for top products.",
    "Create monthly revenue aggregation."
]

    for q in questions:

        print("\n" + "=" * 60)
        print("Question:", q)

        result = etl_agent(q)

        print("\nGenerated Code:\n")
        print(result)