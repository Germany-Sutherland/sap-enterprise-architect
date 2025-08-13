# app.py — SAP AI Enterprise Architect — Agentic (Free Tier)
# Paste CHUNK 1/3, then CHUNK 2/3, then CHUNK 3/3 into one file.

import json
from datetime import datetime
from typing import Dict, List, Any

import numpy as np
import pandas as pd
import streamlit as st

# -----------------------------------------------------
# App Config
# -----------------------------------------------------
st.set_page_config(page_title="SAP AI Enterprise Architect (Free Tier)", layout="wide")
APP_NAME = "SAP AI Enterprise Architect — Agentic (Free)"
VERSION = "v2.1.0"

st.title("🏛️ SAP AI Enterprise Architect — Agentic (Free Tier)")
st.caption("20-agent analysis · GenAI/NLP-lite (rule-based) · Architecture + FMEA · 100% free & open-source")

# -----------------------------------------------------
# Lightweight knowledge base (open-source, rule-based)
# -----------------------------------------------------
SAP_MODULES: Dict[str, str] = {
    "FI": "Financial Accounting",
    "CO": "Controlling",
    "MM": "Materials Management",
    "SD": "Sales & Distribution",
    "PP": "Production Planning",
    "QM": "Quality Management",
    "PM": "Plant Maintenance",
    "EWM": "Extended Warehouse Mgmt",
    "TM": "Transportation Mgmt",
    "HCM": "Human Capital Mgmt",
    "SF": "SuccessFactors",
    "BW/4HANA": "Data Warehousing",
    "MDG": "Master Data Governance",
    "Ariba": "Ariba Procurement",
    "IBP": "Integrated Business Planning",
    "CRM": "Customer Relationship Mgmt",
    "S/4HANA": "S/4HANA Core",
    "Fiori": "Fiori UX"
}

MODULE_KEYWORDS: Dict[str, List[str]] = {
    "FI": ["invoice","ledger","account","finance","payable","receivable","tax","closing"],
    "CO": ["cost","controlling","profit","overhead","allocation"],
    "MM": ["procure","purchase","material","supplier","inventory","mrp"],
    "SD": ["order","sales","quote","delivery","billing","customer"],
    "PP": ["production","bom","routing","shopfloor","mrp","capacity"],
    "QM": ["quality","inspection","defect","compliance"],
    "PM": ["maintenance","asset","breakdown","work order"],
    "EWM": ["warehouse","putaway","picking","yard","slotting"],
    "TM": ["transport","freight","carrier","route","shipment"],
    "HCM": ["payroll","time","leave","hr","attendance"],
    "SF": ["successfactors","talent","recruit","performance","learning"],
    "BW/4HANA": ["report","bi","analytics","warehouse","kpi"],
    "MDG": ["master data","governance","golden record","mdm"],
    "Ariba": ["ariba","sourcing","contract","supplier portal"],
    "IBP": ["planning","demand","supply","inventory opt","sales ops","forecast"],
    "CRM": ["crm","customer care","ticket","service"],
}

NON_SAP_SYSTEMS = {
    "3PL/WMS": ["3pl","wms","logistics partner"],
    "Payment Gateway": ["payment","gateway","upi","card"],
    "Data Lake": ["data lake","lakehouse","delta"],
    "API Mgmt": ["api","integration","apim"],
    "IoT Gateway": ["iot","sensor","machine","edge"],
    "Edge Devices": ["edge","plc","raspberry"],
    "Analytics": ["power bi","tableau","dash","ml"],
    "CRM (Non-SAP)": ["salesforce","zendesk"],
}

HOSTING_CHOICES = ["S/4HANA Cloud", "On-Prem", "Hybrid"]

