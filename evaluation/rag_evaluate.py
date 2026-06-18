from rag.retriever import retrieve


test_cases = [

    (
        "What columns exist in dim_product?",
        "dim_product"
    ),

    (
        "Explain the fact_sales table.",
        "fact_sales"
    ),

    (
        "What customer information is stored?",
        "dim_customer"
    ),

    (
        "What region information exists?",
        "dim_region"
    ),

    (
        "What date attributes are available?",
        "dim_date"
    )

]


passed = 0

print("\n" + "=" * 80)
print("RAG RETRIEVAL EVALUATION")
print("=" * 80)

for question, expected in test_cases:

    docs = retrieve(question)

    retrieved_text = "\n".join(docs)

    success = expected.lower() in retrieved_text.lower()

    print("\nQuestion:")
    print(question)

    print("\nExpected Chunk:")
    print(expected)

    print("\nResult:")
    print("PASS" if success else "FAIL")

    print("-" * 80)

    if success:
        passed += 1


accuracy = (passed / len(test_cases)) * 100

print("\n" + "=" * 80)
print(f"Score: {passed}/{len(test_cases)}")
print(f"Accuracy: {accuracy:.2f}%")
print("=" * 80)