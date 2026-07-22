"""Repository intelligence view for the proof-of-concept demo."""

import plotly.express as px
import streamlit as st

import demo_data
from utils.api_client import get


def load_intelligence() -> tuple[dict, str]:
    try:
        repositories, error = get("/knowledge/repositories")
        if error or not repositories:
            raise RuntimeError(error or "No repository records")
        return demo_data.repository_intelligence(), "Live API connected · enriched demo view"
    except Exception:
        return demo_data.repository_intelligence(), "Demo data · knowledge API unavailable"


def render() -> None:
    data, source = load_intelligence()
    stats, graph = data["stats"], data["graph"]
    st.title("Repository intelligence")
    st.caption("Architecture knowledge distilled from the engineering estate.")
    st.info(source, icon="ℹ️")
    cards = st.columns(4)
    cards[0].metric("Repositories", stats["repositories"], "2 indexed today")
    cards[1].metric("Files understood", f"{stats['files']:,}", "+1,204")
    cards[2].metric("Symbols mapped", f"{stats['symbols']:,}", "+5.8%")
    cards[3].metric("Test coverage", f"{stats['coverage']:.1f}%", "+2.1 pts")

    left, right = st.columns((1.15, 1))
    with left:
        st.subheader("Codebase composition")
        languages = px.treemap(data["languages"], path=["Language"], values="Files", color="Files", color_continuous_scale="Purples")
        languages.update_layout(margin={"l": 0, "r": 0, "t": 15, "b": 0}, height=300, coloraxis_showscale=False)
        st.plotly_chart(languages, use_container_width=True)
    with right:
        st.subheader("Knowledge graph")
        for label, value, note in [("Nodes", graph["nodes"], "symbols and artifacts"), ("Relationships", graph["edges"], "typed dependencies"), ("Communities", graph["communities"], "bounded contexts"), ("Hotspots", graph["hotspots"], "review recommended")]:
            c1, c2 = st.columns((0.5, 1))
            c1.metric(label, f"{value:,}")
            c2.caption(note)

    st.subheader("Extracted engineering conventions")
    conventions = data["conventions"].copy()
    st.dataframe(conventions, use_container_width=True, hide_index=True, column_config={"Confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=100, format="%d%%")})

    st.subheader("Planner status")
    for _, plan in data["planner"].iterrows():
        title, status = st.columns((1, 0.18))
        title.markdown(f"**{plan['Plan']}** · {plan['Tasks']} scoped tasks")
        status.success(plan["Status"])
        st.progress(int(plan["Readiness"]), text=f"{plan['Readiness']}% implementation readiness")


try:
    render()
except Exception as exc:
    st.error(f"Could not render repository intelligence: {exc}")