# -----------------------------------------------------
# Utility functions (NLP/LLM-lite)
# -----------------------------------------------------
def extract_requirements(text: str) -> Dict[str, Any]:
    """
    Lightweight NLP: keyword scoring to map to modules/integrations/hosting.
    100% open-source, no heavy models.
    """
    t = (text or "").lower()
    mod_scores = {m: 0 for m in SAP_MODULES}
    for mod, kws in MODULE_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                mod_scores[mod] += 1
    selected = [m for m, s in mod_scores.items() if s > 0]
    if selected and "S/4HANA" not in selected:
        selected.append("S/4HANA")
    if "fiori" not in t and "Fiori" not in selected:
        selected.append("Fiori")

    exts = []
    for sys, kws in NON_SAP_SYSTEMS.items():
        if any(kw in t for kw in kws):
            exts.append(sys)

    hosting = HOSTING_CHOICES[0]
    if "on-prem" in t or "on prem" in t or "datacenter" in t:
        hosting = "On-Prem"
    if "hybrid" in t:
        hosting = "Hybrid"

    scale_hint = 1000
    for n in [100, 500, 1000, 5000, 10000, 20000]:
        if str(n) in t:
            scale_hint = n

    return {
        "modules": selected or ["S/4HANA", "Fiori"],
        "external": exts,
        "hosting": hosting,
        "users": scale_hint
    }


def build_architecture(analysis: Dict[str, Any]) -> str:
    """Produce Graphviz DOT for Streamlit's st.graphviz_chart."""
    mods = analysis["modules"]
    exts = analysis["external"]
    hosting = analysis["hosting"]

    edges = []
    # Core landscape
    edges.append(("Users", "Fiori"))
    edges.append(("Fiori", "S/4HANA"))
    edges.append(("S/4HANA", hosting))
    for m in mods:
        if m not in ("S/4HANA", "Fiori"):
            edges.append((m, "S/4HANA"))
    for x in exts:
        edges.append((x, "S/4HANA"))
    nodes = sorted({n for a, b in edges for n in (a, b)})

    dot = ["digraph G {"]
    dot.append("rankdir=LR; node [shape=box, style=rounded];")
    for n in nodes:
        dot.append(f"\"{n}\";")
    for a, b in edges:
        dot.append(f"\"{a}\" -> \"{b}\";")
    dot.append("}")
    return "\n".join(dot)

def agent_say(name: str, finding: str) -> Dict[str, str]:
    return {"agent": name, "finding": finding}

# -----------------------------------------------------
# 20-Agent roster (extendable) + rules
# -----------------------------------------------------
AGENTS = [
    "Requirements Analyst",
    "Process Mapper",
    "Module Recommender",
    "Integration Planner",
    "Data Architect",
    "Security Architect",
    "Performance Engineer",
    "Sizing Optimizer",
    "Risk Analyst",
    "Compliance Officer",
    "Cost Estimator",
    "Change Manager",
    "Test Manager",
    "IoT Architect",
    "Disaster Recovery Planner",
    "Localization Lead",
    "Data Privacy Officer",
    "Monitoring & SRE",
    "Master Data Lead",
    "Analytics Lead"
]

