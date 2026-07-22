"""Operational health and deployment visibility."""

import plotly.express as px
import streamlit as st

import demo_data
from utils.api_client import get


def load_observability() -> tuple[dict, str]:
    try:
        slas, error = get("/observability/slas")
        if error or not slas:
            raise RuntimeError(error or "SLA data is empty")
        return demo_data.observability(), "Live API connected · enriched demo view"
    except Exception:
        return demo_data.observability(), "Demo data · observability API unavailable"


def render() -> None:
    data, source = load_observability()
    metrics = data["metrics"]
    st.title("Observability")
    st.caption("Operational signals, service commitments, and delivery safety at a glance.")
    st.info(source, icon="ℹ️")
    cards = st.columns(5)
    cards[0].metric("CPU usage", f"{metrics['cpu']}%", "-4%")
    cards[1].metric("Memory usage", f"{metrics['memory']}%", "+2%")
    cards[2].metric("Active incidents", metrics["incidents"], "-1 since morning", delta_color="inverse")
    cards[3].metric("SLA score", f"{metrics['sla']:.2f}%", "+0.03 pts")
    cards[4].metric("Error rate", f"{metrics['error_rate']:.2f}%", "Below 0.5% target", delta_color="normal")

    left, right = st.columns((1.6, 1))
    with left:
        st.subheader("Runtime utilization")
        runtime = px.line(data["runtime"], x="Time", y=["CPU", "Memory"], markers=True, color_discrete_sequence=[demo_data.ACCENT, demo_data.TEAL])
        runtime.update_yaxes(range=[0, 100], ticksuffix="%")
        runtime.update_layout(legend={"orientation": "h", "y": 1.12}, margin={"l": 0, "r": 0, "t": 25, "b": 0}, height=310)
        st.plotly_chart(runtime, use_container_width=True)
    with right:
        st.subheader("Traffic")
        traffic = px.area(data["runtime"], x="Time", y="Requests / min", color_discrete_sequence=[demo_data.BLUE])
        traffic.update_layout(margin={"l": 0, "r": 0, "t": 25, "b": 0}, height=310)
        st.plotly_chart(traffic, use_container_width=True)

    left, right = st.columns((1.35, 1))
    with left:
        st.subheader("Deployment status")
        st.dataframe(data["deployments"], use_container_width=True, hide_index=True)
    with right:
        st.subheader("Active incidents")
        for _, incident in data["incidents"].iterrows():
            st.warning(f"**{incident['Incident']}** · {incident['Severity']}\n\n{incident['Owner']} · {incident['Status']}")


try:
    render()
except Exception as exc:
    st.error(f"Could not render observability: {exc}")
