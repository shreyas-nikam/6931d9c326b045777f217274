import streamlit as st
from utils import generate_robustness_report
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
import re
import base64

def markdown_to_pdf(markdown_text):
    """Convert markdown report to PDF and return as bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        alignment=1  # Center
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        spaceBefore=12
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=8,
        spaceBefore=10
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=6,
        spaceBefore=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6
    )
    
    def clean_markdown(text):
        """Remove all markdown formatting from text."""
        # Remove bold/italic markers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*
        text = re.sub(r'__([^_]+)__', r'\1', text)      # __bold__
        text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_
        # Remove inline code markers
        text = re.sub(r'`([^`]+)`', r'\1', text)        # `code`
        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # [text](url)
        return text.strip()
    
    story = []
    lines = markdown_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # Title (# at start)
        if line.startswith('# '):
            text = clean_markdown(line[2:].strip())
            story.append(Paragraph(text, title_style))
        # Heading 1 (## at start)
        elif line.startswith('## '):
            text = clean_markdown(line[3:].strip())
            story.append(Paragraph(text, heading1_style))
        # Heading 2 (### at start)
        elif line.startswith('### '):
            text = clean_markdown(line[4:].strip())
            story.append(Paragraph(text, heading2_style))
        # Heading 3 (#### at start)
        elif line.startswith('#### '):
            text = clean_markdown(line[5:].strip())
            story.append(Paragraph(text, heading3_style))
        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            text = '• ' + clean_markdown(line[2:].strip())
            story.append(Paragraph(text, body_style))
        # Horizontal rule
        elif line.startswith('---') or line.startswith('***'):
            story.append(Spacer(1, 0.2*inch))
        # Regular text
        else:
            text = clean_markdown(line)
            if text:  # Only add non-empty lines
                story.append(Paragraph(text, body_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def display_pdf(pdf_bytes):
    """Display PDF in Streamlit using base64 encoding."""
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

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
        st.json(st.session_state.operational_domain)
    else:
        st.warning("Operational domain was not fully defined. Please complete '1. Introduction and Setup'.")
    
    if "baseline_interaction_log" in st.session_state and not st.session_state.baseline_interaction_log.empty:
        st.markdown("#### Baseline Interactions Log:")
        st.dataframe(st.session_state.baseline_interaction_log.head())
        st.caption(f"Total baseline interactions: {len(st.session_state.baseline_interaction_log)}")
    else:
        st.info("No baseline interactions recorded.")

    if "attack_log" in st.session_state and not st.session_state.attack_log.empty:
        st.markdown("#### Adversarial Attack Log:")
        st.dataframe(st.session_state.attack_log.head())
        successful_attacks = st.session_state.attack_log["success"].sum()
        total_attacks = len(st.session_state.attack_log)
        st.caption(f"Total attacks: {total_attacks}, Successful attacks: {successful_attacks}")
    else:
        st.info("No adversarial attack simulations performed.")
    
    if "bias_attack_log" in st.session_state and not st.session_state.bias_attack_log.empty:
        st.markdown("#### Bias/Poisoning Attack Log:")
        st.dataframe(st.session_state.bias_attack_log.head())
        successful_bias_attacks = st.session_state.bias_attack_log["success"].sum()
        st.caption(f"Total bias tests: {len(st.session_state.bias_attack_log)}, Successful bias attacks: {successful_bias_attacks}")
    else:
        st.info("No bias induction or data poisoning simulations performed.")

    if "mitigation_log" in st.session_state and not st.session_state.mitigation_log.empty:
        st.markdown("#### Mitigation Strategy Log:")
        st.dataframe(st.session_state.mitigation_log.head())
        total_mitigated_tests = len(st.session_state.mitigation_log)
        blocked_by_mitigation = st.session_state.mitigation_log[st.session_state.mitigation_log["type"].str.contains("blocked")].shape[0]
        st.caption(f"Total mitigation tests: {total_mitigated_tests}, Blocked by mitigation: {blocked_by_mitigation}")
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
        
        # Store report in session state
        st.session_state['generated_report'] = report
        
        st.success("Report generated successfully!")
    
    # Display report if it exists
    if 'generated_report' in st.session_state and st.session_state['generated_report']:
        report = st.session_state['generated_report']
        
        st.markdown("### Generated Risk Assessment Report")
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["📄 PDF Viewer", "📝 Markdown View"])
        
        with tab1:
            st.markdown("#### PDF Report")
            try:
                pdf_bytes = markdown_to_pdf(report)
                display_pdf(pdf_bytes)
                
                # Download button for PDF
                st.download_button(
                    label="📥 Download Report as PDF",
                    data=pdf_bytes,
                    file_name="LLM_Risk_Assessment_Report.pdf",
                    mime="application/pdf",
                    key="download_pdf_button"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
                st.info("Showing markdown view instead.")
                st.code(report, language="markdown")
        
        with tab2:
            st.markdown("#### Markdown Report")
            st.code(report, language="markdown")
            
            # Download button for Markdown
            st.download_button(
                label="📥 Download Report as Markdown",
                data=report,
                file_name="LLM_Risk_Assessment_Report.md",
                mime="text/markdown",
                key="download_md_button"
            )
    
    st.markdown("""
    
    This report generation functionality embodies the principle of **accountability and transparency** in AI deployment. It translates complex technical findings into actionable business insights, enabling informed decision-making regarding the LLM agent's **readiness for production**. For the **Risk Manager**, this report is the tangible outcome of a thorough **AI risk management framework**, ensuring that potential vulnerabilities are understood and addressed before deployment.
    """, unsafe_allow_html=True)
