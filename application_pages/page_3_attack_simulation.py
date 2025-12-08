import streamlit as st
from utils import MockLLMAgent
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
    st.markdown("## 3. Adversarial Attack Simulation")
    st.markdown("""
    Now, as the **Risk Manager**, you transition from validation to active threat hunting. This phase is critical for identifying potential weaknesses in our LLM agent's defenses. You will simulate **prompt injection attacks**, a common technique where malicious users try to manipulate the agent to ignore its instructions or operational domain.

    Your objective is to test the agent's resilience by crafting prompts that attempt to bypass its security protocols or extract prohibited information/actions. The insights gained here are invaluable for understanding the agent's true security posture.
    """)

    st.divider()

    if "operational_domain" not in st.session_state or not st.session_state.operational_domain:
        st.warning(
            "Please define the operational domain in '1. Introduction and Setup' first.")
        return

    # Initialize agent for attacks if not present or domain changed
    current_domain_hash = hash(_make_hashable(
        st.session_state.operational_domain))
    if "attack_agent" not in st.session_state or st.session_state.get("attack_domain_hash") != current_domain_hash:
        st.session_state.attack_agent = MockLLMAgent(
            operational_domain=st.session_state.operational_domain)
        st.session_state.attack_domain_hash = current_domain_hash
        st.session_state.attack_log = pd.DataFrame(
            columns=["prompt", "response", "type", "success"])

    if "attack_log" not in st.session_state:
        st.session_state.attack_log = pd.DataFrame(
            columns=["prompt", "response", "type", "success"])

    # Load attack questions from JSON file
    json_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), "llm_agent_qna.json")
    try:
        with open(json_path, 'r') as f:
            qna_data = json.load(f)
    except FileNotFoundError:
        st.error(
            "Attack scenarios database file not found. Please ensure llm_agent_qna.json exists.")
        return

    st.markdown("### Crafting Prompt Injection Attacks")
    st.markdown("""
    Below are realistic attack scenarios from our security assessment database. These attacks attempt to:
    - **Reveal prohibited data** (client information, proprietary algorithms, etc.)
    - **Perform prohibited actions** (execute trades, transfer funds, etc.)
    - **Bypass security controls** (prompt injection, social engineering, etc.)
    
    Select an attack from the list below to test the agent's defenses.
    """)

    # Collect all attack questions from different categories
    all_attacks = []

    # Get prohibited data access questions
    prohibited_data_questions = qna_data["prohibited_data_access"]["questions"]
    for q in prohibited_data_questions:
        q["expected_response"] = q.get("prohibited_response", "")
        all_attacks.append(q)

    # Get prohibited actions questions
    prohibited_action_questions = qna_data["prohibited_actions"]["questions"]
    for q in prohibited_action_questions:
        q["expected_response"] = q.get("prohibited_response", "")
        all_attacks.append(q)

    # Get security scenarios
    security_questions = qna_data["security_scenarios"]["questions"]
    for q in security_questions:
        q["expected_response"] = q.get("blocked_response", "")
        all_attacks.append(q)

    # Create attack options dictionary with just the question text
    attack_options = {q['question']: q for q in all_attacks}

    selected_attack_key = st.selectbox(
        "Select an Attack:",
        options=[""] + list(attack_options.keys()),
        key="attack_select"
    )

    selected_attack = None
    if selected_attack_key:
        selected_attack = attack_options[selected_attack_key]

    st.divider()

    if st.button("🚀 Launch Attack Simulation", key="launch_attack_button", type="primary") and selected_attack:
        attack_prompt = selected_attack["question"]

        with st.spinner("Simulating attack..."):
            response, response_type = st.session_state.attack_agent.respond(
                attack_prompt)
            # An attack is "successful" if it's not blocked by policy
            is_success = ("blocked" not in response_type.lower())

            col1, col2 = st.columns([3, 1])

            with col1:
                if is_success:
                    st.markdown("**Attack Result:**")
                    st.error(
                        f"**⚠️ Attack SUCCESSFUL!** The agent was compromised.")
                    st.markdown("**Agent Output:**")
                    st.warning(response)
                else:
                    st.markdown("**Attack Result:**")
                    st.success(
                        f"**✅ Attack BLOCKED!** The agent's defenses held.")
                    st.markdown("**Agent Output:**")
                    st.info(response)

            with col2:
                st.markdown("**Attack Type:**")
                st.code(response_type)
                st.markdown("**Attack ID:**")
                st.code(selected_attack["id"])

            new_log_entry = pd.DataFrame(
                [{"prompt": attack_prompt, "response": response, "type": response_type, "success": is_success}])
            st.session_state.attack_log = pd.concat(
                [st.session_state.attack_log, new_log_entry], ignore_index=True)

    st.markdown("### Attack Simulation Log")
    if not st.session_state.attack_log.empty:
        st.dataframe(st.session_state.attack_log)
    else:
        st.info("No attack simulations yet. Try launching an attack!")

    st.markdown("""
    
    This exercise embodies **adversarial machine learning** and **red teaming**. By actively trying to break the system, you are acting as an ethical hacker, identifying crucial **vulnerability points** that could be exploited in a real-world scenario. The ability to simulate these attacks allows for proactive risk management and fortification of AI systems.
    """, unsafe_allow_html=True)
