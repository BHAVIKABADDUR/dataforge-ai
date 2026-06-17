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

Your job is to decide which specialized agent should handle the user's request.

Available Agents:

1. sql_agent
- Revenue questions
- Sales analysis
- Product analysis
- Customer analysis
- Region analysis
- Questions requiring SQL queries

2. analytics_agent
- Trend analysis
- Business insights
- Explanations of results
- Performance interpretation
- Root cause analysis
- Questions asking WHY something happened
- Questions asking for insights or recommendations
- Questions that explain business performance

3. documentation_agent
- Table descriptions
- Column explanations
- Schema questions
- Data warehouse documentation

4. etl_agent
- PySpark code
- Data engineering tasks
- ETL pipelines
- Transformations

Routing Rules:

- If the user asks WHAT, HOW MUCH, TOP, COUNT, SUM, AVERAGE, REVENUE, SALES, PRODUCTS, CUSTOMERS, REGIONS → sql_agent

- If the user asks WHY, EXPLAIN, INSIGHTS, TRENDS, RECOMMENDATIONS, PERFORMANCE ANALYSIS → analytics_agent

- If the user asks about tables, columns, schema, definitions, documentation → documentation_agent

- If the user asks for PySpark, ETL, transformations, pipelines, data engineering code → etl_agent

Return ONLY one of:

sql_agent
analytics_agent
documentation_agent
etl_agent
"""

def planner_agent(question: str):

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

    questions = [
    "Show revenue by region.",
    "Which products generated the highest revenue?",
    "Explain the dim_product table.",
    "What columns exist in fact_sales?",
    "Write PySpark code to calculate monthly revenue.",
    "Build an ETL pipeline for sales data.",
    "Why is Asia outperforming Europe?",
    "Recommend ways to improve customer revenue."
]
    

    for q in questions:
        print("\n" + "=" * 60)
        print("Question:", q)

        agent = planner_agent(q)

        print("Selected Agent:", agent)