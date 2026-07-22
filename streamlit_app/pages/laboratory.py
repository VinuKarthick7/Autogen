"""Research portfolio and strategy benchmarks."""

import plotly.express as px
import streamlit as st

import demo_data
from utils.api_client import get


def load_laboratory() -> tuple[dict, str]:
    try:
        metrics, error = get("/laboratory/metrics")
        if error or not metrics:
            raise RuntimeError(error or "Laboratory metrics are empty")
        return demo_data.laboratory(), "Live API connected · enriched demo view"
    except Exception:
        return demo_data.laboratory(), "Demo data · laboratory API unavailable"


def render() -> None:
    data, source = load_laboratory()
    metrics = data["metrics"]
    st.title("Laboratory")
    st.caption("Evidence-driven experimentation for the next generation of engineering automation.")
    st.info(source, icon="ℹ️")
    cards = st.columns(4)
    cards[0].metric("Experiments", metrics["experiments"], "3 active")
    cards[1].metric("Strategies", metrics["strategies"], "+2 this quarter")
    cards[2].metric("Best benchmark", f"{metrics['best_score']:.1f}", "+3.8 pts")
    cards[3].metric("Research confidence", f"{metrics['confidence']}%", "+6 pts")

    left, right = st.columns((1.25, 1))
    with left:
        st.subheader("Strategy benchmark")
        benchmark = px.bar(data["benchmarks"], x="Strategy", y="Code quality", text="Code quality", color="Code quality", color_continuous_scale="Tealgrn", range_y=[0, 100])
        benchmark.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        benchmark.update_layout(coloraxis_showscale=False, margin={"l": 0, "r": 0, "t": 25, "b": 0}, height=330)
        st.plotly_chart(benchmark, use_container_width=True)
    with right:
        st.subheader("Strategy profile")
        radar = px.line_polar(data["benchmarks"], r="Latency", theta="Strategy", line_close=True, markers=True, color_discrete_sequence=[demo_data.ACCENT])
        radar.update_layout(showlegend=False, margin={"l": 20, "r": 20, "t": 25, "b": 0}, height=330)
        st.plotly_chart(radar, use_container_width=True)

    st.subheader("Experiment portfolio")
    experiments = data["experiments"].copy()
    st.dataframe(experiments, use_container_width=True, hide_index=True, column_config={"Progress": st.column_config.ProgressColumn("Progress", min_value=0, max_value=100, format="%d%%")})

    st.subheader("Research recommendations")
    for recommendation, rationale in data["recommendations"]:
        st.markdown(f"<div class='recommendation'><b>{recommendation}</b><br><span>{rationale}</span></div>", unsafe_allow_html=True)


try:
    render()
except Exception as exc:
    st.error(f"Could not render laboratory data: {exc}")
