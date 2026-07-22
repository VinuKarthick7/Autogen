"""Autonomous Engineering Cockpit demo entrypoint."""

from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Autonomous Engineering Cockpit",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_styles() -> None:
    """Apply the small shared visual system without blocking the application."""
    try:
        css = (Path(__file__).parent / "assets" / "styles.css").read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception:
        pass


load_styles()
st.sidebar.markdown("## ◈ AEC")
st.sidebar.caption("AUTONOMOUS ENGINEERING COCKPIT")
st.sidebar.divider()

pages = [
    st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    st.Page("pages/repository_intelligence.py", title="Repository Intelligence", icon=":material/account_tree:"),
    st.Page("pages/observability.py", title="Observability", icon=":material/monitoring:"),
    st.Page("pages/organization.py", title="Organization", icon=":material/groups:"),
    st.Page("pages/laboratory.py", title="Laboratory", icon=":material/science:"),
]

st.sidebar.divider()
st.sidebar.success("Demo environment · healthy")
st.navigation(pages, position="sidebar").run()
