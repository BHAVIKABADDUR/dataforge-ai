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

CONTEXT_PROMPT = """
You are a Context Agent.

You receive:

1. Previous Question
2. Current Question

Your job:

- If the current question depends on previous context,
  rewrite it into a complete standalone question.

- If the current question is already complete,
  return it unchanged.

Return ONLY the rewritten question.
"""


def context_agent(previous_question, current_question):

    prompt = f"""
{CONTEXT_PROMPT}

Previous Question:
{previous_question}

Current Question:
{current_question}

Rewritten Question:
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content.strip()


if __name__ == "__main__":

    previous = "What are the top 5 products by revenue?"

    current = "What about Asia?"

    result = context_agent(
        previous,
        current
    )

    print(result)