AGENT_RULES: Dict[str, Any] = {
    "Module Recommender": lambda a: (
        "Recommend modules: "
        + (", ".join([m for m in a["modules"] if m not in ["S/4HANA", "Fiori"]]) or "Core S/4HANA only")
        + "."
    ),
    "Integration Planner": lambda a: "Integrations required: "
        + (", ".join(a["external"]) if a["external"] else "Standard SAP APIs only."),
    "Data Architect": lambda a: "Use BW/4HANA for enterprise KPIs; add MDG for golden records if multiple ERPs.",
    "Security Architect": lambda a: "SSO (SAML/OIDC), role-based access, SoD, encryption in transit/at rest.",
    "Performance Engineer": lambda a: f"Tune for ~{a['users']} named users; cache OData; batch heavy jobs off-hours.",
    "Sizing Optimizer": lambda a: "Start with 3 app nodes; right-size HANA (256–512GB) and scale after load tests.",
    "Risk Analyst": lambda a: "Risks: integration delays, data quality, custom code creep, change fatigue.",
    "Compliance Officer": lambda a: "Ensure GDPR/SoX, audit trails, eInvoicing/local fiscal packs where applicable.",
    "Cost Estimator": lambda a: "Prefer configuration over customization; keep interfaces standard to cut TCO.",
    "Change Manager": lambda a: "Fit-to-Standard, iterative releases, strong training & hypercare.",
    "Test Manager": lambda a: "Automate regression for O2C, P2P, RtR, MTS/MTO; include performance smoke tests.",
    "IoT Architect": lambda a: "Edge filters anomalies; stream events via IoT Gateway; avoid raw telemetry floods.",
    "Process Mapper": lambda a: "Scope: O2C (SD), P2P (MM/Ariba), RtR (FI/CO), Mfg (PP/QM/PM), Logistics (EWM/TM).",
    "Requirements Analyst": lambda a: "Clarify order volumes, SKUs, close timelines, SLAs, reporting, and security.",
    "Disaster Recovery Planner": lambda a: "RPO ≤ 15m, RTO ≤ 2h; enable HANA backups, cross-region DR if Hybrid/Cloud.",
    "Localization Lead": lambda a: "Install localizations (e.g., eWaybill, GST/eInvoice, SAF-T) based on countries.",
    "Data Privacy Officer": lambda a: "Minimize PII in logs; masking/pseudonymization; retention & consent controls.",
    "Monitoring & SRE": lambda a: "Set up end-to-end monitoring, alerting, SLOs; trace critical business flows.",
    "Master Data Lead": lambda a: "Define ownership, stewardship; validations; duplicate prevention; MDG governance.",
    "Analytics Lead": lambda a: "Define KPI catalog; semantic layer; near-real-time replication to BW/4 or lake."
}

