# sap-enterprise-architect


# SAP Enterprise Architecture Generator (Free-tier MVP)

This is a minimal **Streamlit app** that simulates using **Gen AI + NLP + LLM + Agentic AI Agents** to:
- Analyze SAP Enterprise Architecture requirements
- Generate a proposed architecture diagram
- Provide an **FMEA (Failure Mode and Effects Analysis)**

## Features
- **20 simulated AI agents** analyzing input requirements
- Architecture diagram rendered using Streamlit's built-in Graphviz support
- FMEA table showing potential risks, effects, and severity

## How to Run (Locally)
```bash
pip install -r requirements.txt
streamlit run app.py
