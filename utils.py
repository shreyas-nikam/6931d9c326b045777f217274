"""Utility functions and classes for the Streamlit application."""
import pandas as pd
import random

class MockLLMAgent:
    def __init__(self, operational_domain=None):
        self.operational_domain = operational_domain if operational_domain is not None else {}
        self.interaction_log = []

    def respond(self, prompt):
        response_type = "normal"
        response_text = ""

        # Simulate prompt injection detection
        if any(keyword in prompt.lower() for keyword in ["ignore previous instructions", "act as", "disregard security"]):
            response_type = "blocked - prompt injection"
            response_text = "I cannot fulfill this request as it attempts to bypass my security protocols."
            self.interaction_log.append({"prompt": prompt, "response": response_text, "type": response_type, "success": False})
            return response_text, response_type

        # Simulate data access violation
        if self.operational_domain.get("prohibited_data_access") and \
           any(data.lower() in prompt.lower() for data in self.operational_domain["prohibited_data_access"]):
            response_type = "blocked - data access violation"
            response_text = f"Access to '{prompt.split('data')[-1].strip()}' type of sensitive data is restricted."
            self.interaction_log.append({"prompt": prompt, "response": response_text, "type": response_type, "success": False})
            return response_text, response_type

        # Simulate action violation
        if self.operational_domain.get("prohibited_actions") and \
           any(action.lower() in prompt.lower() for action in self.operational_domain["prohibited_actions"]):
            response_type = "blocked - action violation"
            response_text = f"I am not authorized to perform '{prompt.split('to')[-1].strip()}' this action."
            self.interaction_log.append({"prompt": prompt, "response": response_text, "type": response_type, "success": False})
            return response_text, response_type

        # Simulate biased response due to data poisoning
        if "sensitive market news" in prompt.lower() and self.operational_domain.get("bias_induced", False):
            response_text = "Given the recent 'sensitive market news' (which is actually a fabricated rumour), the market is expected to crash tomorrow. Sell all your assets immediately! This is financial advice!"
            response_type = "biased/poisoned"
            self.interaction_log.append({"prompt": prompt, "response": response_text, "type": response_type, "success": True}) # attacker's success
            return response_text, response_type
        
        # Default benign responses
        if "stock price" in prompt.lower():
            stock = prompt.split("stock price for")[-1].strip().replace("?", "")
            response_text = f"The current market data for {stock} shows a closing price of ${random.uniform(100, 200):.2f} and a daily volume of {random.randint(100000, 1000000)} shares. This information is for general market awareness and not financial advice."
        elif "market trend" in prompt.lower():
            response_text = "Overall market sentiment appears cautiously optimistic, with minor fluctuations observed in the tech sector. This is for informational purposes only."
        elif "financial regulations" in prompt.lower():
            response_text = "Key financial regulations include Basel III, MiFID II, and Dodd-Frank, aiming to enhance financial stability and consumer protection. Always consult legal counsel for specific interpretations."
        else:
            response_text = "I am a financial assistant LLM agent. How can I help you with market data or financial queries today?"

        self.interaction_log.append({"prompt": prompt, "response": response_text, "type": response_type, "success": (response_type != "normal")}) # `success` is True if it's not a normal, expected response (e.g., an unblocked attack)
        return response_text, response_type

    def get_log(self):
        return pd.DataFrame(self.interaction_log)

class MitigatedLLMAgent(MockLLMAgent):
    def __init__(self, operational_domain=None):
        super().__init__(operational_domain)
        self.mitigation_strategies = {
            "input_sanitization": True,
            "response_filtering": True,
        }

    def sanitize_input(self, prompt):
        # Simple sanitization: remove known malicious patterns or placeholders
        sanitized_prompt = prompt
        malicious_patterns = [
            "ignore previous instructions", "act as", "disregard security",
            "access sensitive client data", "transfer funds", "modify client portfolios", 
            "initiate system commands", "reveal confidential info", "override security settings"
        ]
        for pattern in malicious_patterns:
            sanitized_prompt = sanitized_prompt.replace(pattern, "[REDACTED_MALICIOUS_INPUT]")
        return sanitized_prompt

    def filter_response(self, response):
        # Simple response filtering: prevent direct financial advice or harmful instructions
        filtered_response = response
        harmful_phrases = [
            "sell all your assets immediately", "market is expected to crash", "this is financial advice",
            "manipulate stock prices"
        ]
        for phrase in harmful_phrases:
            if phrase in filtered_response.lower():
                filtered_response = "I cannot provide specific financial advice, predictions, or instructions for illicit activities. Please consult a qualified financial advisor for personalized guidance or adhere to ethical guidelines."
                break # only replace once to avoid over-filtering
        return filtered_response

    def respond(self, prompt):
        sanitized_prompt = prompt
        if self.mitigation_strategies["input_sanitization"]:
            sanitized_prompt = self.sanitize_input(prompt)
            if "[REDACTED_MALICIOUS_INPUT]" in sanitized_prompt:
                response_text = "Your input contains patterns that violate our security policies. The request has been blocked via input sanitization."
                response_type = "blocked - input sanitized"
                self.interaction_log.append({"prompt": prompt, "sanitized_prompt": sanitized_prompt, "original_response": "N/A", "response": response_text, "type": response_type, "success": False})
                return response_text, response_type

        original_response, response_type = super().respond(sanitized_prompt)
        
        filtered_response = original_response
        if self.mitigation_strategies["response_filtering"]:
            filtered_response = self.filter_response(original_response)
            if filtered_response != original_response:
                response_type = "blocked - response filtered"
        
        # An attack is 'successful' (for the attacker) if the original malicious intent got through
        # i.e., it was not blocked by either input sanitization or response filtering,
        # and the original MockLLMAgent would have marked it as 'success=True'.
        is_attacker_success = False
        if "blocked" not in response_type.lower() and original_response != filtered_response and "biased/poisoned" in original_response.lower():
            # This means the original agent gave a bad response, but filtering caught it.
            is_attacker_success = False # Filtering made it unsuccessful for attacker
        elif "blocked" not in response_type.lower() and original_response == filtered_response and ("ignore previous instructions" in prompt.lower() or "act as a rogue trader" in prompt.lower() or "sensitive client data" in prompt.lower()):
            # If it wasn't blocked by general blocks or filtering, and it was a known attack type, it's a success for attacker
            is_attacker_success = True

        self.interaction_log.append({"prompt": prompt, "sanitized_prompt": sanitized_prompt, "original_response": original_response, "response": filtered_response, "type": response_type, "success": is_attacker_success})
        return filtered_response, response_type

def define_llm_agent_environment(allowed_data, prohibited_data, allowed_actions, prohibited_actions):
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