def run_agents(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    findings = []
    for name in AGENTS:
        rule = AGENT_RULES.get(name)
        try:
            text = rule(analysis) if callable(rule) else "No rule configured."
        except Exception as e:
            text = f"Error: {e}"
        findings.append(agent_say(name, text))
    return findings


def gen_explanation(analysis: Dict[str, Any], findings: List[Dict[str, str]]) -> str:
    """
    LLM-lite narrative composed from agent findings (template-based).
    This avoids paid APIs and heavy models but still reads like an executive summary.
    """
    modules = ", ".join(analysis["modules"])
    integrations = ", ".join(analysis["external"]) if analysis["external"] else "none"

    lines = [
        f"We analyzed your requirements and mapped them to modules: {modules}.",
        f"Hosting model: {analysis['hosting']}. External systems: {integrations}.",
        "",
        "Key specialist assessments:",
    ]
    for m in findings:
        lines.append(f"- **{m['agent']}**: {m['finding']}")
    lines.append("")
    lines.append(
        "Overall recommendation: adopt Fit-to-Standard on S/4HANA, minimize customizations, "
        "enforce strong data governance (MDG), automate testing, and keep integrations standard."
    )
    return "\n".join(lines)

# -----------------------------
# FMEA generation (open-source)
# -----------------------------
def build_fmea(analysis: Dict[str, Any]) -> pd.DataFrame:
    """
    Create an FMEA table for the proposed architecture using simple risk rules.
    Severity, Occurrence, Detection are scored 1–10; RPN = S * O * D.
    """
    rows = []
    components = (
        ["Fiori", "S/4HANA", analysis["hosting"]]
        + [m for m in analysis["modules"] if m not in ["S/4HANA", "Fiori"]]
        + analysis["external"]
    )

    base_risks = {
        "Fiori": (5, 4, 6, "UX performance under load"),
        "S/4HANA": (7, 3, 4, "Data model or custom code defects"),
        "On-Prem": (6, 4, 5, "Capacity planning & patching"),
        "S/4HANA Cloud": (4, 3, 6, "Release change impact"),
        "Hybrid": (6, 5, 6, "Network latency & split ops"),
    }

    for c in components:
        sev, occ, det, mode = base_risks.get(c, (5, 3, 6, "General failure mode"))
        if c in analysis["external"]:
            sev = min(10, sev + 1)
            occ = min(10, occ + 2)
            mode = "Integration latency/contract changes"
        rpn = sev * occ * det
        rows.append({
            "Component": c,
            "Failure Mode": mode,
            "Severity": sev,
            "Occurrence": occ,
            "Detection": det,
            "RPN": rpn,
            "Recommended Action": "Add monitoring, SLAs, automated tests, fallback paths, and operational runbooks."
        })

    df = pd.DataFrame(rows).sort_values("RPN", ascending=False).reset_index(drop=True)
    return df

# -----------------------------------------------------
# UI — Sidebar (global settings)
# -----------------------------------------------------
with st.sidebar:
    st.title(APP_NAME)
    st.caption(f"{VERSION} · Free & open-source · No external APIs")
    users = st.number_input("Estimated named users", 50, 20000, 1000, step=50)
    baseline_weeks = st.number_input("Baseline timeline (weeks)", 4, 104, 16)
    st.markdown("---")
    st.caption("Tip: Paste requirements below. The agent team will analyze and propose an architecture.")

# -----------------------------------------------------
# Tabs
# -----------------------------------------------------
T1, T2, T3, T4 = st.tabs(["Requirements & Agents", "Architecture", "Explanation", "FMEA & Export"])

with T1:
    st.subheader("1) Requirements & Agentic Analysis (20 agents)")
    req = st.text_area(
        "Paste SAP enterprise requirements",
        height=160,
        placeholder="e.g., We process 5k orders/day, need EWM for DC, Ariba sourcing, integrate with 3PL and payment gateway, "
                    "IBP for planning, and monthly financial close in 2 days..."
    )
    run = st.button("Run Agentic Analysis")
    if run:
        analysis = extract_requirements(req)
        analysis["users"] = users
        st.session_state["analysis"] = analysis
        st.success("Analysis extracted. Switch tabs to view Architecture, Explanation, and FMEA.")

    if "analysis" in st.session_state:
        st.json(st.session_state["analysis"])
        st.caption("Parsed modules, external systems, hosting, and scale from your text.")

with T2:
    st.subheader("2) Proposed SAP Enterprise Architecture")
    if "analysis" in st.session_state:
        dot = build_architecture(st.session_state["analysis"])
        st.graphviz_chart(dot, use_container_width=True)
    else:
        st.info("Run the Agentic Analysis first.")

with T3:
    st.subheader("3) GenAI/NLP-lite Explanation")
    if "analysis" in st.session_state:
        findings = run_agents(st.session_state["analysis"])  # 20 agents
        st.session_state["findings"] = findings
        narrative = gen_explanation(st.session_state["analysis"], findings)
        st.markdown(narrative)
        st.markdown("_This narrative is generated by open-source, rule-based templates (LLM-lite)._")
    else:
        st.info("Run the Agentic Analysis first.")

with T4:
    st.subheader("4) FMEA of the Proposed SAP Enterprise Architecture")
    if "analysis" in st.session_state:
        df_fmea = build_fmea(st.session_state["analysis"])
        st.dataframe(df_fmea, use_container_width=True)
        bundle = {
            "generated_at": datetime.utcnow().isoformat(),
            "analysis": st.session_state["analysis"],
            "findings": st.session_state.get("findings", []),
            "fmea": df_fmea.to_dict(orient="records"),
        }
        st.download_button(
            "Download Bundle (JSON)",
            data=json.dumps(bundle, indent=2),
            file_name="sap_architecture_with_fmea.json",
            mime="application/json"
        )
    else:
        st.info("Run the Agentic Analysis first.")
