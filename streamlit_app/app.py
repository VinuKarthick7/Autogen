"""Autonomous Engineering Cockpit entrypoint."""

from pathlib import Path

import streamlit as st


st.set_page_config(page_title="Autonomous Engineering Cockpit", page_icon=":material/hub:", layout="wide", initial_sidebar_state="expanded")


def _load_styles() -> None:
    try:
        css = (Path(__file__).parent / "assets" / "styles.css").read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except OSError:
        pass


_load_styles()
st.sidebar.markdown("## AEC")
st.sidebar.caption("AUTONOMOUS ENGINEERING COCKPIT")
st.sidebar.divider()
pages = [
    st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    st.Page("pages/repository_intelligence.py", title="Repository Intelligence", icon=":material/account_tree:"),
]
st.sidebar.divider()
st.sidebar.caption("Repository analysis workspace")
st.navigation(pages, position="sidebar").run()
