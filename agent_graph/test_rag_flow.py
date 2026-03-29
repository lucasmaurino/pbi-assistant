from informational.rag.vector_store import search

tests = [
    "What is Payments Modernization about?",
    "What does PBI-102 focus on?",
    "How are PBIs supposed to move to Done?",
    "Why is validation being refactored?"
]

for q in tests:
    print("User:", q)
    results = search(q, k=2)

    for r in results:
        print("-", r.page_content[:200], "...")
    print("-" * 60)
