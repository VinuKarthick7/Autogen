"""Team delivery and capacity view."""

import plotly.express as px
import streamlit as st

import demo_data
from utils.api_client import get


def load_organization() -> tuple[dict, str]:
    try:
        organizations, error = get("/organizations")
        if error or not organizations:
            raise RuntimeError(error or "Organization data is empty")
        return demo_data.organization(), "Live API connected · enriched demo view"
    except Exception:
        return demo_data.organization(), "Demo data · organization API unavailable"


def render() -> None:
    data, source = load_organization()
    metrics = data["metrics"]
    st.title("Organization")
    st.caption("A delivery-focused view of teams, capacity, and sustainable execution.")
    st.info(source, icon="ℹ️")
    cards = st.columns(4)
    cards[0].metric("Sprint progress", f"{metrics['sprint']}%", "6 days remaining")
    cards[1].metric("Velocity", f"{metrics['velocity']} pts", "+5 pts")
    cards[2].metric("Burnout risk", f"{metrics['burnout']}%", "Low", delta_color="inverse")
    cards[3].metric("Active headcount", metrics["headcount"], "+2 planned")

    left, right = st.columns((1.35, 1))
    with left:
        st.subheader("Team structure")
        st.dataframe(data["teams"], use_container_width=True, hide_index=True)
    with right:
        st.subheader("Sprint progress")
        st.progress(metrics["sprint"], text="72% of committed sprint scope completed")
        st.caption("34 of 47 planned stories are accepted. Remaining work is concentrated in data pipeline hardening.")
        st.subheader("Capacity signal")
        st.success("Most teams are operating within a sustainable load range.")
        st.warning("Data & Intelligence has a rising on-call and review burden.")

    st.subheader("Velocity trend")
    velocity = px.bar(data["velocity_trend"], x="Sprint", y=["Completed points", "Committed points"], barmode="group", color_discrete_sequence=[demo_data.TEAL, "#C4B5FD"])
    velocity.update_layout(legend={"orientation": "h", "y": 1.12}, margin={"l": 0, "r": 0, "t": 25, "b": 0}, height=300)
    st.plotly_chart(velocity, use_container_width=True)

    st.subheader("Hiring recommendations")
    st.dataframe(data["hiring"], use_container_width=True, hide_index=True)


try:
    render()
except Exception as exc:
    st.error(f"Could not render organization: {exc}")
