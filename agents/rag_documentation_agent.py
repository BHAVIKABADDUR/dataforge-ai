from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from rag.retriever import retrieve

import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)


def rag_documentation_agent(question):

    docs = retrieve(question)

    context = "\n\n".join(docs)

    prompt = f"""
You are the Documentation Agent for RetailIQ.

Answer ONLY using the retrieved documentation.

If the answer is not present in the documentation,
say:

"I could not find that information in the documentation."

Documentation:

{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content


if __name__ == "__main__":

    questions = [
        "What columns exist in dim_product?",
        "Explain the fact_sales table."
    ]

    for q in questions:

        print("\n" + "=" * 60)
        print("Question:", q)

        answer = rag_documentation_agent(q)

        print("\nAnswer:")
        print(answer)