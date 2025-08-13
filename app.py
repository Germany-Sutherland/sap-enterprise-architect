import streamlit as st
import pandas as pd

# ---- Core Agent Functions ---- #
def agent_business_analysis(req):
    return {"modules": ["S/4HANA", "Fiori", "BW/4HANA"], "external": []}

def agent_architecture_design(parsed):
    return {"hosting": "S/4HANA Cloud", "integration": ["SAP Cloud Connector"], "security": ["Role-Based Access Control"]}

def agent_scalability(parsed):
    return {"scalability": "Supports 1k+ users", "db": "HANA DB"}

def agent_explanation(parsed, design):
    return f"This architecture uses {', '.join(parsed['modules'])} hosted on {design['hosting']} with integrations {', '.join(design['integration'])}."

def agent_fmea(parsed, design):
    data = [
        ["Module Failure", "Data loss risk", 8, 7, 6],
        ["Integration Failure", "Downtime risk", 9, 5, 4]
    ]
    df = pd.DataFrame(data, columns=["Failure Mode", "Effect", "Severity", "Occurrence", "Detection"])
    df["RPN"] = df["Severity"] * df["Occurrence"] * df["Detection"]
    return df

# ---- Streamlit UI ---- #
st.set_page_config(page_title="SAP AI Enterprise Architect - MVP", layout="wide")
st.title("SAP AI Enterprise Architect — Agentic (Free)")

req_text = st.text_area("Paste SAP enterprise requirements", height=150)

if st.button("Run Agentic Analysis"):
    parsed = agent_business_analysis(req_text)
    design = agent_architecture_design(parsed)
    scale = agent_scalability(parsed)
    explanation = agent_explanation(parsed, design)
    fmea_df = agent_fmea(parsed, design)

    st.subheader("Parsed Requirements")
    st.json(parsed)

    st.subheader("Proposed Architecture")
    dot = f"""
    digraph G {{
        rankdir=LR;
        node [shape=box];
        {" -> ".join(parsed['modules'])};
        "{parsed['modules'][-1]}" -> "{design['hosting']}";
    }}
    """
    st.graphviz_chart(dot)  # This uses Streamlit's built-in Graphviz

    st.subheader("Explanation")
    st.write(explanation)

    st.subheader("FMEA of Proposed Architecture")
    st.dataframe(fmea_df)

    st.success("Analysis complete!")
