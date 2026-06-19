# ui/app.py
# DataForge AI — Streamlit Chat Interface (Refined · 4 KPIs · Fixed Sidebar)

import pandas as pd
import plotly.express as px
import streamlit as st
import sys
import os
import time
import json
import html
from pathlib import Path
from uuid import uuid4

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graph.langgraph_workflow import app, get_memory

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="DataForge AI",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design System ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap');

:root {
  --bg:         #F4F5F7;
  --surface:    #FFFFFF;
  --surface-2:  #FAFAFB;
  --ink:        #0B1220;
  --ink-2:      #2A3142;
  --muted:      #6B7280;
  --subtle:     #9CA3AF;
  --line:       #E5E7EB;
  --line-2:     #EEF0F3;
  --accent:     #B8821B;
  --accent-soft:#FBF3DF;
  --indigo:     #3D52A0;
  --plum:       #6D4BC4;
  --rose:       #B83A5C;
  --green:      #0F9D6E;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--ink) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 13px !important;
}
[data-testid="stMain"],
[data-testid="stAppViewBlockContainer"],
.main .block-container {
  background: var(--bg) !important;
  padding: 0 !important;
  max-width: 100% !important;
}

/* ── Sidebar — all layers ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
[data-testid="stSidebar"] section,
section[data-testid="stSidebar"] {
  background: #FFFFFF !important;
  background-color: #FFFFFF !important;
}
[data-testid="stSidebar"] {
  border-right: 1px solid #E5E7EB !important;
  min-width: 236px !important;
  max-width: 236px !important;
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
  transform: none !important;
  position: relative !important;
  left: 0 !important;
  flex-shrink: 0 !important;
}
/* Keep sidebar expanded — hide collapse/toggle buttons */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
button[aria-label="Close sidebar"],
button[aria-label="open sidebar"],
button[aria-label="collapse sidebar"] {
  display: none !important;
}
/* Prevent sidebar from being pushed off-screen */
section[data-testid="stSidebar"][aria-expanded="false"] {
  margin-left: 0 !important;
  transform: none !important;
  display: block !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] > div {
  display: block !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
  font-family: 'Inter', sans-serif !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: 6px !important;
  color: #2A3142 !important;
  font-size: 12.5px !important;
  font-weight: 400 !important;
  padding: 6px 10px !important;
  width: 100% !important;
  text-align: left !important;
  font-family: 'Inter', sans-serif !important;
  box-shadow: none !important;
  transition: background .12s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: #EEF0F3 !important;
  color: #0B1220 !important;
}
[data-testid="stSidebar"] button[kind="primary"] {
  background: #FBF3DF !important;
  border-color: #F0DCA0 !important;
  color: #7A5511 !important;
  font-weight: 600 !important;
  box-shadow: inset 3px 0 0 #B8821B !important;
}

/* Main buttons */
.main .stButton > button {
  background: #FFFFFF !important;
  border: 1px solid #E5E7EB !important;
  border-radius: 6px !important;
  color: #2A3142 !important;
  font-size: 12px !important;
  font-family: 'Inter', sans-serif !important;
  padding: 6px 14px !important;
  box-shadow: none !important;
}
.main .stButton > button:hover {
  background: #FAFAFB !important;
  border-color: #D1D5DB !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
  background: #FFFFFF !important;
  border: 1px solid #E5E7EB !important;
  border-radius: 12px !important;
  padding: 16px 18px !important;
  margin-bottom: 12px !important;
  box-shadow: 0 1px 3px rgba(11,18,32,0.04) !important;
}

/* Chat input */
[data-testid="stBottom"],
[data-testid="stBottom"] > div {
  background: #FFFFFF !important;
  border-top: 1px solid #E5E7EB !important;
}
[data-testid="stChatInput"] {
  background: #FAFAFB !important;
  border: 1px solid #E5E7EB !important;
  border-radius: 10px !important;
  font-size: 13px !important;
}
[data-testid="stChatInput"] textarea {
  color: #0B1220 !important;
  font-family: 'Inter', sans-serif !important;
}

/* Code */
.stCodeBlock, pre, code {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 12px !important;
}

