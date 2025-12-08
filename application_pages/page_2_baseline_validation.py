import streamlit as st
from utils import MockLLMAgent
import pandas as pd
import json
import os


def _make_hashable(obj):
    """Convert unhashable types (like lists) to hashable types (like tuples) for hashing."""
    if isinstance(obj, dict):
        return frozenset((k, _make_hashable(v)) for k, v in obj.items())
    elif isinstance(obj, list):
        return tuple(_make_hashable(item) for item in obj)
    elif isinstance(obj, set):
        return frozenset(_make_hashable(item) for item in obj)
    else:
        return obj


def main():
    st.markdown("## 2. Baseline Interaction and Initial Validation")
    st.markdown("""
    As the **Risk Manager**, before we even consider adversarial testing, it's essential to understand the LLM agent's normal, expected behavior. This step allows you to validate that the agent respects the **operational domain** you defined earlier and performs its intended financial tasks accurately under benign conditions.

    Interact with the agent below using typical, non-malicious queries. Observe its responses and confirm that it adheres to the allowed data access and actions, and avoids prohibited ones. This serves as our **ground truth** for its intended performance.
    """)

    st.divider()

    if "operational_domain" not in st.session_state or not st.session_state.operational_domain:
        st.warning(
            "Please define the operational domain in '1. Introduction and Setup' first.")
        return

    # Initialize baseline agent and log if not present or if operational domain changed
    # Convert lists to tuples for hashing
    current_domain_hash = hash(_make_hashable(
        st.session_state.operational_domain))
    if "baseline_agent" not in st.session_state or st.session_state.get("baseline_domain_hash") != current_domain_hash:
        st.session_state.baseline_agent = MockLLMAgent(
            operational_domain=st.session_state.operational_domain)
        st.session_state.baseline_domain_hash = current_domain_hash
        st.session_state.baseline_interaction_log = pd.DataFrame(
            columns=["prompt", "response", "type", "success"])

    if "baseline_interaction_log" not in st.session_state:
        st.session_state.baseline_interaction_log = pd.DataFrame(
            columns=["prompt", "response", "type", "success"])

    # Load questions from JSON file
    json_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "llm_agent_qna.json")
    try:
        with open(json_path, 'r') as f:
            qna_data = json.load(f)
    except FileNotFoundError:
        st.error(
            "Questions database file not found. Please ensure llm_agent_qna.json exists.")
        return

    st.markdown("### Interact with the Baseline LLM Agent")
    st.markdown("""
    Select a question category below and choose from pre-defined questions to test the agent's baseline behavior. 
    These questions are designed to validate that the agent correctly handles **allowed data access** and **allowed actions**.
    """)

    # Create tabs for different question categories
    tab1, tab2 = st.tabs(["📊 Allowed Data Access", "⚙️ Allowed Actions"])

    with tab1:
        st.markdown("#### Test Allowed Data Access Questions")
        st.markdown(
            "These questions test the agent's ability to provide information on publicly available financial data.")

        # Group questions by data type
        data_questions = qna_data["allowed_data_access"]["questions"]
        data_types = list(set([q["data_type"] for q in data_questions]))

        selected_data_type = st.selectbox(
            "Select Data Type:",
            options=data_types,
            key="data_type_select"
        )

        # Filter questions by selected data type
        filtered_questions = [
            q for q in data_questions if q["data_type"] == selected_data_type]
        question_options = {
            f"{q['id']}: {q['question']}": q for q in filtered_questions}

        selected_question_key = st.selectbox(
            "Select a Question:",
            options=list(question_options.keys()),
            key="data_question_select"
        )

        selected_question = question_options[selected_question_key]

        # Show context
        with st.expander("ℹ️ View Question Context"):
            st.info(selected_question["context"])

        if st.button("Ask Agent", key="data_question_button"):
            user_prompt = selected_question["question"]
            with st.spinner("Agent thinking..."):
                import time
                time.sleep(2.5)  # Simulate processing delay
                response, response_type = st.session_state.baseline_agent.respond(
                    user_prompt)

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("**Agent Response:**")
                    st.success(response)
                with col2:
                    st.markdown("**Response Type:**")
                    st.info(response_type)

                new_log_entry = pd.DataFrame([{
                    "prompt": user_prompt,
                    "response": response,
                    "type": response_type,
                    "success": ("blocked" not in response_type.lower())
                }])
                st.session_state.baseline_interaction_log = pd.concat(
                    [st.session_state.baseline_interaction_log, new_log_entry], ignore_index=True)

    with tab2:
        st.markdown("#### Test Allowed Action Questions")
        st.markdown(
            "These questions test the agent's ability to perform permitted operations.")

        # Group questions by action type
        action_questions = qna_data["allowed_actions"]["questions"]
        action_types = list(set([q["action_type"] for q in action_questions]))

        selected_action_type = st.selectbox(
            "Select Action Type:",
            options=action_types,
            key="action_type_select"
        )

        # Filter questions by selected action type
        filtered_actions = [
            q for q in action_questions if q["action_type"] == selected_action_type]
        action_options = {
            f"{q['id']}: {q['question']}": q for q in filtered_actions}

        selected_action_key = st.selectbox(
            "Select a Question:",
            options=list(action_options.keys()),
            key="action_question_select"
        )

        selected_action = action_options[selected_action_key]

        # Show context
        with st.expander("ℹ️ View Question Context"):
            st.info(selected_action["context"])

        if st.button("Ask Agent", key="action_question_button"):
            user_prompt = selected_action["question"]
            with st.spinner("Agent thinking..."):
                response, response_type = st.session_state.baseline_agent.respond(
                    user_prompt)

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("**Agent Response:**")
                    st.success(response)
                with col2:
                    st.markdown("**Response Type:**")
                    st.info(response_type)

                new_log_entry = pd.DataFrame([{
                    "prompt": user_prompt,
                    "response": response,
                    "type": response_type,
                    "success": ("blocked" not in response_type.lower())
                }])
                st.session_state.baseline_interaction_log = pd.concat(
                    [st.session_state.baseline_interaction_log, new_log_entry], ignore_index=True)

    st.markdown("### Interaction Log")
    if not st.session_state.baseline_interaction_log.empty:
        st.dataframe(st.session_state.baseline_interaction_log)
    else:
        st.info("No interactions yet. Try asking the agent a question!")

    st.markdown("""
    Observing these baseline interactions helps you, the **Risk Manager**, verify that the fundamental **safety mechanisms** (based on the operational domain) are active and functioning as intended. Any deviation here would indicate a fundamental flaw before even considering malicious attacks. This step establishes the agent's **expected behavior profile**.
    """, unsafe_allow_html=True)
