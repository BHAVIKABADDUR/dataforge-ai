from agents.planner_agent import planner_agent
from agents.sql_agent import sql_agent
from agents.analytics_agent import analytics_agent

def run_workflow(question):

    selected_agent = planner_agent(question)

    print("\n" + "=" * 60)
    print("Planner Selected:", selected_agent)

    if selected_agent == "sql_agent":

        sql, columns, rows = sql_agent(question)

        return {
            "agent": "sql_agent",
            "sql": sql,
            "columns": columns,
            "rows": rows
        }

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

    else:

        return {
            "agent": selected_agent,
            "message": "Agent not implemented yet."
        }


if __name__ == "__main__":

    questions = [
        "What are the top 5 products by revenue?",
        "Why is Asia outperforming Europe?",
        "Explain the fact_sales table."
    ]

    for q in questions:

        print("\n" + "=" * 80)
        print("Question:", q)

        result = run_workflow(q)

        print("\nResult:")
        print(result)