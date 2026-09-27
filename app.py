import streamlit as st

from src.agent_graph import analyse_ticket
from src.hybrid_retriever import build_index

st.set_page_config(
    page_title="Support Ticket Resolution Assistant",
    page_icon="🔎",
    layout="wide"
)

st.title("Support Ticket Resolution Assistant")
st.write(
    "A read-only prototype using hybrid retrieval and a controlled agent."
)

with st.sidebar:
    st.header("Ticket details")
    category = st.selectbox(
        "Category",
        [
            "authentication",
            "configuration",
            "software-access",
            "unknown"
        ]
    )

ticket = st.text_area(
    "Enter a new support ticket",
    height=160,
    value=(
        "The user cannot access the Finance application after resetting "
        "their password and receives an authentication error."
    )
)

if st.button("Analyse Ticket", type="primary"):
    with st.spinner("Searching evidence and preparing recommendation..."):
        build_index()
        result = analyse_ticket(ticket, category)

    st.subheader("Summary")
    st.write(result["summary"])

    st.subheader("Diagnostic steps")
    for step in result["diagnostic_steps"]:
        st.write(f"- {step}")

    st.subheader("Recommended resolution")
    for step in result["recommended_resolution"]:
        st.write(f"- {step}")

    st.subheader("Evidence used")
    for evidence in result["evidence"]:
        st.write(
            f'**{evidence["source_id"]}** '
            f'({evidence["source_type"]}): '
            f'{evidence["reason"]}'
        )

    st.subheader("Freshness warnings")
    if result["outdated_warnings"]:
        for warning in result["outdated_warnings"]:
            st.warning(warning)
    else:
        st.success("No outdated-document warning was generated.")

    st.subheader("Escalation decision")
    if result["should_escalate"]:
        st.error(result["escalation_reason"])
    else:
        st.success("Evidence is sufficient for a recommended next step.")

    st.metric("Confidence", f'{result["confidence"]:.0%}')