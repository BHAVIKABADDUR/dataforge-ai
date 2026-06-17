from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.planner_agent import planner_agent
from agents.sql_agent import sql_agent
from agents.analytics_agent import analytics_agent
from agents.documentation_agent import documentation_agent
from agents.etl_agent import etl_agent


# ── State ──────────────────────────────────────────────────
class AgentState(TypedDict):
    question: str
    selected_agent: str
    data: str
    result: str


# ── Planner Node ───────────────────────────────────────────
def planner_node(state):

    question = state["question"]

    selected = planner_agent(question)

    return {
        "selected_agent": selected
    }


# ── SQL Node ───────────────────────────────────────────────
def sql_node(state):

    question = state["question"]

    sql, columns, rows = sql_agent(question)

    return {
        "result": str(rows[:5])
    }


# ── SQL For Analytics Node ─────────────────────────────────
def sql_for_analytics_node(state):

    sql_question = "Show revenue by region."

    sql, columns, rows = sql_agent(sql_question)

    data = []

    for row in rows:
        data.append(
            " | ".join(str(x) for x in row)
        )

    return {
        "data": "\n".join(data)
    }


# ── Analytics Node ─────────────────────────────────────────
def analytics_node(state):

    question = state["question"]

    data = state["data"]

    analysis = analytics_agent(
        question,
        data
    )

    return {
        "result": analysis
    }


# ── Documentation Node ─────────────────────────────────────
def documentation_node(state):

    question = state["question"]

    answer = documentation_agent(question)

    return {
        "result": answer
    }


# ── ETL Node ───────────────────────────────────────────────
def etl_node(state):

    question = state["question"]

    code = etl_agent(question)

    return {
        "result": code
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

workflow.add_node(
    "sql_node",
    sql_node
)

workflow.add_node(
    "sql_for_analytics_node",
    sql_for_analytics_node
)

workflow.add_node(
    "analytics_node",
    analytics_node
)

workflow.add_node(
    "documentation_node",
    documentation_node
)

workflow.add_node(
    "etl_node",
    etl_node
)

workflow.set_entry_point(
    "planner"
)

workflow.add_conditional_edges(
    "planner",
    router,
    {
        "sql_agent": "sql_node",
        "analytics_agent": "sql_for_analytics_node",
        "documentation_agent": "documentation_node",
        "etl_agent": "etl_node"
    }
)

# SQL Path
workflow.add_edge(
    "sql_node",
    END
)

# Analytics Path
workflow.add_edge(
    "sql_for_analytics_node",
    "analytics_node"
)

workflow.add_edge(
    "analytics_node",
    END
)

# Documentation Path
workflow.add_edge(
    "documentation_node",
    END
)

# ETL Path
workflow.add_edge(
    "etl_node",
    END
)

app = workflow.compile()


# ── Test ───────────────────────────────────────────────────
if __name__ == "__main__":

    questions = [
        "Why is Asia outperforming Europe?"
    ]

    for q in questions:

        print("\n" + "=" * 80)
        print("Question:", q)

        result = app.invoke(
            {
                "question": q
            }
        )

        print("\nResult:")
        print(result)