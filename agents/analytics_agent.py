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

ANALYTICS_PROMPT = """
You are a Senior Business Analyst for RetailIQ.

Your role is to:

- Explain business performance
- Identify trends
- Provide insights
- Suggest recommendations
- Interpret business results

Do NOT generate SQL.

Do NOT generate code.

Respond like a business analyst speaking to a manager.

Keep responses concise and actionable.
"""

def analytics_agent(question: str):

    prompt = f"""
{ANALYTICS_PROMPT}

Question:
{question}

Business Analysis:
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content.strip()


if __name__ == "__main__":

    questions = [
        "Why is Asia outperforming Europe?",
        "Recommend ways to increase revenue.",
        "What insights can you provide about customer segments?",
        "Explain sales trends over time."
    ]

    for q in questions:
        print("\n" + "=" * 60)
        print("Question:", q)

        result = analytics_agent(q)

        print("\nAnalysis:")
        print(result)