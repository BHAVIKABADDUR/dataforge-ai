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

PROMPT = """
You are a business analytics planner.

Your job is to convert business questions into simple data retrieval questions
that a SQL agent can answer.

Rules:
- Always return a data question that retrieves numbers from the warehouse
- Never ask for explanations — only ask for data
- Keep the data question simple and specific

Examples:

Why is Asia outperforming Europe?
→ Show revenue by region.

Which customer segment performs best?
→ Show revenue by customer segment.

Which products generate the most revenue?
→ Show revenue by product.

Which region performs best?
→ Show revenue by region.

Which region has the lowest performance?
→ Show revenue by region ordered from lowest to highest.

Which region is underperforming?
→ Show revenue by region.

Which product is declining?
→ Show revenue by product ordered from lowest to highest.

Why is revenue dropping?
→ Show monthly revenue trend.

Which category performs worst?
→ Show revenue by category ordered from lowest to highest.

How are customer segments performing?
→ Show revenue by customer segment.

Return only the data question. Nothing else.
"""


def analytics_planner_agent(question: str):

    prompt = f"""
{PROMPT}

Question:
{question}

Data Question:
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content.strip()


if __name__ == "__main__":

    questions = [
    "Which region has the lowest performance and why?",
    "What is driving the revenue gap between segments?",
    "Which product category is underperforming?",
    "Is there a seasonal trend in our sales?"
]

    for q in questions:

        print("\n" + "=" * 60)
        print("Question:", q)

        result = analytics_planner_agent(q)

        print("\nData Question:")
        print(result)