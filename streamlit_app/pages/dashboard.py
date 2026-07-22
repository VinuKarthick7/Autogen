"""Live dashboard for a locally analyzed repository."""

from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from api_client import analyze_repository, browse_folders, latest_analysis, recent_analyses


def _current_analysis() -> dict | None:
    if "repository_analysis" in st.session_state:
        return st.session_state.repository_analysis
    analysis, error = latest_analysis()
    if analysis:
        st.session_state.repository_analysis = analysis
        return analysis
    if error and "No repository has been analyzed" not in error:
        st.caption(error)
    return None


def _clear_analysis() -> None:
    """Clear widget-backed values before Streamlit creates the form widgets."""
    st.session_state.pop("repository_path", None)
    st.session_state.pop("repository_analysis", None)


def _analysis_form() -> None:
    st.subheader("Analyze a repository")
    recent, _ = recent_analyses()
    if recent:
        recent_paths = [item["path"] for item in recent]
        selected = st.selectbox("Recent repositories", options=[""] + recent_paths, format_func=lambda value: "Select a recent repository" if not value else value, key="recent_repository")
        if selected and st.button("Use selected repository"):
            st.session_state.repository_path = selected
            st.rerun()
    if st.button("Browse Folder"):
        st.session_state.show_folder_browser = not st.session_state.get("show_folder_browser", False)
    if st.session_state.get("show_folder_browser"):
        browser_root = st.text_input("Server folder to browse", value=st.session_state.get("browse_root", str(Path.cwd().parent)), key="browse_root")
        if st.button("List folders"):
            listing, error = browse_folders(browser_root)
            if error:
                st.error(error)
            else:
                st.session_state.folder_listing = listing["directories"]
        folders = st.session_state.get("folder_listing", [])
        if folders:
            folder_paths = [item["path"] for item in folders]
            selected_folder = st.selectbox("Available folders", folder_paths, key="selected_folder")
            if st.button("Use this folder"):
                st.session_state.repository_path = selected_folder
                st.rerun()
    with st.form("repository-analysis"):
        path = st.text_input("Repository path", key="repository_path", placeholder=r"C:\projects\PMS\pinesphere_backend")
        scan, clear = st.columns((1, 0.22))
        submitted = scan.form_submit_button("Analyze Repository", type="primary", use_container_width=True)
        clear.form_submit_button("Clear", use_container_width=True, on_click=_clear_analysis)
    if not submitted:
        return
    path = st.session_state.repository_path.strip()
    if not path:
        st.error("Enter a repository path before starting analysis.")
        return
    with st.spinner("Scanning files, source code, imports, APIs, and models..."):
        analysis, error = analyze_repository(path)
    if error:
        st.error(f"Analysis failed: {error}")
        return
    st.session_state.repository_analysis = analysis
    st.rerun()


def _render_analysis(analysis: dict) -> None:
    st.success(f"Analyzed **{analysis['repository_name']}** · {analysis['path']}")
    scanned_at = datetime.fromisoformat(analysis["scanned_at"].replace("Z", "+00:00"))
    st.caption(f"Last scanned {scanned_at.strftime('%d %b %Y, %H:%M UTC')} · {analysis['scan_duration_ms'] / 1000:.2f} seconds" + (" · cached result" if analysis.get("cached") else ""))
    cards = st.columns(6)
    for card, label, value in zip(cards, ("Repository", "Total files", "API endpoints", "Database models", "Test files", "Repository health"), (analysis["repository_name"], f"{analysis['files']:,}", analysis["api_endpoints"], analysis["database_models"], analysis["tests"], f"{analysis['health_score']}/100")):
        card.metric(label, value)

    languages = pd.DataFrame(analysis["languages"].items(), columns=["Language", "Files"])
    left, right = st.columns((1.25, 1))
    with left:
        st.subheader("Language composition")
        if languages.empty:
            st.info("No source files were found in this repository.")
        else:
            chart = px.treemap(languages, path=["Language"], values="Files", color="Files", color_continuous_scale="Purples")
            chart.update_layout(coloraxis_showscale=False, margin={"l": 0, "r": 0, "t": 15, "b": 0}, height=330)
            st.plotly_chart(chart, use_container_width=True)
    with right:
        st.subheader("Repository health")
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=analysis["health_score"], number={"suffix": "/100"}, gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#14B8A6"}, "steps": [{"range": [0, 60], "color": "#FEE2E2"}, {"range": [60, 80], "color": "#FEF3C7"}, {"range": [80, 100], "color": "#D1FAE5"}]}))
        gauge.update_layout(margin={"l": 20, "r": 20, "t": 35, "b": 5}, height=250)
        st.plotly_chart(gauge, use_container_width=True)
        st.progress(analysis["health_score"], text=f"{analysis['todos']} TODO markers · {analysis['circular_imports']} circular imports detected")

    st.subheader("Analysis inventory")
    inventory = pd.DataFrame([{"Signal": label, "Count": analysis[key]} for label, key in (("Directories", "directories"), ("Python modules", "python_modules"), ("Functions", "functions"), ("Classes", "classes"), ("Symbols", "symbols"), ("Imports", "imports"))])
    st.dataframe(inventory, use_container_width=True, hide_index=True)
    with st.expander("Health score evidence"):
        st.dataframe(pd.DataFrame(analysis["health_checks"]), use_container_width=True, hide_index=True)


def render() -> None:
    st.title("Engineering command center")
    st.caption("Analyze one real repository and explore its codebase intelligence.")
    _analysis_form()
    analysis = _current_analysis()
    if analysis:
        _render_analysis(analysis)
    else:
        st.info("Enter a repository path and select **Analyze Repository** to populate the dashboard with live results.")


render()