/* Dataframe / expander */
[data-testid="stDataFrame"] { border: 1px solid #E5E7EB !important; border-radius: 10px !important; }
[data-testid="stExpander"] { border: 1px solid #E5E7EB !important; border-radius: 10px !important; background: #FFFFFF !important; }
[data-testid="stExpander"] summary { font-size: 12px !important; color: #2A3142 !important; }

/* Status */
[data-testid="stStatus"] {
  background: #FFFFFF !important;
  border: 1px solid #E5E7EB !important;
  border-radius: 10px !important;
  font-size: 12px !important;
}

/* Loading skeleton */
@keyframes dataforge-pulse {
  0%, 100% { opacity: .45; }
  50% { opacity: 1; }
}
.df-skeleton {
  background:#FFFFFF;border:1px solid #E5E7EB;border-radius:12px;
  padding:18px;margin-bottom:12px;
}
.df-skeleton-line {
  height:10px;border-radius:999px;background:#E5E7EB;
  margin-bottom:10px;animation:dataforge-pulse 1.25s ease-in-out infinite;
}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] { gap: 6px; }
[data-testid="stTabs"] button[role="tab"] {
  background:#FFFFFF;border:1px solid #E5E7EB;border-radius:8px 8px 0 0;
  padding:8px 14px;font-size:11.5px;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  background:#0B1220;color:#FFFFFF;border-color:#0B1220;
}

/* Checkbox */
[data-testid="stCheckbox"] label { font-size: 12px !important; color: #2A3142 !important; }

hr { border-color: #E5E7EB !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Inline-style HTML atoms ───────────────────────────────

S = "font-family:Inter,sans-serif;"  # shorthand

def agent_pill_html(agent_key):
    cfg = {
        "sql_agent":           ("#FBF3DF", "#B8821B", "#F0DCA0", "◆ SQL Agent"),
        "analytics_agent":     ("#EEF1FB", "#3D52A0", "#C9D2EE", "◈ Analytics"),
        "documentation_agent": ("#F2EEFC", "#6D4BC4", "#D6C9F2", "❡ Docs · RAG"),
        "etl_agent":           ("#FCEDF1", "#B83A5C", "#F4C7D2", "⚙ ETL · PySpark"),
    }
    bg, fg, bd, label = cfg.get(agent_key, ("#F4F5F7", "#2A3142", "#E5E7EB", "🤖 Agent"))
    return (
        f'<span style="display:inline-flex;align-items:center;gap:6px;'
        f'background:{bg};color:{fg};border:1px solid {bd};'
        f'border-radius:999px;padding:3px 11px;font-size:11px;font-weight:500;'
        f'{S}margin-bottom:12px;">{label}</span>'
    )

def metric_card_html(label, value):
    return (
        f'<div style="background:#FFFFFF;border:1px solid #E5E7EB;'
        f'border-left:3px solid #B8821B;border-radius:10px;'
        f'padding:18px 22px;display:inline-block;min-width:200px;">'
        f'<div style="font-size:10px;font-weight:600;text-transform:uppercase;'
        f'letter-spacing:0.12em;color:#9CA3AF;{S}">{label.replace("_"," ")}</div>'
        f'<div style="font-family:Fraunces,serif;font-size:32px;font-weight:600;'
        f'color:#0B1220;margin-top:4px;letter-spacing:-0.02em;">{value}</div>'
        f'</div>'
    )

def nav_label(text):
    return (
        f'<div style="font-size:10px;font-weight:600;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:#9CA3AF;{S}'
        f'margin:18px 4px 8px 4px;">{text}</div>'
    )

def nav_item(icon, text, active=False, badge=None):
    bg    = "background:#FBF3DF;box-shadow:inset 2px 0 0 #B8821B;" if active else ""
    fw    = "font-weight:500;" if active else "font-weight:400;"
    badge_html = (
        f'<span style="margin-left:auto;background:#E5E7EB;color:#6B7280;'
        f'font-size:10px;padding:1px 7px;border-radius:999px;{S}">{badge}</span>'
        if badge is not None else ""
    )
    return (
        f'<div style="display:flex;align-items:center;gap:9px;padding:7px 10px;'
        f'border-radius:6px;color:#0B1220;font-size:13px;{fw}{bg}{S}'
        f'margin-bottom:1px;">{icon} {text}{badge_html}</div>'
    )

def agent_dot_item(color, text):
    return (
        f'<div style="display:flex;align-items:center;gap:9px;padding:5px 10px;'
        f'font-size:12px;color:#2A3142;{S}">'
        f'<div style="width:6px;height:6px;border-radius:50%;'
        f'background:{color};flex-shrink:0;"></div>{text}</div>'
    )

def agent_status_card(icon, bg, name, sub):
    return (
        f'<div style="display:flex;align-items:center;gap:10px;'
        f'background:#FFFFFF;border:1px solid #E5E7EB;border-radius:10px;'
        f'padding:10px 12px;margin-bottom:6px;">'
        f'<div style="width:30px;height:30px;border-radius:7px;background:{bg};'
        f'display:grid;place-items:center;font-size:14px;flex-shrink:0;">{icon}</div>'
        f'<div>'
        f'<div style="font-size:12.5px;font-weight:500;color:#0B1220;{S}">{name}</div>'
        f'<div style="font-size:10.5px;color:#9CA3AF;{S};margin-top:1px;">{sub}</div>'
        f'</div>'
        f'<div style="margin-left:auto;width:7px;height:7px;border-radius:50%;'
        f'background:#0F9D6E;box-shadow:0 0 0 3px rgba(15,157,110,0.12);"></div>'
        f'</div>'
    )

def stat_row(key, val, last=False):
    border = "" if last else "border-bottom:1px solid #EEF0F3;"
    return (
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'padding:8px 0;{border}">'
        f'<span style="font-size:12.5px;color:#6B7280;{S}">{key}</span>'
        f'<span style="font-size:12px;font-weight:500;color:#0B1220;'
        f'font-family:JetBrains Mono,monospace;font-variant-numeric:tabular-nums;">{val}</span>'
        f'</div>'
    )

def routing_bar(label, color, count, pct):
    return (
        f'<div style="margin-bottom:10px;">'
        f'<div style="display:flex;justify-content:space-between;'
        f'font-size:11px;color:#2A3142;{S}margin-bottom:4px;">'
        f'<span>{label}</span>'
        f'<span style="color:#6B7280;">{count} · {pct}%</span></div>'
        f'<div style="height:4px;background:#EEF0F3;border-radius:999px;">'
        f'<div style="width:{pct}%;height:100%;background:{color};border-radius:999px;"></div>'
        f'</div></div>'
    )


SAVED_QUERIES_FILE = Path(__file__).with_name("saved_queries.json")


def load_saved_queries():
    try:
        if SAVED_QUERIES_FILE.exists():
            saved = json.loads(SAVED_QUERIES_FILE.read_text(encoding="utf-8"))
            if isinstance(saved, list):
                return saved
    except (OSError, json.JSONDecodeError):
        pass
    return []


def persist_saved_queries():
    try:
        SAVED_QUERIES_FILE.write_text(
            json.dumps(st.session_state.saved_queries, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return True
    except OSError as exc:
        st.error(f"Could not save queries: {exc}")
        return False


# ── Session State ─────────────────────────────────────────
for k, v in {
    "messages": [], "pending_prompt": None,
    "agent_counts": {}, "total_questions": 0,
    "last_elapsed": None, "last_agent": "—",
    "saved_queries": load_saved_queries(), "current_view": "Chat",
    "flash_message": None,
}.items():
    st.session_state.setdefault(k, v)

# Migrate saved queries created by the previous in-memory version.
if st.session_state.saved_queries and isinstance(st.session_state.saved_queries[0], str):
    st.session_state.saved_queries = [
        {"id": uuid4().hex, "title": query[:60], "query": query}
        for query in st.session_state.saved_queries
    ]
    persist_saved_queries()

if st.session_state.flash_message:
    st.toast(st.session_state.flash_message)
    st.session_state.flash_message = None


@st.dialog("Delete saved query?")
def confirm_delete_query(query_id):
    saved_query = next(
        (item for item in st.session_state.saved_queries if item["id"] == query_id),
        None,
    )
    if not saved_query:
        st.info("This query has already been removed.")
        return
    st.write(f'“{saved_query["title"]}” will be permanently removed.')
    cancel_col, delete_col = st.columns(2)
    with cancel_col:
        if st.button("Cancel", use_container_width=True, key=f"cancel_delete_{query_id}"):
            st.rerun()
    with delete_col:
        if st.button("Delete query", type="primary", use_container_width=True, key=f"confirm_delete_{query_id}"):
            st.session_state.saved_queries = [
                item for item in st.session_state.saved_queries if item["id"] != query_id
            ]
            persist_saved_queries()
            st.session_state.flash_message = "Saved query deleted"
            st.rerun()


@st.dialog("Clear this conversation?")
def confirm_clear_session():
    st.write("Messages and session statistics will be cleared. Your saved queries will remain available.")
    cancel_col, clear_col = st.columns(2)
    with cancel_col:
        if st.button("Cancel", use_container_width=True, key="cancel_clear"):
            st.rerun()
    with clear_col:
        if st.button("Clear conversation", type="primary", use_container_width=True, key="confirm_clear"):
            st.session_state.messages = []
            st.session_state.agent_counts = {}
            st.session_state.total_questions = 0
            st.session_state.last_elapsed = None
            st.session_state.last_agent = "—"
            st.session_state.flash_message = "Conversation cleared"
            st.rerun()


# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:

    # App header
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;'
        f'padding:4px 4px 16px 4px;border-bottom:1px solid #E5E7EB;margin-bottom:18px;">'
        f'<div style="width:32px;height:32px;background:#0B1220;border-radius:8px;'
        f'display:grid;place-items:center;color:#FFFFFF;font-weight:600;font-size:13px;">DF</div>'
        f'<div>'
        f'<div style="font-family:Fraunces,serif;font-size:16px;font-weight:600;'
        f'color:#0B1220;letter-spacing:-0.01em;line-height:1.1;">DataForge</div>'
        f'<div style="font-size:10.5px;color:#9CA3AF;{S}margin-top:2px;">RetailIQ Warehouse</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # Workspace nav
    st.markdown(nav_label("Workspace"), unsafe_allow_html=True)
    hist = len([m for m in st.session_state.messages if m["role"] == "user"])
    if st.button(
        "💬  Chat",
        key="nav_chat",
        use_container_width=True,
        type="primary" if st.session_state.current_view == "Chat" else "secondary",
    ):
        st.session_state.current_view = "Chat"
        st.rerun()
    st.markdown(nav_item("🕐", "History", badge=hist), unsafe_allow_html=True)
    if st.button(
        f"📌  Saved queries ({len(st.session_state.saved_queries)})",
        key="nav_saved_queries",
        use_container_width=True,
        type="primary" if st.session_state.current_view == "Saved Queries" else "secondary",
    ):
        st.session_state.current_view = "Saved Queries"
        st.rerun()

    st.markdown(nav_label("Agents"), unsafe_allow_html=True)
    for color, name in [
        ("#B8821B", "SQL"),
        ("#3D52A0", "Analytics"),
        ("#6D4BC4", "Documentation"),
        ("#B83A5C", "ETL · PySpark"),
    ]:
        st.markdown(agent_dot_item(color, name), unsafe_allow_html=True)

    st.markdown(nav_label("Quick Queries"), unsafe_allow_html=True)
    for label in [
        "Top products by revenue",
        "Monthly revenue trend",
        "Region performance",
        "Gold table: revenue",
    ]:
        if st.button(f"→  {label}", key=f"qq_{label}"):
            st.session_state.pending_prompt = label

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="border:1px solid #E5E7EB;border-radius:8px;'
        f'padding:10px 12px;background:#FAFAFB;">'
        f'<div style="font-size:12px;font-weight:500;color:#0B1220;{S}">📁 Retail_Data_Warehouse</div>'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:10.5px;'
        f'color:#6B7280;margin-top:2px;">⎇ master</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑 Reset", key="reset_btn", use_container_width=True):
            confirm_clear_session()
    with c2:
        if st.session_state.messages:
            data = "\n\n".join(f"[{m['role'].upper()}]\n{m['content']}" for m in st.session_state.messages)
            st.download_button("📥 Export", data=data, file_name="dataforge.txt",
                               mime="text/plain", use_container_width=True, key="export_btn")


# ── Chart builder ─────────────────────────────────────────
def auto_chart(df, question):
    if df is None or df.empty or len(df.columns) < 2:
        return
    q = question.lower()
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()
    if not num_cols or not cat_cols:
        return
    x, y = cat_cols[0], num_cols[0]

    if any(w in q for w in ["trend", "monthly", "month", "year", "over time"]):
        fig = px.line(df, x=x, y=y, markers=True, color_discrete_sequence=["#B8821B"])
        fig.update_traces(line=dict(width=2.2))
    elif any(w in q for w in ["share", "percentage", "breakdown"]) and len(df) <= 8:
        fig = px.pie(df, names=x, values=y,
                     color_discrete_sequence=["#B8821B","#3D52A0","#6D4BC4","#B83A5C","#0F9D6E"])
        fig.update_traces(marker=dict(line=dict(color="#fff", width=2)))
    else:
        fig = px.bar(df.sort_values(y, ascending=False), x=x, y=y,
                     color_discrete_sequence=["#B8821B"])
        fig.update_traces(marker_line_width=0)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#6B7280", size=11),
        margin=dict(t=36, b=20, l=4, r=4), height=255,
        xaxis=dict(showgrid=False, linecolor="#E5E7EB"),
        yaxis=dict(gridcolor="#EEF0F3", linecolor="#E5E7EB"),
        showlegend=False, bargap=0.35,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_result_tabs(prompt, final_answer, agent, generated_sql=None, columns=None, rows=None, raw_result=""):
    """Render one response using a consistent analytics workspace pattern."""
    insight_tab, records_tab, query_tab, visual_tab = st.tabs(
        ["✦ Insight", "▦ Records", "⌘ Query", "◈ Visual"]
    )

    df = pd.DataFrame(rows, columns=columns) if columns and rows else None

    # For ETL agent, PySpark code may land in final_answer instead of raw_result.
    # Detect code and route it to the Query tab; show a summary in Insight instead.
    is_etl = agent == "etl_agent"
    pyspark_code = ""
    etl_summary = final_answer
    if is_etl:
        code_candidate = raw_result.strip() if (raw_result and raw_result.strip()) else final_answer.strip()
        looks_like_code = (
            "pyspark" in code_candidate.lower()
            or code_candidate.startswith("from ")
            or code_candidate.startswith("import ")
            or ".groupBy(" in code_candidate
            or ".withColumn" in code_candidate
            or "spark." in code_candidate
        )
        if looks_like_code:
            pyspark_code = code_candidate
            etl_summary = (
                "PySpark ETL script generated. "
                "View the code in the **⌘ Query** tab."
            )

    with insight_tab:
        if is_etl and pyspark_code:
            st.markdown(
                f'<div style="color:#9CA3AF;font-size:12.5px;font-style:italic;'
                f'font-family:Inter,sans-serif;padding:4px 0;">'
                f'⌘ PySpark ETL script generated — see the <b>Query</b> tab for the code.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(final_answer)

    with records_tab:
        if df is not None:
            if len(df) == 1 and len(df.columns) == 1:
                st.markdown(
                    metric_card_html(df.columns[0], str(df.iloc[0, 0])),
                    unsafe_allow_html=True,
                )
            else:
                st.caption(f"{len(df):,} rows · {len(df.columns)} columns")
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("This response does not include tabular records.")

    with query_tab:
        if generated_sql:
            st.code(generated_sql, language="sql")
        elif is_etl and pyspark_code:
            st.code(pyspark_code, language="python")
        elif is_etl and raw_result:
            st.code(raw_result, language="python")
        else:
            st.info("No generated query is available for this response.")

    with visual_tab:
        if df is not None and len(df) > 1 and len(df.columns) > 1:
            auto_chart(df, prompt)
        else:
            st.info("A visual needs at least two fields and multiple records.")


# ── Response renderer ─────────────────────────────────────
def render_response(prompt):
    with st.chat_message("assistant"):
        loading = st.empty()
        loading.markdown(
            '<div class="df-skeleton">'
            '<div class="df-skeleton-line" style="width:28%"></div>'
            '<div class="df-skeleton-line" style="width:92%"></div>'
            '<div class="df-skeleton-line" style="width:76%;margin-bottom:0"></div>'
            '</div>',
            unsafe_allow_html=True,
        )
        t0 = time.time()
        try:
            result = app.invoke({"question": prompt})
            elapsed = round(time.time() - t0, 1)
            loading.empty()

            final_answer  = result["final_answer"]
            raw_result    = result.get("result", "")
            agent_used    = result.get("selected_agent", "unknown")
            generated_sql = result.get("generated_sql")
            columns       = result.get("columns")
            rows          = result.get("rows")

            st.session_state.total_questions += 1
            st.session_state.last_elapsed = elapsed
            st.session_state.last_agent = agent_used.replace("_agent", "").upper()
            st.session_state.agent_counts[agent_used] = (
                st.session_state.agent_counts.get(agent_used, 0) + 1
            )

            st.markdown(agent_pill_html(agent_used), unsafe_allow_html=True)
            st.caption(f"Completed in {elapsed:.1f}s")
            render_result_tabs(
                prompt, final_answer, agent_used, generated_sql,
                columns, rows, raw_result,
            )

            row_count = len(rows) if rows else 0

            # Store response with full metadata for rich re-rendering
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_answer,
                "metadata": {
                    "agent": agent_used,
                    "elapsed": elapsed,
                    "sql_generated": bool(generated_sql),
                    "rows": row_count,
                    "columns": columns,
                    "data_rows": rows,
                    "generated_sql": generated_sql,
                    "raw_result": raw_result,
                }
            })

        except Exception as e:
            loading.empty()
            st.error(f"Error: {e}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {e}",
                "metadata": {
                    "agent": "error",
                    "elapsed": 0,
                    "sql_generated": False,
                    "rows": 0
                }
            })


# ── Main layout ───────────────────────────────────────────
# Proportions: Sidebar 18% (native) | Main 60% | Right 22%
# Visible area = [0.73 main, 0.27 right] of remaining space
main_col, right_col = st.columns([0.73, 0.27], gap="small")

with main_col:

    # Workspace header
    view_title = "Saved query library" if st.session_state.current_view == "Saved Queries" else "Ask your warehouse"
    view_subtitle = (
        "Reusable questions for your RetailIQ warehouse"
        if st.session_state.current_view == "Saved Queries"
        else "Explore revenue, customers, products, and operations in plain English."
    )
    st.markdown(
        f'<div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:0 0 12px 12px;'
        f'padding:18px 22px;display:flex;align-items:center;gap:20px;box-shadow:0 1px 2px rgba(11,18,32,.03);">'
        f'<div style="flex:1;min-width:220px;">'
        f'<div style="font-size:9.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;'
        f'color:#B8821B;{S}margin-bottom:4px;">RetailIQ Copilot</div>'
        f'<div style="font-family:Fraunces,serif;font-size:21px;font-weight:600;color:#0B1220;'
        f'letter-spacing:-.02em;line-height:1.15;">{view_title}</div>'
        f'<div style="font-size:11.5px;color:#6B7280;{S}margin-top:4px;">{view_subtitle}</div>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;justify-content:flex-end;">'
        f'<span style="padding:6px 10px;border-radius:8px;background:#F4F5F7;color:#2A3142;'
        f'font-size:11px;font-weight:600;{S}">{st.session_state.total_questions:02d} queries</span>'
        f'<span style="padding:6px 9px;border:1px solid #F0DCA0;border-radius:8px;background:#FFFBF2;'
        f'color:#7A5511;font-size:10.5px;{S}"><b>◆</b> SQL</span>'
        f'<span style="padding:6px 9px;border:1px solid #C9D2EE;border-radius:8px;background:#F7F8FD;'
        f'color:#3D52A0;font-size:10.5px;{S}"><b>◈</b> Analytics</span>'
        f'<span style="padding:6px 9px;border:1px solid #D6C9F2;border-radius:8px;background:#FAF8FE;'
        f'color:#6D4BC4;font-size:10.5px;{S}"><b>❡</b> Docs</span>'
        f'<span style="padding:6px 9px;border:1px solid #F4C7D2;border-radius:8px;background:#FFF8FA;'
        f'color:#B83A5C;font-size:10.5px;{S}"><b>⚙</b> ETL</span>'
        f'<span style="padding:6px 10px;border-radius:999px;background:#ECFDF5;color:#0F7A57;'
        f'font-size:10.5px;font-weight:600;{S}border:1px solid #BBF7D0;">● Live</span>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # KPI strip — 4 cards, pure HTML
    kpi_data = [
        ("$",  "#FBF3DF", "#B8821B", "Total Revenue",  "$67.96<span style='font-size:15px;color:#6B7280;font-family:Inter,sans-serif;'>M</span>", "Real metric · RetailIQDW"),
        ("◉",  "#EEF1FB", "#3D52A0", "Customers",      "8,960",   "Count from <code style='font-family:JetBrains Mono,monospace;font-size:10.5px;background:#F4F5F7;color:#2A3142;border:1px solid #E5E7EB;padding:1px 5px;border-radius:4px;'>dim_customer</code>"),
        ("▦",  "#FCEDF1", "#B83A5C", "Sales Records",  "50,000",  "Count from <code style='font-family:JetBrains Mono,monospace;font-size:10.5px;background:#F4F5F7;color:#2A3142;border:1px solid #E5E7EB;padding:1px 5px;border-radius:4px;'>fact_sales</code>"),
        ("◆",  "#F2EEFC", "#6D4BC4", "Active Agents",  "4",       "SQL · Analytics · Docs · ETL"),
    ]
    cols = st.columns(4)
    for col, (icon, icon_bg, icon_fg, label, val_html, sub) in zip(cols, kpi_data):
        with col:
            st.markdown(
                f'<div style="background:#FFFFFF;border:1px solid #E5E7EB;'
                f'padding:12px 16px;display:flex;flex-direction:column;gap:5px;">'
                f'<div style="display:flex;align-items:center;gap:8px;">'
                f'<div style="width:22px;height:22px;border-radius:5px;background:{icon_bg};'
                f'color:{icon_fg};display:grid;place-items:center;font-size:11px;">{icon}</div>'
                f'<div style="font-size:10px;font-weight:600;text-transform:uppercase;'
                f'letter-spacing:0.12em;color:#9CA3AF;{S}">{label}</div></div>'
                f'<div style="font-family:Fraunces,serif;font-size:20px;font-weight:600;'
                f'color:#0B1220;letter-spacing:-0.02em;line-height:1.1;">{val_html}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Content starts directly below the KPI strip.
    # Do not use an opening HTML wrapper here: Streamlit renders subsequent
    # elements in separate containers, leaving an empty min-height spacer.
    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)

    if st.session_state.current_view == "Saved Queries":
        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #E5E7EB;'
            f'border-radius:12px;padding:22px 24px;margin-bottom:16px;">'
            f'<div style="font-family:Fraunces,serif;font-size:20px;font-weight:600;'
            f'color:#0B1220;">Saved Queries</div>'
            f'<div style="font-size:12px;color:#6B7280;{S}margin-top:5px;">'
            f'{len(st.session_state.saved_queries)} saved '
            f'{"query" if len(st.session_state.saved_queries) == 1 else "queries"}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.saved_queries:
            st.info("No saved queries yet. Run a query, then click Save query.")
        else:
            for saved_query in reversed(st.session_state.saved_queries):
                query_id = saved_query["id"]
                with st.container(border=True):
                    title_col, run_col, delete_col = st.columns([0.68, 0.16, 0.16])
                    with title_col:
                        edited_title = st.text_input(
                            "Query name",
                            value=saved_query["title"],
                            key=f"title_{query_id}",
                            label_visibility="collapsed",
                        )
                    with run_col:
                        if st.button("▶ Run", key=f"run_{query_id}", use_container_width=True):
                            st.session_state.pending_prompt = saved_query["query"]
                            st.session_state.current_view = "Chat"
                            st.rerun()
                    with delete_col:
                        if st.button("Delete", key=f"delete_{query_id}", use_container_width=True):
                            confirm_delete_query(query_id)

                    st.markdown(
                        f'<div style="font-size:12.5px;color:#6B7280;{S}padding:2px 2px 4px;">'
                        f'{html.escape(saved_query["query"])}</div>',
                        unsafe_allow_html=True,
                    )
                    if edited_title.strip() and edited_title.strip() != saved_query["title"]:
                        if st.button("Save renamed title", key=f"rename_{query_id}"):
                            saved_query["title"] = edited_title.strip()
                            persist_saved_queries()
                            st.session_state.flash_message = "Saved query renamed"
                            st.rerun()

    # Empty state — Enterprise Copilot sits directly below the KPI cards
    elif not st.session_state.messages:
        st.markdown(
            f'<div style="text-align:center;padding:32px 24px;border:1px dashed #E5E7EB;'
            f'border-radius:12px;background:#FFFFFF;margin:0;">'
            f'<div style="width:44px;height:44px;margin:0 auto 14px;border-radius:10px;'
            f'background:#0B1220;color:#FFFFFF;display:grid;place-items:center;font-size:18px;">◆</div>'
            f'<div style="font-family:Fraunces,serif;font-size:18px;font-weight:600;'
            f'color:#0B1220;letter-spacing:-0.01em;">Enterprise Analytics Copilot</div>'
            f'<div style="font-size:13px;color:#6B7280;{S}margin-top:12px;'
            f'max-width:380px;margin-left:auto;margin-right:auto;line-height:1.6;">'
            f'<div>✓ Natural-language SQL generation</div>'
            f'<div>✓ Business insight analysis</div>'
            f'<div>✓ Schema exploration with RAG</div>'
            f'<div>✓ PySpark ETL generation</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;'
            f'color:#9CA3AF;{S}margin:16px 0 8px;">Try a starting point</div>',
            unsafe_allow_html=True,
        )
        starter_cols = st.columns(4)
        starter_prompts = [
            ("Revenue trend", "Show the monthly revenue trend"),
            ("Top regions", "Compare revenue performance by region"),
            ("Best products", "Show the top products by revenue"),
            ("Explore schema", "Explain the key warehouse tables and relationships"),
        ]
        for starter_col, (label, starter_prompt) in zip(starter_cols, starter_prompts):
            with starter_col:
                if st.button(label, key=f"starter_{label}", use_container_width=True):
                    st.session_state.pending_prompt = starter_prompt

    # Message stream with enhanced enterprise card styling
    visible_messages = st.session_state.messages if st.session_state.current_view == "Chat" else []
    for msg_index, msg in enumerate(visible_messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                # Extract metadata if available
                metadata = msg.get("metadata", {})
                agent = metadata.get("agent", "—")
                elapsed = metadata.get("elapsed", "—")
                sql_generated = metadata.get("sql_generated", False)
                rows_count = metadata.get("rows", 0)
                columns = metadata.get("columns", [])
                data_rows = metadata.get("data_rows", [])
                generated_sql = metadata.get("generated_sql", "")
                raw_result = metadata.get("raw_result", "")
                
                # Compact response metadata
                st.markdown(
                    f'<div style="background:#FAFAFB;border:1px solid #E5E7EB;'
                    f'border-radius:9px;padding:9px 12px;display:flex;align-items:center;'
                    f'gap:12px;margin-bottom:10px;">'
                    f'<span style="font-weight:500;color:#0B1220;font-size:12px;{S}">{agent}</span>'
                    f'<span style="color:#9CA3AF;font-size:11px;">•</span>'
                    f'<span style="color:#6B7280;font-size:11px;{S}">{elapsed}s</span>'
                    f'<span style="color:#9CA3AF;font-size:11px;">•</span>'
                    f'<span style="color:#6B7280;font-size:11px;{S}">SQL: {"Yes" if sql_generated else "No"}</span>'
                    f'<span style="color:#9CA3AF;font-size:11px;">•</span>'
                    f'<span style="color:#6B7280;font-size:11px;{S}">{rows_count} rows</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                user_prompt = next(
                    (
                        previous["content"]
                        for previous in reversed(visible_messages[:msg_index])
                        if previous["role"] == "user"
                    ),
                    msg["content"],
                )
                render_result_tabs(
                    user_prompt,
                    msg["content"],
                    agent,
                    generated_sql,
                    columns,
                    data_rows,
                    raw_result,
                )
            else:
                st.markdown(msg["content"])

# ── Right panel ───────────────────────────────────────────
with right_col:
    # Session
    st.markdown(
        f'<div style="font-size:10px;font-weight:600;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:#9CA3AF;{S}margin-bottom:12px;">Session</div>',
        unsafe_allow_html=True,
    )
    avg = f"{st.session_state.last_elapsed}s" if st.session_state.last_elapsed else "—"
    st.markdown(
        f'<div style="border:1px solid #E5E7EB;border-radius:10px;padding:12px 14px;background:#FAFAFB;">'
        + stat_row("Queries", f"{st.session_state.total_questions:03d}")
        + stat_row("Last agent", st.session_state.last_agent)
        + stat_row("Last latency", avg, last=True)
        + '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    # Routing breakdown
    if st.session_state.agent_counts:
        st.markdown(
            f'<div style="font-size:10px;font-weight:600;letter-spacing:0.12em;'
            f'text-transform:uppercase;color:#9CA3AF;{S}margin-bottom:12px;">Routing</div>',
            unsafe_allow_html=True,
        )
        total = sum(st.session_state.agent_counts.values())
        COLORS = {"sql_agent":"#B8821B","analytics_agent":"#3D52A0",
                  "documentation_agent":"#6D4BC4","etl_agent":"#B83A5C"}
        for agent, count in st.session_state.agent_counts.items():
            pct = int((count / total) * 100) if total else 0
            st.markdown(
                routing_bar(agent.replace("_agent","").upper(), COLORS.get(agent,"#9CA3AF"), count, pct),
                unsafe_allow_html=True,
            )

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    # Context
    st.markdown(
        f'<div style="font-size:10px;font-weight:600;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:#9CA3AF;{S}margin-bottom:12px;">Context</div>',
        unsafe_allow_html=True,
    )
    mem = get_memory()
    if mem and mem.get("last_question"):
        q = mem["last_question"]
        st.markdown(
            f'<div style="border:1px solid #E5E7EB;border-radius:10px;'
            f'padding:12px 14px;background:#FAFAFB;font-size:12px;'
            f'color:#2A3142;{S}line-height:1.5;">'
            f'<div style="font-size:10px;font-weight:600;letter-spacing:0.1em;'
            f'text-transform:uppercase;color:#9CA3AF;margin-bottom:4px;">Last query</div>'
            f'{q[:120]}{"…" if len(q)>120 else ""}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div style="font-size:12px;color:#9CA3AF;font-style:italic;{S}">No active context.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    # Agent Status
    st.markdown(
        f'<div style="font-size:10px;font-weight:600;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:#9CA3AF;{S}margin-bottom:12px;">Agent Status</div>',
        unsafe_allow_html=True,
    )
    for icon, bg, name, sub in [
        ("◆", "#FBF3DF", "SQL",        "Query engine"),
        ("◈", "#EEF1FB", "Analytics",  "Insight analysis"),
        ("❡", "#F2EEFC", "Docs",       "RAG · schema"),
        ("⚙", "#FCEDF1", "ETL",        "PySpark codegen"),
    ]:
        st.markdown(agent_status_card(icon, bg, name, sub), unsafe_allow_html=True)

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    # Actions
    st.markdown(
        f'<div style="font-size:10px;font-weight:600;letter-spacing:0.12em;'
        f'text-transform:uppercase;color:#9CA3AF;{S}margin-bottom:12px;">Actions</div>',
        unsafe_allow_html=True,
    )
    if st.session_state.messages:
        data = "\n\n".join(f"[{m['role'].upper()}]\n{m['content']}" for m in st.session_state.messages)
        st.download_button("📥 Export chat", data=data, file_name="dataforge.txt",
                           mime="text/plain", use_container_width=True, key="right_export")
    latest_query = next(
        (m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"),
        None,
    )
    if st.button(
        "💾 Save latest query",
        key="save_q",
        use_container_width=True,
        disabled=not latest_query,
    ):
        existing_queries = {item["query"] for item in st.session_state.saved_queries}
        if latest_query not in existing_queries:
            st.session_state.saved_queries.append({
                "id": uuid4().hex,
                "title": latest_query[:60],
                "query": latest_query,
            })
            persist_saved_queries()
            st.session_state.flash_message = "Query saved to your library"
        else:
            st.session_state.flash_message = "Query is already saved"
        st.session_state.current_view = "Saved Queries"
        st.rerun()
    if st.button("🗑 Clear session", key="right_clear", use_container_width=True):
        confirm_clear_session()

# ── Input & dispatch ──────────────────────────────────────
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
    st.session_state.messages.append({"role": "user", "content": prompt})
    with main_col:
        render_response(prompt)
    st.rerun()

if st.session_state.current_view == "Chat" and (prompt := st.chat_input("Ask anything about your RetailIQ warehouse…")):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with main_col:
        render_response(prompt)
    st.rerun()