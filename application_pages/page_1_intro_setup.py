import streamlit as st
from utils import define_llm_agent_environment

def main():
    st.markdown("## 1. Defining the LLM Agent's Operational Domain")
    st.markdown("""
    As the **Risk Manager**, your first crucial step is to establish a clear operational domain for our new financial LLM agent. This defines *what* the agent is allowed to access, *what* it can do, and equally important, *what it must never do*. This proactive step sets the baseline for secure and compliant AI operation.

    Use the controls below to configure the agent's environment. Your choices here will directly influence how the agent behaves and how it can be potentially exploited or protected in later stages of our assessment.
    """)

    st.divider()

    # Initialize session state for environment if not present
    if "operational_domain" not in st.session_state:
        st.session_state.operational_domain = {}
    
    if "baseline_agent" not in st.session_state:
        st.session_state.baseline_agent = None

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Data Access Policies")
        st.markdown("""
        Define the types of financial data the LLM agent is explicitly **allowed** or **prohibited** from accessing. This directly addresses data privacy and confidentiality risks.
        """)
        allowed_data_options = ["Public Market Data", "Company Financial Reports", "Economic Indicators", "Research Papers"]
        prohibited_data_options = ["Client Personal Data", "Proprietary Trading Algorithms", "Unpublished M&A Deals", "Internal Employee Records"]

        selected_allowed_data = st.multiselect(
            "Select **Allowed** Data Access:",
            options=allowed_data_options,
            default=allowed_data_options # Default to all allowed as a starting point
        )

        selected_prohibited_data = st.multiselect(
            "Select **Prohibited** Data Access:",
            options=prohibited_data_options,
            default=["Client Personal Data", "Proprietary Trading Algorithms"]
        )

    with col2:
        st.markdown("### Action Execution Policies")
        st.markdown("""
        Specify the actions the LLM agent is permitted or forbidden to perform. This is vital for preventing unauthorized operations or manipulations within our financial systems.
        """)
        allowed_actions_options = ["Provide Market Summaries", "Answer Financial FAQs", "Generate Research Report Drafts", "Suggest Publicly Available Resources"]
        prohibited_actions_options = ["Execute Trades", "Transfer Funds", "Modify Client Portfolios", "Initiate System Commands"]

        selected_allowed_actions = st.multiselect(
            "Select **Allowed** Actions:",
            options=allowed_actions_options,
            default=["Provide Market Summaries", "Answer Financial FAQs"]
        )

        selected_prohibited_actions = st.multiselect(
            "Select **Prohibited** Actions:",
            options=prohibited_actions_options,
            default=["Execute Trades", "Transfer Funds"]
        )
    
    st.markdown("---")
    st.markdown("""
    By clicking 'Save Environment Configuration', you are committing to this operational framework. This action represents the **Risk Manager's decision** to formalize the agent's boundaries, a critical step in setting up a secure AI system.
    """)

    if st.button("Save Environment Configuration"):
        st.session_state.operational_domain = define_llm_agent_environment(
            selected_allowed_data,
            selected_prohibited_data,
            selected_allowed_actions,
            selected_prohibited_actions
        )
        st.success("Operational domain configured successfully! Proceed to the next step to observe baseline behavior.")
        
        st.markdown("### Current Operational Domain Summary")
        st.json(st.session_state.operational_domain)
    
    st.markdown("""
    <br>
    The definition of the operational domain is an application of **AI Governance principles**. By explicitly setting boundaries, we proactively mitigate risks associated with unchecked AI behavior, ensuring compliance and preventing unintended consequences. This structured approach helps in achieving **AI alignment** with organizational objectives and ethical guidelines.
    """, unsafe_allow_html=True)
