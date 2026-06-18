from memory.memory_store import save_memory, get_memory

save_memory(
    "What are the top 5 products by revenue?",
    "sql_agent",
    "top products result"
)

memory = get_memory()

print(memory["last_question"])