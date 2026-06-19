# agents/planner_agent.py
# Planner Agent for DataForge AI — routes user intent to specialized agents

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

PLANNER_PROMPT = """
You are the Planner Agent for DataForge AI.

Your job is to select the correct specialized agent.

Available Agents:

1. sql_agent
Use for:
- Revenue analysis
- Sales analysis
- Product analysis
- Customer analysis
- Region analysis
- KPI reporting
- Trend reporting
- Questions requiring SQL queries
- Questions asking for data retrieval

Examples:
What are the top 5 products by revenue?
→ sql_agent

Show monthly revenue trends.
→ sql_agent

Show revenue by category.
→ sql_agent

Show quarterly revenue.
→ sql_agent

Which customer segment generates the most revenue?
→ sql_agent

What is the average discount by category?
→ sql_agent


2. analytics_agent
Use for:
- Business insights
- Recommendations
- Performance interpretation
- Root cause analysis
- Explanations of business results
- Questions asking WHY something happened
- Questions asking for recommendations

Examples:
Why is Asia outperforming Europe?
→ analytics_agent

Why did revenue decrease?
→ analytics_agent

What customer insights can you provide?
→ analytics_agent

Recommend ways to increase revenue.
→ analytics_agent

Explain business performance.
→ analytics_agent


3. documentation_agent
Use for:
- Table descriptions
- Column explanations
- Schema questions
- Data warehouse documentation

Examples:
Explain the fact_sales table.
→ documentation_agent

Describe dim_product.
→ documentation_agent

What columns exist in fact_sales?
→ documentation_agent

Describe the RetailIQDW schema.
→ documentation_agent


4. etl_agent
Use for:
- PySpark code
- ETL pipelines
- Data engineering tasks
- Transformations
- Gold/Silver layer creation

Examples:
Write PySpark code to calculate monthly revenue.
→ etl_agent

Generate PySpark code for customer aggregation.
→ etl_agent

Create a Gold table for revenue by region.
→ etl_agent

Build an ETL pipeline for sales data.
→ etl_agent


Important Rules:

- Questions asking for DATA, REPORTS, REVENUE, SALES, PRODUCTS, CUSTOMERS, REGIONS, COUNTS, SUMS, AVERAGES, MONTHLY TRENDS, QUARTERLY TRENDS, KPI REPORTS → sql_agent

- Questions asking WHY, RECOMMENDATIONS, INSIGHTS, BUSINESS INTERPRETATION, ROOT CAUSE ANALYSIS → analytics_agent

- Questions about TABLES, COLUMNS, SCHEMA, DEFINITIONS, DOCUMENTATION → documentation_agent

- Questions asking for PYSPARK, ETL, DATA ENGINEERING CODE, TRANSFORMATIONS, PIPELINES → etl_agent

Return ONLY one of:

sql_agent
analytics_agent
documentation_agent
etl_agent
"""


def planner_agent(question: str) -> str:

    question_lower = question.lower()

    # ── Deterministic ETL Routing ─────────────────────────

    etl_keywords = [
        "create",
        "build",
        "generate",
        "write",
        "develop",
        "pyspark",
        "etl",
        "transformation",
        "pipeline",
        "gold table",
        "silver table"
    ]

    if any(keyword in question_lower for keyword in etl_keywords):
        return "etl_agent"

    # ── LLM Planner ───────────────────────────────────────

    prompt = f"""
{PLANNER_PROMPT}

User Question:
{question}

Agent:
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content.strip()


if __name__ == "__main__":

    test_cases = [
        "Create profitability analysis",
        "Create gross margin analysis",
        "Create churn transformation",
        "Build an ETL pipeline for sales data",
        "Show revenue by region.",
        "Explain the dim_product table.",
        "Why is Asia outperforming Europe?"
    ]

    for q in test_cases:
        print("\n" + "=" * 60)
        print("Question:", q)
        agent = planner_agent(q)
        print("Selected Agent:", agent)