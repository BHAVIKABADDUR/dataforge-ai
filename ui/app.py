# ui/app.py
# DataForge AI — Streamlit Chat Interface

import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.langgraph_workflow import app, get_memory

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="DataForge AI",
    page_icon="🤖",
    layout="wide"
)

# ── Header ─────────────────────────────────────────────────
st.title("🤖 DataForge AI")
st.caption("Agentic AI for Retail Analytics — powered by LangGraph + Groq")

# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.header("About DataForge AI")
    st.markdown("""
    **DataForge AI** is a multi-agent system that answers 
    questions about the RetailIQ data warehouse.
    
    **Agents:**
    - 🔍 SQL Agent — queries warehouse
    - 📊 Analytics Agent — explains trends
    - 📚 Documentation Agent — describes schema
    - ⚙️ ETL Agent — generates PySpark code
    
    **Try asking:**
    - What are the top 5 products by revenue?
    - Why is Asia outperforming Europe?
    - Explain the fact_sales table.
    - Create a Gold table for revenue by region.
    """)

    st.divider()

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ── Chat History ───────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat Input ─────────────────────────────────────────────
if prompt := st.chat_input("Ask anything about RetailIQ..."):

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Run workflow
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = app.invoke({"question": prompt})
                final_answer = result["final_answer"]
                agent_used = result.get("selected_agent", "unknown")

                # Show which agent was used
                st.caption(f"Agent: {agent_used}")

                # Display answer
                st.markdown(final_answer)

                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_answer
                })

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })