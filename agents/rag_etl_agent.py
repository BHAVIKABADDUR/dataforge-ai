# agents/rag_etl_agent.py
# ETL Agent with RAG — uses retrieved schema to prevent hallucination

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

# Hardcoded allowed columns as safety guardrail
ALLOWED_COLUMNS = """
silver_sales columns (the ONLY columns you may use):
- order_id
- customer_id
- customer_segment
- order_date
- region
- category
- product
- quantity
- price
- discount
- total_sales
"""

ETL_PROMPT = """
You are the ETL Agent for RetailIQ.

You will be given:
1. Retrieved schema documentation
2. A list of allowed columns
3. A user request

Rules:
- Use ONLY the columns listed in the allowed columns section
- Never invent or assume columns that are not listed
- Use silver_sales as the input DataFrame
- Use total_sales for revenue calculations
- Generate PySpark DataFrame code only
- Do not explain the code
- Do not generate SQL
- Assume Spark session already exists
- Strip markdown from output
- Return code only
- Use ONLY columns present in the schema.

- Do not invent business rules.

- Do not invent churn thresholds.

- Do not invent customer lifetime assumptions.

- Do not invent profit, cost, margin, or inventory values unless they exist in the schema.

- If required information does not exist in the schema, explain the limitation and generate the closest possible transformation using available columns.
"""


def rag_etl_agent(question: str) -> str:
    from rag.retriever import retrieve

    question_lower = question.lower()

    # ── Business Rule Guardrails ──────────────────────────

    if any(
        word in question_lower
        for word in [
            "profit",
            "profitability",
            "margin",
            "gross margin",
            "net margin"
        ]
    ):
        return """
Profitability analysis cannot be generated.

Reason:
The RetailIQ schema does not contain cost, profit,
margin, or expense fields.

Available financial fields:
- quantity
- price
- discount
- total_sales
"""

    if any(
        word in question_lower
        for word in [
            "churn",
            "retention",
            "attrition"
        ]
    ):
        return """
Customer churn transformation cannot be generated.

Reason:
The RetailIQ schema does not define a churn rule.

Additional business logic is required
(e.g. 30 days inactive, 90 days inactive, etc.).
"""

    if any(
        word in question_lower
        for word in [
            "lifetime value",
            "customer lifetime value",
            "clv"
        ]
    ):
        return """
from pyspark.sql import functions as F

customer_lifetime_value = (
    silver_sales
    .groupBy("customer_id")
    .agg(
        F.sum("total_sales").alias("lifetime_revenue"),
        F.count("order_id").alias("total_orders"),
        F.avg("total_sales").alias("avg_order_value")
    )
)
"""

    # ── RAG Retrieval ─────────────────────────────────────

    docs = retrieve(question, top_k=2)

    context = "\n\n".join(docs)

    prompt = f"""
{ETL_PROMPT}

Retrieved Schema Documentation:
{context}

{ALLOWED_COLUMNS}

Request:
{question}

PySpark Code:
"""

    response = llm.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )

    code = response.content.strip()

    code = (
        code
        .replace("```python", "")
        .replace("```", "")
        .strip()
    )

    return code


if __name__ == "__main__":

    test_cases = [
        "Create profitability analysis",
        "Create churn transformation",
        "Create customer lifetime value transformation"
    ]

    for q in test_cases:
        print("\n" + "=" * 60)
        print("Question:", q)
        result = rag_etl_agent(q)
        print("\nGenerated Code:\n")
        print(result)