from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os

load_dotenv()

# ── 1. LLM Setup ─────────────────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# ── 2. Analytics Prompt ──────────────────────────────────────────────────────
ANALYTICS_PROMPT = """
You are a Senior Business Analyst for RetailIQ.

Your responsibilities:

- Explain business performance
- Identify trends
- Provide business insights
- Interpret data
- Suggest recommendations

Rules:

- Use ONLY the provided data.
- Do NOT invent facts.
- Do NOT assume information that is not present in the data.
- If exact calculations are required, use only the values shown in the data.
- Do not exaggerate differences.
- Reference the actual numbers provided.
- Do NOT generate SQL.
- Do NOT generate code.

Structure your response as:

1. Key Finding
2. Business Interpretation
3. Recommendation
"""

# ── 3. Analytics Agent ───────────────────────────────────────────────────────
def analytics_agent(question: str, data: str):

    prompt = f"""
{ANALYTICS_PROMPT}

Business Question:
{question}

Available Data:
{data}

Business Analysis:
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content.strip()

# ── 4. Test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    question = "Why is Asia outperforming Europe?"

    data = """
Region | Revenue
Asia | 100
Europe | 90
"""
    result = analytics_agent(
        question,
        data
    )

    print("\n" + "=" * 60)
    print("Question:", question)

    print("\nData:")
    print(data)

    print("\nAnalysis:")
    print(result)