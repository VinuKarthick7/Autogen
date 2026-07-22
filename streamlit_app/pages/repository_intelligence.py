"""Detailed live repository intelligence from the latest scan."""

import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from api_client import latest_analysis


def _analysis() -> dict | None:
    if "repository_analysis" in st.session_state:
        return st.session_state.repository_analysis
    analysis, error = latest_analysis()
    if analysis:
        st.session_state.repository_analysis = analysis
        return analysis
    if error and "No repository has been analyzed" not in error:
        st.error(error)
    return None


def _dependency_graph(edges: list[dict]) -> go.Figure | None:
    nodes = sorted({item["source"] for item in edges} | {item["target"] for item in edges})[:24]
    if not nodes:
        return None
    positions = {node: (math.cos(index * 2 * math.pi / len(nodes)), math.sin(index * 2 * math.pi / len(nodes))) for index, node in enumerate(nodes)}
    x_edges, y_edges = [], []
    for edge in edges:
        if edge["source"] in positions and edge["target"] in positions:
            x_edges.extend([positions[edge["source"]][0], positions[edge["target"]][0], None])
            y_edges.extend([positions[edge["source"]][1], positions[edge["target"]][1], None])
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=x_edges, y=y_edges, mode="lines", line={"color": "#A78BFA", "width": 1}, hoverinfo="skip"))
    figure.add_trace(go.Scatter(x=[positions[node][0] for node in nodes], y=[positions[node][1] for node in nodes], mode="markers+text", text=[node.split(".")[-1] for node in nodes], textposition="top center", marker={"size": 14, "color": "#14B8A6"}, hovertext=nodes, hoverinfo="text"))
    figure.update_layout(showlegend=False, xaxis={"visible": False}, yaxis={"visible": False}, margin={"l": 0, "r": 0, "t": 10, "b": 0}, height=380, plot_bgcolor="rgba(0,0,0,0)")
    return figure


def render() -> None:
    st.title("Repository intelligence")
    st.caption("Static analysis results from the most recently scanned local repository.")
    analysis = _analysis()
    if not analysis:
        st.info("No analysis is available yet. Open **Dashboard**, enter a repository path, and run the scan.")
        return
    cards = st.columns(5)
    for card, label, value in zip(cards, ("Files", "Symbols", "Imports", "API count", "Model count"), (f"{analysis['files']:,}", f"{analysis['symbols']:,}", f"{analysis['imports']:,}", analysis["api_endpoints"], analysis["database_models"])):
        card.metric(label, value)

    left, right = st.columns((1, 1.2))
    with left:
        st.subheader("Language composition")
        source_languages = pd.DataFrame(analysis["source_languages"].items(), columns=["Language", "Files"])
        if source_languages.empty:
            st.info("No source-code languages are available.")
        else:
            chart = px.pie(source_languages, names="Language", values="Files", hole=0.55, color_discrete_sequence=px.colors.sequential.Purples_r)
            chart.update_layout(margin={"l": 0, "r": 0, "t": 15, "b": 0}, height=300)
            st.plotly_chart(chart, use_container_width=True)
        supporting = pd.DataFrame(analysis["supporting_files"].items(), columns=["File type", "Files"])
        with st.expander("Supporting files"):
            st.dataframe(supporting, use_container_width=True, hide_index=True) if not supporting.empty else st.info("No supporting files were found.")
    with right:
        st.subheader("Dependency graph")
        filters = st.columns(4)
        show_api = filters[0].checkbox("Show API modules", value=True)
        show_services = filters[1].checkbox("Show services", value=True)
        show_archived = filters[2].checkbox("Show archived modules", value=False)
        show_tests = filters[3].checkbox("Show tests", value=False)
        allowed_kinds = {"project"}
        if show_api:
            allowed_kinds.add("api")
        if show_services:
            allowed_kinds.add("services")
        if show_archived:
            allowed_kinds.add("archived")
        if show_tests:
            allowed_kinds.add("tests")
        graph = _dependency_graph([edge for edge in analysis["dependency_edges"] if edge["source_kind"] in allowed_kinds])
        if graph:
            st.plotly_chart(graph, use_container_width=True)
        else:
            st.info("No Python import relationships were found.")

    st.subheader("Imports by category")
    standard_tab, third_party_tab, internal_tab = st.tabs(["Standard library", "Third-party packages", "Internal project imports"])
    for tab, category in zip((standard_tab, third_party_tab, internal_tab), ("Standard library", "Third-party packages", "Internal project imports")):
        with tab:
            imports = pd.DataFrame(analysis["imports_by_category"][category])
            st.dataframe(imports, use_container_width=True, hide_index=True) if not imports.empty else st.info(f"No {category.lower()} were found.")

    with st.container():
        st.subheader("Detected API routes")
        routes = pd.DataFrame(analysis["api_routes"])
        st.dataframe(routes, use_container_width=True, hide_index=True) if not routes.empty else st.info("No FastAPI-style route decorators were found.")

    st.subheader("Detected database models")
    models = pd.DataFrame(analysis["models"])
    st.dataframe(models, use_container_width=True, hide_index=True) if not models.empty else st.info("No SQLAlchemy or SQLModel-style models were found.")


render()
