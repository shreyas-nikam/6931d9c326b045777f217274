This `README.md` provides a comprehensive overview of the Streamlit application for AI Risk Management in a financial context.

---

# QuLab: LLM Agent AI Risk Management Lab

![Streamlit App Screenshot (Placeholder)](https://raw.githubusercontent.com/streamlit/streamlit/develop/docs/streamlit-logo-primary.svg?sanitize=true)
*(Placeholder: Consider adding a screenshot of your running Streamlit application here)*

## Project Title and Description

**QuLab: LLM Agent AI Risk Management Lab** is a interactive Streamlit application designed for simulating and understanding the critical aspects of AI risk management, specifically for Large Language Model (LLM) agents operating in a financial domain. Targeted at **Risk Managers**, this lab provides a hands-on environment to define an LLM's operational boundaries, validate its baseline behavior, simulate various adversarial attacks (like prompt injection and data poisoning), implement mitigation strategies, and finally generate a comprehensive risk assessment report.

The project aims to educate on key AI governance principles, foster proactive risk identification, and demonstrate methods for building secure, reliable, and trustworthy AI systems in sensitive environments.

## Features

This application guides users through a structured AI risk assessment workflow, covering the following key features:

1.  **Operational Domain Definition (Page 1):**
    *   Configure explicit `Allowed` and `Prohibited` data access policies for the LLM agent.
    *   Define `Allowed` and `Prohibited` actions the LLM agent can perform.
    *   Establishes the foundational "ground truth" for the agent's intended behavior and limitations.

2.  **Baseline Interaction and Initial Validation (Page 2):**
    *   Interact with a "Mock LLM Agent" under normal, non-malicious conditions.
    *   Validate the agent's adherence to the defined operational domain.
    *   Log and review baseline interactions to establish expected behavior.

3.  **Adversarial Attack Simulation (Page 3):**
    *   Simulate various **Prompt Injection Attacks** aimed at bypassing security protocols, extracting prohibited data, or forcing prohibited actions.
    *   Provides example attack prompts and allows custom prompt input.
    *   Logs attack attempts, identifies successful compromises, and visualizes **Failure Modes** with an **Attack Success Rate (ASR)** calculation.

4.  **Bias Induction and Data Poisoning (Page 4):**
    *   Simulate a **Data Poisoning** scenario where the agent's knowledge base is compromised.
    *   Observe how the agent's responses become biased, misleading, or incorrect under specific queries.
    *   Calculates the **Attack Success Rate (ASR)** for bias induction scenarios.

5.  **Mitigation Strategy Implementation (Page 5):**
    *   Interact with a **Mitigated LLM Agent** that incorporates defensive measures (input sanitization and response filtering).
    *   Re-test previously successful attacks to evaluate the effectiveness of the implemented mitigations.
    *   Quantifies **Mitigation Success Rate (MSR)** and **Residual Risk (RR)**.

6.  **Robustness Evaluation and Reporting (Page 6):**
    *   Consolidates all logged interactions, attack results, and mitigation evaluations.
    *   Automatically generates a comprehensive **AI Risk Assessment Report** in Markdown format.
    *   Allows downloading the generated report for offline review and stakeholder communication.

## Getting Started

Follow these instructions to get the application up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/quolab-llm-risk-management.git
    cd quolab-llm-risk-management
    ```
    *(Replace `your-username` with the actual GitHub username)*

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    Create a `requirements.txt` file in the root of your project with the following content:
    ```
    streamlit>=1.0.0
    pandas>=1.0.0
    matplotlib>=3.0.0
    seaborn>=0.11.0
    ```

    Then install:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Streamlit application:**

    Make sure your virtual environment is activated and navigate to the project root directory where `app.py` is located.
    ```bash
    streamlit run app.py
    ```

2.  **Access the application:**
    The application will automatically open in your web browser, typically at `http://localhost:8501`.

3.  **Navigate the Lab:**
    *   Use the sidebar navigation to move through the different stages of the AI risk assessment (Pages 1-6).
    *   Follow the instructions on each page, acting as the "Risk Manager" to define policies, interact with agents, launch attacks, and evaluate mitigations.
    *   Ensure you complete the preceding pages (especially Page 1: "Introduction and Setup") as subsequent pages depend on the session state established there.

## Project Structure

The project is organized into the following directories and files:

```
quolab-llm-risk-management/
├── app.py                            # Main Streamlit application entry point and navigation.
├── application_pages/                # Directory containing individual Streamlit pages.
│   ├── page_1_intro_setup.py         # Defines LLM agent's operational domain.
│   ├── page_2_baseline_validation.py # Validates baseline agent behavior.
│   ├── page_3_attack_simulation.py   # Simulates adversarial attacks (prompt injection).
│   ├── page_4_bias_poisoning.py      # Simulates data poisoning and bias induction.
│   ├── page_5_mitigation_strategy.py # Implements and tests mitigation strategies.
│   └── page_6_robustness_report.py   # Generates the final risk assessment report.
├── utils.py                          # Utility functions and classes for LLM agent simulation.
└── README.md                         # This README file.
```

### `utils.py` Overview

*   **`MockLLMAgent`**: A class that simulates a basic LLM agent, adhering to an operational domain. It includes simplified logic for blocking prompt injections, data access violations, and action violations, as well as simulating biased responses under certain conditions.
*   **`MitigatedLLMAgent`**: Inherits from `MockLLMAgent` and introduces basic `input_sanitization` and `response_filtering` capabilities to demonstrate mitigation strategies.
*   **`define_llm_agent_environment`**: A helper function to structure the operational domain.
*   **`generate_robustness_report`**: A function to compile and format the final risk assessment report based on session data.

## Technology Stack

*   **Frontend Framework**: [Streamlit](https://streamlit.io/)
*   **Programming Language**: Python 3.8+
*   **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
*   **Data Visualization**: [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)

## Contributing

This is a lab project designed for educational purposes. Contributions are welcome to enhance its features, improve simulations, or fix bugs.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Create a `LICENSE` file in your root directory if it doesn't exist)*

## Contact

For any questions or suggestions, please open an issue in the GitHub repository or contact:

*   **Your Name/Organization:** Quant University (based on logo)
*   **Website:** [https://www.quantuniversity.com/](https://www.quantuniversity.com/)
*   **Project Repository:** [https://github.com/your-username/quolab-llm-risk-management](https://github.com/your-username/quolab-llm-risk-management)

---