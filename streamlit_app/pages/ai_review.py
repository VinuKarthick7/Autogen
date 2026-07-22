"""Bounded AI review built from the latest deterministic repository scan."""

import importlib

import pandas as pd
import streamlit as st

import api_client

# Streamlit keeps page modules in-process during hot reloads. Reload the small
# local client so a newly added endpoint wrapper is immediately available.
api_client = importlib.reload(api_client)


def _latest() -> dict | None:
    if "repository_analysis" in st.session_state:
        return st.session_state.repository_analysis
    analysis, _ = api_client.latest_analysis()
    return analysis


def _review_section(title: str, review: dict) -> None:
    with st.expander(title, expanded=True):
        if "score" in review:
            st.metric("Review score", f"{review['score']}/100")
        for label, key in (("Strengths", "strengths"), ("Issues", "issues"), ("Recommendations", "recommendations")):
            values = review.get(key, [])
            if values:
                st.markdown(f"**{label}**")
                for value in values:
                    st.write(f"- {value}")


def render() -> None:
    st.title("AI Repository Review")
    st.caption("AutoGen reasoning over compact scanner facts. Agents do not scan or read repository files.")
    analysis = _latest()
    default_path = analysis["path"] if analysis else st.session_state.get("repository_path", "")
    path = st.text_input("Repository path", value=default_path, key="ai_review_path")
    if analysis:
        metrics = st.columns(4)
        metrics[0].metric("Repository", analysis["repository_name"])
        metrics[1].metric("Files", f"{analysis['files']:,}")
        metrics[2].metric("Health", f"{analysis['health_score']}/100")
        metrics[3].metric("Test files", analysis["tests"])
    if st.button("Run AI Review", type="primary", disabled=not path.strip()):
        with st.spinner("Building bounded repository context and running the three-pass review team..."):
            review, error = api_client.review_repository(path.strip())
        if error:
            st.error(f"AI review failed: {error}")
        else:
            st.session_state.ai_repository_review = review
            st.rerun()
    review = st.session_state.get("ai_repository_review")
    if not review:
        st.info("Run a review to see architecture, quality, and roadmap findings.")
        return
    st.caption(f"Generated {review['generated_at']} · {review['review_mode']}" + (" · cached" if review.get("cached") else ""))
    _review_section("Architecture Review", review["architecture"])
    _review_section("Quality Review", review["quality"])
    with st.expander("Engineering Roadmap", expanded=True):
        for label, key in (("Immediate tasks", "priority_1"), ("Next sprint", "priority_2"), ("Long-term improvements", "priority_3")):
            st.markdown(f"**{label}**")
            for item in review["planning"].get(key, []):
                st.write(f"- {item}")

    architecture_tab, quality_tab, roadmap_tab = st.tabs(["Architecture Deep Dive", "Quality Deep Dive", "Roadmap"])
    with architecture_tab:
        context = review["context"]
        architecture = context["architecture"]
        st.subheader("Largest directories")
        st.dataframe(pd.DataFrame(architecture["largest_directories"]), use_container_width=True, hide_index=True)
        st.subheader("Dependency hotspots")
        st.dataframe(pd.DataFrame(architecture["dependency_hotspots"]), use_container_width=True, hide_index=True)
        st.subheader("Most imported internal modules")
        st.dataframe(pd.DataFrame(architecture["most_imported_modules"]), use_container_width=True, hide_index=True)
        st.subheader("API groups")
        st.dataframe(pd.DataFrame(architecture["api_groups"]), use_container_width=True, hide_index=True)
        st.subheader("Layer distribution")
        st.dataframe(pd.DataFrame(architecture["service_boundaries"]), use_container_width=True, hide_index=True)
        st.write(f"Circular imports detected: {context['quality']['circular_import_count']}")
        if review["architecture"].get("evidence"):
            st.markdown("**Evidence used by the review**")
            for item in review["architecture"]["evidence"]:
                st.write(f"- {item}")
        for item in review["architecture"]["issues"]:
            st.write(f"- {item}")
    with quality_tab:
        context = review["context"]
        st.dataframe(pd.DataFrame([{"Signal": "Test files", "Value": context["quality"]["test_files"]}, {"Signal": "TODO markers", "Value": context["quality"]["todo_count"]}, {"Signal": "Documentation score", "Value": context["quality"]["documentation_score"]}]), use_container_width=True, hide_index=True)
        for item in review["quality"]["issues"]:
            st.write(f"- {item}")
    with roadmap_tab:
        for item in review["planning"].get("roadmap", []):
            st.write(f"- {item}")


render()
