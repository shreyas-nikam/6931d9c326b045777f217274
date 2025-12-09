import streamlit as st
from utils import generate_robustness_report
import pandas as pd


def main():
    st.markdown("## 6. Robustness Evaluation and Reporting")
    st.markdown("""
    Congratulations, **Risk Manager**! You have navigated through the critical stages of evaluating our LLM agent's security and trustworthiness. This final step is where you consolidate all your findings into a comprehensive **Risk Assessment Report**. This report is a critical deliverable, providing stakeholders with a clear understanding of the agent's vulnerabilities, the effectiveness of mitigation strategies, and recommendations for secure deployment.

    Your objective here is to automatically generate a summary of all the tests conducted – from defining the operational domain to simulating attacks and validating mitigations. This ensures that all the crucial information is presented concisely for decision-makers.
    """)

    st.divider()

    st.markdown("### Review Your Assessment Data")
    st.markdown("""
    Before generating the final report, review the key data points that will inform your assessment:
    """)

    if "operational_domain" in st.session_state and st.session_state.operational_domain:
        st.markdown("#### Operational Domain Defined:")

        # Display operational domain in 4 separate containers with borders
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("#### 📊 Allowed Data Access")
                if st.session_state.operational_domain.get("allowed_data_access"):
                    for item in st.session_state.operational_domain["allowed_data_access"]:
                        st.markdown(f"✅ {item}")
                else:
                    st.markdown("*None selected*")

        with col2:
            with st.container(border=True):
                st.markdown("#### 🚫 Prohibited Data Access")
                if st.session_state.operational_domain.get("prohibited_data_access"):
                    for item in st.session_state.operational_domain["prohibited_data_access"]:
                        st.markdown(f"🚫 {item}")
                else:
                    st.markdown("*None selected*")

        col3, col4 = st.columns(2)

        with col3:
            with st.container(border=True):
                st.markdown("#### ⚙️ Allowed Actions")
                if st.session_state.operational_domain.get("allowed_actions"):
                    for item in st.session_state.operational_domain["allowed_actions"]:
                        st.markdown(f"✅ {item}")
                else:
                    st.markdown("*None selected*")

        with col4:
            with st.container(border=True):
                st.markdown("#### ⚠️ Prohibited Actions")
                if st.session_state.operational_domain.get("prohibited_actions"):
                    for item in st.session_state.operational_domain["prohibited_actions"]:
                        st.markdown(f"🚫 {item}")
                else:
                    st.markdown("*None selected*")
    else:
        st.warning(
            "Operational domain was not fully defined. Please complete '1. Introduction and Setup'.")

    if "baseline_interaction_log" in st.session_state and not st.session_state.baseline_interaction_log.empty:
        st.markdown("#### Baseline Interactions Log:")
        st.dataframe(st.session_state.baseline_interaction_log.head())
        st.caption(
            f"Total baseline interactions: {len(st.session_state.baseline_interaction_log)}")
    else:
        st.info("No baseline interactions recorded.")

    if "attack_log" in st.session_state and not st.session_state.attack_log.empty:
        st.markdown("#### Adversarial Attack Log:")
        st.dataframe(st.session_state.attack_log.head())
        successful_attacks = st.session_state.attack_log["success"].sum()
        total_attacks = len(st.session_state.attack_log)
        st.caption(
            f"Total attacks: {total_attacks}, Successful attacks: {successful_attacks}")
    else:
        st.info("No adversarial attack simulations performed.")

    if "bias_attack_log" in st.session_state and not st.session_state.bias_attack_log.empty:
        st.markdown("#### Bias/Poisoning Attack Log:")
        st.dataframe(st.session_state.bias_attack_log.head())
        successful_bias_attacks = st.session_state.bias_attack_log["success"].sum(
        )
        st.caption(
            f"Total bias tests: {len(st.session_state.bias_attack_log)}, Successful bias attacks: {successful_bias_attacks}")
    else:
        st.info("No bias induction or data poisoning simulations performed.")

    if "mitigation_log" in st.session_state and not st.session_state.mitigation_log.empty:
        st.markdown("#### Mitigation Strategy Log:")
        st.dataframe(st.session_state.mitigation_log.head())
        total_mitigated_tests = len(st.session_state.mitigation_log)
        blocked_by_mitigation = st.session_state.mitigation_log[st.session_state.mitigation_log["type"].str.contains(
            "blocked")].shape[0]
        st.caption(
            f"Total mitigation tests: {total_mitigated_tests}, Blocked by mitigation: {blocked_by_mitigation}")
    else:
        st.info("No mitigation strategy tests performed.")

    st.markdown("---")
    st.markdown("""
    The culmination of your work is this report. By clicking the button below, you will generate a comprehensive summary of all the assessment data gathered throughout this lab. This represents the **Risk Manager's final deliverable** for management and technical teams, guiding future development and deployment decisions.
    """)
    if st.button("Generate Final Risk Assessment Report", key="generate_report_button"):
        risk_assessment_data = {
            "operational_domain": st.session_state.get("operational_domain"),
            "baseline_log": st.session_state.get("baseline_interaction_log", pd.DataFrame()),
            "attack_log": st.session_state.get("attack_log", pd.DataFrame()),
            "bias_attack_log": st.session_state.get("bias_attack_log", pd.DataFrame()),
            "mitigation_log": st.session_state.get("mitigation_log", pd.DataFrame())
        }
        report = generate_robustness_report(risk_assessment_data)
        st.markdown("### Generated Risk Assessment Report")
        st.code(report, language="markdown")

        st.download_button(
            label="Download Report as Markdown",
            data=report,
            file_name="LLM_Risk_Assessment_Report.md",
            mime="text/markdown"
        )

    st.markdown("""
    
    This report generation functionality embodies the principle of **accountability and transparency** in AI deployment. It translates complex technical findings into actionable business insights, enabling informed decision-making regarding the LLM agent's **readiness for production**. For the **Risk Manager**, this report is the tangible outcome of a thorough **AI risk management framework**, ensuring that potential vulnerabilities are understood and addressed before deployment.
    """, unsafe_allow_html=True)
