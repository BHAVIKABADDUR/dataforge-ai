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

SCHEMA_DOCUMENTATION = """
RetailIQDW Schema

fact_sales
-----------
sales_key
order_id
customer_id
product_id
region_id
date_id
quantity
price
discount
total_sales

Purpose:
Stores transactional sales records.

dim_customer
------------
customer_id
customer_segment

Purpose:
Stores customer segment information.

dim_product
-----------
product_id
product
category

Purpose:
Stores product and category information.

dim_region
----------
region_id
region

Purpose:
Stores sales region information.

dim_date
--------
date_id
order_date
year
month
quarter
day

Purpose:
Stores date attributes for reporting.
"""

DOCUMENTATION_PROMPT = """
You are the Documentation Agent for RetailIQ.

Your responsibilities:

- Explain tables
- Explain columns
- Explain schema relationships
- Describe business definitions

Use ONLY the provided schema documentation.

Do not invent tables.

Do not invent columns.

Respond clearly for business users.
"""

def documentation_agent(question: str):

    prompt = f"""
{DOCUMENTATION_PROMPT}

Schema Documentation:

{SCHEMA_DOCUMENTATION}

Question:

{question}

Answer:
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content.strip()


if __name__ == "__main__":

    questions = [
        "Explain the fact_sales table.",
        "What columns exist in dim_product?",
        "Describe the RetailIQDW schema.",
        "What does total_sales mean?"
    ]

    for q in questions:

        print("\n" + "=" * 60)
        print("Question:", q)

        result = documentation_agent(q)

        print("\nAnswer:")
        print(result)