from memory.memory_store import save_memory, get_memory

save_memory(
    "What are the top 5 products by revenue?",
    "sql_agent",
    "phone, tablet, headphones"
)

print(get_memory())