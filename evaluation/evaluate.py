from agents.planner_agent import planner_agent


test_cases = [
    {
        "question": "What are the top 5 products by revenue?",
        "expected_agent": "sql_agent"
    },
    {
        "question": "Why is Asia outperforming Europe?",
        "expected_agent": "analytics_agent"
    },
    {
        "question": "Explain the fact_sales table.",
        "expected_agent": "documentation_agent"
    },
    {
        "question": "Create a Gold table for revenue by region.",
        "expected_agent": "etl_agent"
    },
    {
        "question": "Show monthly revenue trends.",
        "expected_agent": "sql_agent"
    },
    {
        "question": "What customer insights can you provide?",
        "expected_agent": "analytics_agent"
    },
    {
        "question": "Describe dim_product.",
        "expected_agent": "documentation_agent"
    },
    {
        "question": "Generate PySpark code for customer aggregation.",
        "expected_agent": "etl_agent"
    }
]


def evaluate_planner():

    passed = 0
    total = len(test_cases)

    print("\n" + "=" * 80)
    print("PLANNER AGENT EVALUATION")
    print("=" * 80)

    for test in test_cases:

        question = test["question"]
        expected = test["expected_agent"]

        selected = planner_agent(question)

        success = selected == expected

        if success:
            passed += 1

        print("\nQuestion:")
        print(question)

        print("\nExpected:")
        print(expected)

        print("\nSelected:")
        print(selected)

        print("\nResult:")
        print("PASS" if success else "FAIL")

        print("-" * 80)

    accuracy = (passed / total) * 100

    print("\n" + "=" * 80)
    print(f"Final Score: {passed}/{total}")
    print(f"Accuracy: {accuracy:.2f}%")
    print("=" * 80)


if __name__ == "__main__":
    evaluate_planner()