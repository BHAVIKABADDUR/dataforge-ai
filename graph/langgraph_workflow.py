from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.planner_agent import planner_agent


class AgentState(TypedDict):
    question: str
    selected_agent: str


# ── Planner Node ───────────────────────────────────────────
def planner_node(state):

    question = state["question"]

    selected = planner_agent(question)

    return {
        "selected_agent": selected
    }


# ── Router ─────────────────────────────────────────────────
def router(state):

    return state["selected_agent"]


# ── Build Graph ────────────────────────────────────────────
workflow = StateGraph(AgentState)

workflow.add_node(
    "planner",
    planner_node
)

workflow.set_entry_point(
    "planner"
)

workflow.add_conditional_edges(
    "planner",
    router,
    {
        "sql_agent": END,
        "analytics_agent": END,
        "documentation_agent": END,
        "etl_agent": END
    }
)

app = workflow.compile()


# ── Test ───────────────────────────────────────────────────
if __name__ == "__main__":

    questions = [
        "What are the top 5 products by revenue?",
        "Why is Asia outperforming Europe?",
        "Explain the fact_sales table.",
        "Write PySpark code to calculate monthly revenue."
    ]

    for q in questions:

        print("\n" + "=" * 60)
        print("Question:", q)

        result = app.invoke(
            {
                "question": q
            }
        )

        print(result)