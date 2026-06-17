from agents.planner_agent import planner_agent
from agents.sql_agent import sql_agent
from agents.analytics_agent import analytics_agent
from agents.documentation_agent import documentation_agent


def run_workflow(question):

    selected_agent = planner_agent(question)

    print("\n" + "=" * 60)
    print("Planner Selected:", selected_agent)

    # SQL Agent
    if selected_agent == "sql_agent":

        sql, columns, rows = sql_agent(question)

        return {
            "agent": "sql_agent",
            "sql": sql,
            "columns": columns,
            "rows": rows
        }

    # Analytics Agent
    elif selected_agent == "analytics_agent":

        sample_data = """
Region | Revenue
Asia | 17254330.37
Europe | 16921682.58
"""

        result = analytics_agent(
            question,
            sample_data
        )

        return {
            "agent": "analytics_agent",
            "analysis": result
        }

    # Documentation Agent
    elif selected_agent == "documentation_agent":

        result = documentation_agent(question)

        return {
            "agent": "documentation_agent",
            "answer": result
        }

    # ETL Agent (not built yet)
    elif selected_agent == "etl_agent":

        return {
            "agent": "etl_agent",
            "message": "ETL Agent not implemented yet."
        }

    # Fallback
    else:

        return {
            "agent": selected_agent,
            "message": "Unknown agent selected."
        }


if __name__ == "__main__":

    questions = [
        "What are the top 5 products by revenue?",
        "Why is Asia outperforming Europe?",
        "Explain the fact_sales table.",
        "What columns exist in dim_product?",
        "Describe the RetailIQDW schema."
    ]

    for q in questions:

        print("\n" + "=" * 80)
        print("Question:", q)

        result = run_workflow(q)

        print("\nResult:")
        print(result)