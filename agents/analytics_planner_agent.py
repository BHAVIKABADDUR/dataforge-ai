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

Convert business questions into data questions.

Examples:

Why is Asia outperforming Europe?
→ Show revenue by region.

Which customer segment performs best?
→ Show revenue by customer segment.

Which products generate the most revenue?
→ Show revenue by product.

Which region performs best?
→ Show revenue by region.

Return only the data question.
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
        "Why is Asia outperforming Europe?",
        "Which customer segment performs best?",
        "Which products generate the most revenue?",
        "Which region performs best?"
    ]

    for q in questions:

        print("\n" + "=" * 60)
        print("Question:", q)

        result = analytics_planner_agent(q)

        print("\nData Question:")
        print(result)