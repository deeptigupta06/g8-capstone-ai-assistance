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
    "A read-only assistant that searches resolved tickets and "
    "knowledge-base articles to recommend grounded next steps."
)


application_options = [
    "HR Leave Application",
    "Payroll Application",
    "CRM",
    "CMS",
    "Enterprise Applications",
    "Oracle",
    "PeopleSoft",
    "Authentication",
    "Microsoft 365",
    "VPN and Remote Access",
    "Others"
]


question_options = {
    "HR Leave Application": [
        "Leave request cannot be submitted",
        "Leave balance is incorrect",
        "Leave approval is pending",
        "Leave application login fails"
    ],

    "Payroll Application": [
        "Payslip is unavailable",
        "Payroll login fails",
        "Salary information is incorrect",
        "Payroll access is denied"
    ],

    "CRM": [
        "CRM login fails",
        "Customer record cannot be opened",
        "CRM page is not loading",
        "CRM permission error appears"
    ],

    "CMS": [
        "CMS login fails",
        "Web page cannot be published",
        "CMS editor is not loading",
        "User cannot edit content"
    ],

    "Enterprise Applications": [
        "Enterprise application login fails",
        "Application page is not loading",
        "User receives an access denied message",
        "Application configuration error appears"
    ],

    "Oracle": [
        "Oracle login fails",
        "Oracle role is missing",
        "Oracle form does not open",
        "Oracle transaction cannot be submitted"
    ],

    "PeopleSoft": [
        "PeopleSoft login fails",
        "PeopleSoft page does not load",
        "PeopleSoft role is missing",
        "PeopleSoft approval is pending"
    ],

    "Authentication": [
        "User cannot log in",
        "Password reset does not work",
        "Multi-factor authentication fails",
        "Account is locked"
    ],

    "Microsoft 365": [
        "Microsoft 365 login fails",
        "Outlook is not synchronising",
        "Teams meeting cannot be created",
        "SharePoint page cannot be opened"
    ],

    "VPN and Remote Access": [
        "VPN login fails",
        "VPN connection drops",
        "Remote access is unavailable",
        "User cannot access internal applications remotely"
    ],

    "Others": [
        "Other issue"
    ]
}


with st.sidebar:
    st.header("Ticket details")

    application = st.selectbox(
        "Select application",
        application_options
    )

    selected_question = st.selectbox(
        "Select common problem",
        question_options[application]
    )


st.subheader("Describe the support issue")


if application == "Others":
    ticket_description = st.text_area(
        "Enter the support ticket",
        height=160,
        placeholder=(
            "Describe the issue, error message, affected application, "
            "and steps already attempted."
        )
    )
else:
    ticket_description = st.text_area(
        "Support ticket details",
        height=160,
        value=selected_question
    )


additional_details = st.text_area(
    "Additional details",
    height=120,
    placeholder=(
        "Add error messages, user impact, dates, screenshots, "
        "or other relevant information."
    )
)


full_ticket = f"""
Application: {application}
Problem type: {selected_question}
Ticket description: {ticket_description}
Additional details: {additional_details}
"""


if st.button("Analyse Ticket", type="primary"):

    if not ticket_description.strip():
        st.warning(
            "Please enter or select a support ticket description."
        )

    else:
        with st.spinner(
            "Searching tickets and knowledge-base articles..."
        ):
            build_index()

            result = analyse_ticket(
                full_ticket,
                application,
                application
            )


        st.divider()

        st.subheader("Problem summary")
        st.write(result.get("summary", ""))


        st.subheader("Classification")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Application",
                result.get("application", application)
            )

        with col2:
            st.metric(
                "Category",
                result.get("category", application)
            )

        with col3:
            confidence = result.get("confidence", 0)
            st.metric(
                "Confidence",
                f"{float(confidence):.0%}"
            )


        st.subheader("Diagnostic steps")

        diagnostic_steps = result.get(
            "diagnostic_steps",
            []
        )

        if diagnostic_steps:
            for step in diagnostic_steps:
                st.write(f"- {step}")
        else:
            st.info(
                "No diagnostic steps were generated."
            )


        st.subheader("Recommended resolution")

        resolution_steps = result.get(
            "recommended_resolution",
            []
        )

        if resolution_steps:
            for step in resolution_steps:
                st.write(f"- {step}")
        else:
            st.info(
                "No supported resolution was found."
            )


        st.subheader("Knowledge-base references")

        evidence = result.get(
            "evidence",
            []
        )

        if evidence:
            for source in evidence:
                source_id = source.get(
                    "source_id",
                    "Unknown"
                )

                source_type = source.get(
                    "source_type",
                    "Unknown"
                )

                title = source.get(
                    "title",
                    ""
                )

                reason = source.get(
                    "reason",
                    ""
                )

                url = source.get(
                    "url",
                    ""
                )

                st.markdown(
                    f"**{source_id}** "
                    f"({source_type})"
                )

                if title:
                    st.write(
                        f"Title: {title}"
                    )

                if reason:
                    st.write(
                        f"Why it was selected: {reason}"
                    )

                if url:
                    st.markdown(
                        f"[Open knowledge article]({url})"
                    )

                st.divider()
        else:
            st.info(
                "No knowledge-base reference was found."
            )


        st.subheader("Instructions for support agent")

        agent_instructions = result.get(
            "agent_instructions",
            []
        )

        if agent_instructions:
            for instruction in agent_instructions:
                st.write(f"- {instruction}")
        else:
            st.write(
                "- Confirm the user ID."
            )
            st.write(
                "- Capture the exact error message."
            )
            st.write(
                "- Capture a screenshot."
            )
            st.write(
                "- Record the time of occurrence."
            )


        st.subheader("Document freshness warnings")

        warnings = result.get(
            "outdated_warnings",
            []
        )

        if warnings:
            for warning in warnings:
                st.warning(warning)
        else:
            st.success(
                "No outdated-document warning was generated."
            )


        st.subheader("Escalation decision")

        should_escalate = result.get(
            "should_escalate",
            False
        )

        if should_escalate:
            st.error(
                result.get(
                    "escalation_reason",
                    "Escalation is recommended."
                )
            )
        else:
            st.success(
                "Evidence is sufficient for a recommended next step."
            )


        st.subheader(
            "Information required before escalation"
        )

        escalation_information = result.get(
            "escalation_information",
            []
        )

        if escalation_information:
            for item in escalation_information:
                st.write(f"- {item}")
        else:
            st.write("- User ID")
            st.write("- Exact error message")
            st.write("- Screenshot")
            st.write("- Time of occurrence")