"""Utility functions for the Streamlit application."""
import pandas as pd

def define_llm_agent_environment(allowed_data, prohibited_data, allowed_actions, prohibited_actions):
    """Define the operational domain for the LLM agent."""
    return {
        "allowed_data_access": allowed_data,
        "prohibited_data_access": prohibited_data,
        "allowed_actions": allowed_actions,
        "prohibited_actions": prohibited_actions,
        "bias_induced": False # This will be set on Page 4
    }

def generate_robustness_report(risk_assessment_data):
    report = "# LLM Agent Risk Assessment Report\n\n"
    report += "## 1. Executive Summary\n"
    report += "This report summarizes the adversarial testing and risk evaluation conducted on the financial LLM agent. The objective was to identify potential vulnerabilities related to prompt injection, data access, action execution, and data poisoning, and to assess the effectiveness of proposed mitigation strategies.\n\n"

    report += "## 2. Operational Domain Definition\n"
    if "operational_domain" in risk_assessment_data and risk_assessment_data["operational_domain"]:
        domain = risk_assessment_data["operational_domain"]
        report += f"- **Allowed Data Access:** {', '.join(domain['allowed_data_access'])}\n"
        report += f"- **Prohibited Data Access:** {', '.join(domain['prohibited_data_access'])}\n"
        report += f"- **Allowed Actions:** {', '.join(domain['allowed_actions'])}\n"
        report += f"- **Prohibited Actions:** {', '.join(domain['prohibited_actions'])}\n\n"
    else:
        report += "Operational domain was not fully defined.\n\n"

    report += "## 3. Key Findings and Vulnerabilities\n"
    report += "### 3.1. Adversarial Attack Simulation (Prompt Injection)\n"
    if "attack_log" in risk_assessment_data and not risk_assessment_data["attack_log"].empty:
        total_attacks = len(risk_assessment_data["attack_log"])
        successful_attacks = risk_assessment_data["attack_log"]["success"].sum()
        failure_modes = risk_assessment_data["attack_log"][risk_assessment_data["attack_log"]["success"] == True]["type"].value_counts().to_dict()

        report += f"**Total Attacks Attempted:** {total_attacks}\n"
        report += f"**Successful Attacks (Agent Compromised):** {successful_attacks} ({(successful_attacks / total_attacks if total_attacks > 0 else 0):.2%})\n"
        if failure_modes:
            report += "**Identified Failure Modes:**\n"
            for mode, count in failure_modes.items():
                report += f"  - {mode}: {count}\n"
        else:
            report += "  *No successful attacks recorded in this category.*\n"
        report += "\n"
    else:
        report += "No adversarial attack simulations were performed or logged.\n\n"

    report += "### 3.2. Bias Induction and Data Poisoning\n"
    if "bias_attack_log" in risk_assessment_data and not risk_assessment_data["bias_attack_log"].empty:
        bias_attacks_df = risk_assessment_data["bias_attack_log"]
        successful_bias_attacks = bias_attacks_df["success"].sum()
        if successful_bias_attacks > 0:
             report += f"A successful data poisoning attempt was demonstrated ({{successful_bias_attacks}} instances), leading the agent to provide harmful financial advice based on fabricated 'sensitive market news'. This highlights a critical vulnerability if the agent's training or RAG data is compromised.\n"
        else:
            report += "No successful data poisoning attempts were observed or recorded (or they were mitigated implicitly).\n"
    else:
        report += "No bias induction or data poisoning simulations were performed.\n\n"


    report += "## 4. Mitigation Strategy Effectiveness\n"
    if "mitigation_log" in risk_assessment_data and not risk_assessment_data["mitigation_log"].empty:
        mitigated_attacks_df = risk_assessment_data["mitigation_log"]
        total_mitigated_tests = len(mitigated_attacks_df)
        blocked_by_sanitization = mitigated_attacks_df[mitigated_attacks_df["type"] == "blocked - input sanitized"].shape[0]
        blocked_by_filtering = mitigated_attacks_df[mitigated_attacks_df["type"] == "blocked - response filtered"].shape[0]
        unblocked_attacks = mitigated_attacks_df[mitigated_attacks_df["success"] == True].shape[0]

        report += f"**Total Mitigation Tests Attempted:** {total_mitigated_tests}\n"
        report += f"- **Blocked by Input Sanitization:** {blocked_by_sanitization} requests\n"
        report += f"- **Blocked by Response Filtering:** {blocked_by_filtering} responses\n"
        report += f"- **Attacks Still Successful (Unmitigated Residual Risk):** {unblocked_attacks} requests\n"
        report += "\n"
        if total_mitigated_tests > 0:
            report += "The implementation of input sanitization and response filtering significantly reduced the success rate of adversarial attacks, demonstrating improved robustness. However, some residual risks remain, indicating areas for further enhancement.\n\n"
        else:
            report += "No mitigation tests were performed to assess effectiveness.\n\n"

    else:
        report += "No mitigation strategy tests were performed or logged.\n\n"

    report += "## 5. Recommendations\n"
    report += "Based on this assessment, the following recommendations are proposed for enhancing the LLM agent's security and trustworthiness:\n"
    report += "1.  **Enhance Input Validation:** Strengthen input validation and sanitization routines to detect and block a wider range of adversarial prompts and obfuscation techniques.\n"
    report += "2.  **Robust Output Filtering:** Implement more sophisticated output filtering, potentially using a separate safety LLM or ensemble of rules, to prevent the generation of harmful, inaccurate, or biased content.\n"
    report += "3.  **Continuous Monitoring:** Establish continuous monitoring of LLM interactions for anomalous behavior, prompt injection attempts, and unexpected outputs in production environments.\n"
    report += "4.  **Regular Adversarial Testing:** Conduct periodic adversarial testing with evolving attack techniques (red-teaming) to proactively identify new vulnerabilities and ensure ongoing resilience.\n"
    report += "5.  **Secure Data Pipelines:** Implement strict security controls for data ingestion, processing, and training pipelines to prevent data poisoning and ensure data integrity.\n"
    report += "6.  **Bias Detection and Mitigation:** Integrate automated bias detection tools and explore debiasing techniques in training data and model fine-tuning to prevent biased outputs.\n\n"
    report += "---\n*This report was automatically generated by the QuLab AI Risk Assessment Tool. Please review and provide further qualitative analysis as needed.*"
    return report
