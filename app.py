import streamlit as st
from agents import run_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS (Streamlit-native injection, no HTML components) ───────────────
st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700&family=DM+Sans:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── App shell ── */
    .block-container {
        max-width: 1100px;
        padding: 2.5rem 2rem 4rem;
    }

    /* ── Hero header ── */
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 16px;
        padding: 2.4rem 2.8rem;
        margin-bottom: 2rem;
        border: 1px solid #334155;
    }
    .hero h1 {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        color: #f8fafc;
        margin: 0 0 0.4rem;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: #94a3b8;
        margin: 0;
        font-size: 1rem;
    }

    /* ── Search bar area ── */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1.5px solid #334155;
        background: #0f172a;
        color: #f1f5f9;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        font-family: 'DM Sans', sans-serif;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.2);
    }
    .stTextInput > label {
        color: #cbd5e1;
        font-weight: 500;
        font-size: 0.9rem;
    }

    /* ── Button ── */
    .stButton > button {
        background: #6366f1;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 2rem;
        font-size: 0.95rem;
        font-weight: 600;
        font-family: 'DM Sans', sans-serif;
        transition: background 0.2s, transform 0.1s;
        width: 100%;
    }
    .stButton > button:hover {
        background: #4f46e5;
        transform: translateY(-1px);
    }
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* ── Result cards ── */
    .result-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        height: 100%;
    }
    .result-card h3 {
        font-family: 'Syne', sans-serif;
        font-size: 1rem;
        color: #6366f1;
        margin: 0 0 1rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 0.78rem;
    }
    .result-card p, .result-card li {
        color: #cbd5e1;
        line-height: 1.75;
        font-size: 0.95rem;
    }

    /* ── Section divider ── */
    .section-label {
        font-family: 'Syne', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #475569;
        margin-bottom: 0.5rem;
    }

    /* ── Score badge ── */
    .score-badge {
        display: inline-block;
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.3rem 0.9rem;
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        color: #a5b4fc;
        margin-bottom: 1rem;
    }

    /* ── Spinner text ── */
    .stSpinner > div {
        color: #6366f1 !important;
    }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #64748b;
        border-radius: 8px 8px 0 0;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        padding: 0.5rem 1.2rem;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: #1e293b !important;
        color: #a5b4fc !important;
        border-bottom: 2px solid #6366f1;
    }

    /* ── Streamlit dark override ── */
    .stApp {
        background-color: #020817;
    }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔬 Multi-Agent Research System</h1>
    <p>Search → Scrape → Write → Critique &nbsp;·&nbsp; Powered by AI agents</p>
</div>
""", unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")

with col_input:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of large language models on healthcare",
        label_visibility="collapsed",
    )

with col_btn:
    run = st.button("Run →", use_container_width=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── Pipeline ──────────────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.warning("⚠️  Please enter a research topic before running.")
    else:
        with st.spinner("Running agents  ·  search → scrape → write → critique…"):
            report, critique = run_pipeline(topic)

        # ── Tabs: Report / Critique / Raw ─────────────────────────────────
        tab_report, tab_critique = st.tabs(["📄  Report", "🧠  Critique"])

        with tab_report:
            # Parse sections out of the report for clean display
            sections = {}
            current = None
            buffer = []
            headings = ["Introduction:", "Key Insights:", "Conclusion:", "Sources:"]

            for line in report.splitlines():
                stripped = line.strip()
                if stripped in headings:
                    if current:
                        sections[current] = "\n".join(buffer).strip()
                    current = stripped.rstrip(":")
                    buffer = []
                else:
                    buffer.append(line)

            if current:
                sections[current] = "\n".join(buffer).strip()

            if sections:
                for heading, body in sections.items():
                    st.markdown(f"<p class='section-label'>{heading}</p>", unsafe_allow_html=True)
                    st.markdown(body)
                    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            else:
                # Fallback: just render the raw text
                st.markdown(report)

        with tab_critique:
            # Pull score line out for a badge if present
            score_line = ""
            critique_body_lines = []
            for line in critique.splitlines():
                if line.strip().lower().startswith("score:"):
                    score_line = line.strip().replace("Score:", "").replace("score:", "").strip()
                else:
                    critique_body_lines.append(line)

            if score_line:
                st.markdown(
                    f"<div class='score-badge'>⭐ {score_line}</div>",
                    unsafe_allow_html=True,
                )

            critique_body = "\n".join(critique_body_lines).strip()

            # Parse critique sections similarly
            crit_sections = {}
            c_current = None
            c_buffer = []
            c_headings = ["Strengths:", "Improvements:", "Verdict:"]

            for line in critique_body.splitlines():
                stripped = line.strip()
                if stripped in c_headings:
                    if c_current:
                        crit_sections[c_current] = "\n".join(c_buffer).strip()
                    c_current = stripped.rstrip(":")
                    c_buffer = []
                else:
                    c_buffer.append(line)

            if c_current:
                crit_sections[c_current] = "\n".join(c_buffer).strip()

            if crit_sections:
                for heading, body in crit_sections.items():
                    st.markdown(f"<p class='section-label'>{heading}</p>", unsafe_allow_html=True)
                    st.markdown(body)
                    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            else:
                st.markdown(critique_body)

        # ── Download (plain text, no HTML component) ──────────────────────
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        download_text = f"TOPIC: {topic}\n\n{'='*60}\nREPORT\n{'='*60}\n\n{report}\n\n{'='*60}\nCRITIQUE\n{'='*60}\n\n{critique}"

        st.download_button(
            label="⬇  Download report (.txt)",
            data=download_text.encode("utf-8"),
            file_name=f"report_{topic[:40].replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=False,
        )