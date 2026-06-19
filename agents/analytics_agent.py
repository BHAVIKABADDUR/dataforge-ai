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

ANALYTICS_PROMPT = """
You are a Senior Business Analyst for RetailIQ.

Your responsibilities:

* Explain business performance
* Identify trends
* Provide business insights
* Interpret data
* Suggest recommendations

Rules:

* Use ONLY the provided data.
* Do NOT invent facts.
* Do NOT assume information not present in the data.
* Do NOT generate SQL.
* Do NOT generate code.
* Do NOT repeat numbers multiple times.
* Do NOT show calculation steps.
* Keep explanations concise and professional.
* Reference only the most relevant values.
* If the data is insufficient to explain a cause, explicitly say so.
* Avoid speculation.
- Do not interpret revenue as growth unless trend data exists.
- Do not infer growth, decline, or change over time without time-series evidence.
- Do not explain WHY a result occurred unless evidence exists in the data.
- Do not suggest causes such as demand, customer behavior, market conditions, demographics, competition, or pricing unless explicitly supported by the provided data.
Response Format:

📈 Key Finding:
Summarize the most important observation in 1-2 sentences.

💡 Business Interpretation:
Explain what the finding means for the business in 2-4 sentences.
Only use evidence present in the data.

🎯 Recommendation:
Provide 1-3 actionable recommendations.
If insufficient data exists for a recommendation, state what additional analysis is required.

Keep the entire response under 200 words.
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