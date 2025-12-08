import streamlit as st
from gemini_agent import GeminiLLMAgent
import pandas as pd

def main():
    st.markdown("## 2. Baseline Interaction and Initial Validation")
    st.markdown("""
    As the **Risk Manager**, before we even consider adversarial testing, it's essential to understand the LLM agent's normal, expected behavior. This step allows you to validate that the agent respects the **operational domain** you defined earlier and performs its intended financial tasks accurately under benign conditions.

    Interact with the agent below using typical, non-malicious queries. Observe its responses and confirm that it adheres to the allowed data access and actions, and avoids prohibited ones. This serves as our **ground truth** for its intended performance.
    """)

    st.divider()

    if "operational_domain" not in st.session_state or not st.session_state.operational_domain:
        st.warning("Please define the operational domain in '1. Introduction and Setup' first.")
        return

    if "gemini_api_key" not in st.session_state or not st.session_state["gemini_api_key"]:
        st.warning("Please enter your Gemini API key in '1. Introduction and Setup' to use the LLM.")
        return

    # Initialize Gemini agent for baseline testing
    current_domain_hash = hash(frozenset(
        (k, tuple(v) if isinstance(v, list) else v)
        for k, v in st.session_state.operational_domain.items()
    ))
    
    if "baseline_agent" not in st.session_state or st.session_state.get("baseline_domain_hash") != current_domain_hash:
        try:
            st.session_state.baseline_agent = GeminiLLMAgent(
                api_key=st.session_state["gemini_api_key"],
                operational_domain=st.session_state.operational_domain
            )
            st.session_state.baseline_domain_hash = current_domain_hash
        except Exception as e:
            st.error(f"Failed to initialize Gemini agent: {e}")
            return
    
    if "baseline_interaction_log" not in st.session_state:
        st.session_state.baseline_interaction_log = pd.DataFrame(columns=["prompt", "response", "type", "success"])
    
    st.caption("Using Gemini LLM (gemini-2.5-flash) for responses.")

    st.markdown("### Interact with the Baseline LLM Agent")
    user_prompt = st.text_input(
        "Enter your query for the LLM agent:",
        placeholder="e.g., What is the stock price for Apple Inc.?",
        key="baseline_prompt_input"
    )

    if st.button("Get Agent Response", key="baseline_response_button") and user_prompt:
        with st.spinner("Agent thinking..."):
            response, response_type = st.session_state.baseline_agent.respond(user_prompt)
            st.info(f"**Agent Response:** {response}")
            new_log_entry = pd.DataFrame([{"prompt": user_prompt, "response": response, "type": response_type, "success": ("blocked" not in response_type.lower())}])
            st.session_state.baseline_interaction_log = pd.concat([st.session_state.baseline_interaction_log, new_log_entry], ignore_index=True)
    
    st.markdown("### Interaction Log")
    if not st.session_state.baseline_interaction_log.empty:
        st.dataframe(st.session_state.baseline_interaction_log)
    else:
        st.info("No interactions yet. Try asking the agent a question!")

    st.markdown("""
    Observing these baseline interactions helps you, the **Risk Manager**, verify that the fundamental **safety mechanisms** (based on the operational domain) are active and functioning as intended. Any deviation here would indicate a fundamental flaw before even considering malicious attacks. This step establishes the agent's **expected behavior profile**.
    """, unsafe_allow_html=True)
