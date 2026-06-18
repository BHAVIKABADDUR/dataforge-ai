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

CLASSIFY_PROMPT = """
You are a question classifier.

Classify the current question as either COMPLETE or FOLLOW_UP.

FOLLOW_UP means the question is ambiguous without knowing the previous question.
Examples of FOLLOW_UP:
- "What about Asia?"
- "How about Europe?"
- "Show the same for Q2."
- "What about customer segments?"
- "And for fashion category?"

COMPLETE means the question makes full sense on its own.
Examples of COMPLETE:
- "Why is Asia outperforming Europe?"
- "Explain the fact_sales table."
- "What are the top 5 products by revenue?"
- "Create a PySpark transformation for customer segmentation."
- "What columns exist in dim_product?"

Return ONLY one word: COMPLETE or FOLLOW_UP
"""

REWRITE_PROMPT = """
You are a Context Agent.

Rewrite the follow-up question into a complete standalone question
using the previous question as context.

Return ONLY the rewritten question. Nothing else.
"""


def context_agent(previous_question, current_question):

    # Step 1: Classify the question
    classify_prompt = f"""
{CLASSIFY_PROMPT}

Previous Question:
{previous_question}

Current Question:
{current_question}

Classification:
"""

    classification = llm.invoke(
        [HumanMessage(content=classify_prompt)]
    ).content.strip().upper()

    # Step 2: If complete, return unchanged
    if "COMPLETE" in classification:
        return current_question

    # Step 3: If follow-up, rewrite it
    rewrite_prompt = f"""
{REWRITE_PROMPT}

Previous Question:
{previous_question}

Follow-up Question:
{current_question}

Rewritten Question:
"""

    rewritten = llm.invoke(
        [HumanMessage(content=rewrite_prompt)]
    ).content.strip()

    return rewritten


if __name__ == "__main__":

    test_cases = [
        {
            "previous": "What is the total revenue by category?",
            "current": "What about the fashion category specifically?",
            "expected": "FOLLOW_UP"
        },
        {
            "previous": "Show me revenue by region",
            "current": "Which customer segment has the highest average order value?",
            "expected": "COMPLETE"
        },
        {
            "previous": "What are the top products in Asia?",
            "current": "Same for Europe?",
            "expected": "FOLLOW_UP"
        },
        {
            "previous": "Explain the dim_customer table",
            "current": "Generate a PySpark script to load fact_sales into a Delta table",
            "expected": "COMPLETE"
        }
    ]

    for test in test_cases:
        print("\n" + "=" * 60)
        print("Previous :", test["previous"])
        print("Current  :", test["current"])
        print("Expected :", test["expected"])
        result = context_agent(test["previous"], test["current"])
        print("Result   :", result)