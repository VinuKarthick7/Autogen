"""Executive overview for the proof-of-concept demo."""

import plotly.express as px
import streamlit as st

import demo_data
from utils.api_client import get


def load_dashboard() -> tuple[dict, str]:
    try:
        health, error = get("/health")
        if error or not isinstance(health, dict):
            raise RuntimeError(error or "Health payload is incomplete")
        # The backend health check is intentionally used only as a live-data signal;
        # the demo model fills in the richer executive data shape.
        data = demo_data.dashboard()
        data["metrics"]["health"] = float(health.get("uptime", data["metrics"]["health"]))
        return data, "Live API connected · demo analytics model"
    except Exception:
        return demo_data.dashboard(), "Demo data · backend unavailable"


def render() -> None:
    data, source = load_dashboard()
    metrics = data["metrics"]
    st.title("Engineering command center")
    st.caption("A live view of autonomous delivery, quality, and platform posture.")
    st.info(source, icon="ℹ️")

    columns = st.columns(5)
    columns[0].metric("Repositories analyzed", f"{metrics['repositories']}", "+3 this month")
    columns[1].metric("Features generated", f"{metrics['features']}", "+18 this week")
    columns[2].metric("Test pass rate", f"{metrics['pass_rate']:.1f}%", "+1.2 pts")
    columns[3].metric("Security score", f"{metrics['security']}/100", "+4 pts")
    columns[4].metric("System health", f"{metrics['health']:.2f}%", "Operational")

    left, right = st.columns((1.45, 1))
    with left:
        st.subheader("Delivery momentum")
        chart = px.bar(data["delivery"], x="Week", y="Features", text="Features", color_discrete_sequence=[demo_data.ACCENT])
        chart.add_scatter(x=data["delivery"]["Week"], y=data["delivery"]["Tests"], mode="lines+markers", name="Test pass rate", yaxis="y2", line={"color": demo_data.TEAL, "width": 3})
        chart.update_layout(yaxis2={"overlaying": "y", "side": "right", "range": [85, 100], "ticksuffix": "%"}, legend={"orientation": "h", "y": 1.12}, margin={"l": 0, "r": 0, "t": 25, "b": 0}, height=330)
        st.plotly_chart(chart, use_container_width=True)
    with right:
        st.subheader("Repository posture")
        posture = px.bar(data["repositories"], x="Health", y="Repository", orientation="h", color="Health", color_continuous_scale=[demo_data.ROSE, demo_data.AMBER, demo_data.TEAL], range_color=[80, 100])
        posture.update_layout(coloraxis_showscale=False, margin={"l": 0, "r": 0, "t": 15, "b": 0}, height=330)
        st.plotly_chart(posture, use_container_width=True)

    st.subheader("Recent activity")
    for _, item in data["activity"].iterrows():
        a, b, c = st.columns((0.12, 1.1, 0.42))
        a.markdown(f"**{item['Time']}**")
        b.markdown(f"**{item['Event']}**  \n{item['Detail']}")
        c.success(item["Status"])


try:
    render()
except Exception as exc:
    st.error(f"Could not render the dashboard: {exc}")
