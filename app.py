import os
import io
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Any, Tuple

import numpy as np
import pandas as pd
import streamlit as st
import networkx as nx

# Optional imports guarded to keep free tier happy
try:
    from pdfminer.high_level import extract_text as pdf_extract_text
    PDF_OK = True
except Exception:
    PDF_OK = False

# ---------------
# App Constants
# ---------------
APP_NAME = "SAP AI Architect (Agentic) — Free Tier"
VERSION = "v1.0.0"

SAP_MODULES = {
    "FI": "Financial Accounting",
    "CO": "Controlling",
    "MM": "Materials Management",
    "SD": "Sales and Distribution",
    "PP": "Production Planning",
    "QM": "Quality Management",
    "PM": "Plant Maintenance",
    "WM": "Warehouse Management",
    "EWM": "Extended Warehouse Management",
    "TM": "Transportation Management",
    "HCM": "Human Capital Management",
    "SF": "SuccessFactors",
    "BW/4HANA": "Data Warehousing",
    "MDG": "Master Data Governance",
    "Ariba": "Procurement Ariba",
    "IBP": "Integrated Business Planning",
    "CRM": "Customer Relationship Management",
    "S4HANA": "S/4HANA Core",
}

MODULE_KEYWORDS = {
    "FI": ["invoice", "ledger", "account", "finance", "payable", "receivable", "tax", "closing"],
    "CO": ["cost", "controlling", "profit center", "overhead", "allocation"],
    "MM": ["procure", "purchase", "material", "supplier", "inventory"],
    "SD": ["order", "sales", "quote", "delivery", "billing", "customer"],
    "PP": ["production", "mrp", "manufactur", "bom", "routing", "shopfloor"],
    "QM": ["quality", "inspection", "defect", "compliance"],
    "PM": ["maintenance", "asset", "breakdown", "work order"],
    "WM": ["warehouse", "putaway", "picking", "bins"],
    "EWM": ["ewm", "yard", "labor management", "wave", "slotting"],
    "TM": ["transport", "shipment", "freight", "carrier", "route"],
    "HCM": ["payroll", "time", "leave", "hr", "attendance"],
    "SF": ["successfactors", "talent", "recruit", "performance", "learning"],
    "BW/4HANA": ["report", "bi", "analytics", "warehouse", "kpi"],
    "MDG": ["master data", "governance", "golden record", "mdm"],
    "Ariba": ["ariba", "sourcing", "contract", "supplier portal"],
    "IBP": ["planning", "demand", "supply", "inventory opt", "sales ops"],
    "CRM": ["crm", "customer care", "ticket", "service"],
    "S4HANA": ["s/4", "s4hana", "central finance", "core"],
}

# -------------------------
# Minimal Agentic Framework
# -------------------------
class Message(Dict[str, Any]):
    pass

class Tool:
    name: str
    desc: str
    def __init__(self, name: str, desc: str, fn):
        self.name = name
        self.desc = desc
        self.fn = fn
    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

class Agent:
    def __init__(self, name: str, role: str, style: str, tools: List[Tool]):
        self.name = name
        self.role = role
        self.style = style  # persona writing style
        self.tools = {t.name: t for t in tools}

    def think(self, prompt: str, scratch: Dict[str, Any]) -> Message:
        """Heuristic LLM-free thinking: plan → act → reflect."""
        # Simple planning by keywords
        plan = []
        p = prompt.lower()
        if any(k in p for k in ["diagram", "landscape", "architecture"]):
            plan.append("Propose SAP modules and draw a landscape.")
        if any(k in p for k in ["cost", "size", "optimi", "budget"]):
            plan.append("Run optimizer for size/cost trade-offs.")
        if any(k in p for k in ["risk", "delay", "timeline"]):
            plan.append("Run risk simulation and mitigation list.")
        if not plan:
            plan.append("Clarify requirements and propose next steps.")

        # Tool selection
        actions = []
        if "optimizer" in " ".join(plan).lower() and "optimize" in self.tools:
            actions.append(("optimize", {}))
        if "draw" in " ".join(plan).lower() and "design_arch" in self.tools:
            actions.append(("design_arch", {}))
        if "risk" in " ".join(plan).lower() and "risk_sim" in self.tools:
            actions.append(("risk_sim", {}))

        # Execute tools
        results = {}
        for name, kwargs in actions:
            try:
                results[name] = self.tools[name](scratch)
            except Exception as e:
                results[name] = {"error": str(e)}

        # Reflection (very light):
        reflection = "Review results for consistency; propose actionable next steps and assumptions."
        text = f"Plan: {plan}\nResults: {list(results.keys())}\nReflection: {reflection}"
        return {"agent": self.name, "role": self.role, "content": text, "results": results, "time": datetime.utcnow().isoformat()}

# --------------------
# Tools (Free‑tier safe)
# --------------------

def tool_design_arch(scratch: Dict[str, Any]) -> Dict[str, Any]:
    req = scratch.get("requirements", "")
    modules = map_requirements_to_modules(req)
    edges = [("User", "Fiori"), ("Fiori", "S4HANA")]
    for m in modules:
        if m != "S4HANA":
            edges.append((m, "S4HANA"))
    nodes = list({n for e in edges for n in e})
    dot = ["digraph G {"]
    dot.append("rankdir=LR; node [shape=box, style=rounded];")
    for n in nodes:
        dot.append(f'"{n}";')
    for a,b in edges:
        dot.append(f'"{a}" -> "{b}";')
    dot.append("}")
    return {"modules": modules, "dot": "\n".join(dot)}


def tool_optimize(scratch: Dict[str, Any]) -> Dict[str, Any]:
    # Quantum‑inspired simulated annealing for size/cost
    rng = np.random.default_rng(42)
    demand = max(50, min(20000, int(scratch.get("users", 1000))))
    # decision vars: [app_servers, hana_size_gb]
    x = np.array([3, 256], dtype=float)
    T = 10.0
    def cost(x):
        app, hana = x
        perf_penalty = max(0, demand/500 - app) ** 2 + max(0, demand/5 - hana) ** 2
        infra_cost = app*200 + hana*3
        return infra_cost + 50*perf_penalty
    best = x.copy(); bestc = cost(x)
    for _ in range(400):
        cand = x + rng.normal(0, [1, 20])
        cand[0] = max(1, cand[0])
        cand[1] = max(64, cand[1])
        c = cost(cand)
        if c < bestc or rng.random() < np.exp((bestc - c)/max(1e-6, T)):
            x, best, bestc = cand, cand.copy(), c
        T *= 0.98
    return {"users": demand, "app_servers": int(round(best[0])), "hana_gb": int(round(best[1])), "score": round(bestc,2)}


def tool_risk_sim(scratch: Dict[str, Any]) -> Dict[str, Any]:
    rng = np.random.default_rng(123)
    base_weeks = scratch.get("timeline_weeks", 16)
    interfaces = scratch.get("interfaces", 10)
    complexity = scratch.get("complexity", 0.5)  # 0..1
    N = 2000
    durations = []
    for _ in range(N):
        risk_factor = rng.normal(1 + 0.5*complexity + interfaces/100.0, 0.1)
        durations.append(base_weeks * max(0.7, risk_factor))
    arr = np.array(durations)
    p80 = float(np.quantile(arr, 0.8))
    p90 = float(np.quantile(arr, 0.9))
    return {"p50": round(float(np.median(arr)),1), "p80": round(p80,1), "p90": round(p90,1)}


# --------------
# Helper functions
# --------------

def map_requirements_to_modules(text: str) -> List[str]:
    t = (text or "").lower()
    scores = {k:0 for k in SAP_MODULES}
    for mod, kws in MODULE_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                scores[mod] += 1
    # Always include S4 core if anything triggered
    modules = [m for m,s in scores.items() if s>0]
    if modules and "S4HANA" not in modules:
        modules.append("S4HANA")
    # If nothing matched, default to core discovery
    return modules or ["S4HANA"]


def parse_pdf(file_bytes: bytes) -> str:
    if not PDF_OK:
        return "PDF parser unavailable on this deploy."
    with io.BytesIO(file_bytes) as f:
        try:
            text = pdf_extract_text(f)
            return text[:10000]  # keep it light
        except Exception as e:
            return f"PDF parse error: {e}"


# -----------------------
# Streamlit UI Components
# -----------------------

def sidebar_state():
    st.sidebar.title(APP_NAME)
    st.sidebar.caption(f"{VERSION} · free‑tier friendly")
    with st.sidebar.expander("Global Settings"):
        users = st.number_input("Concurrent named users (estimate)", 50, 20000, 1000, step=50)
        interfaces = st.number_input("# of interfaces", 0, 200, 10, step=1)
        complexity = st.slider("Solution complexity", 0.0, 1.0, 0.5)
        timeline_weeks = st.number_input("Baseline timeline (weeks)", 4, 104, 16)
        st.session_state.setdefault("scratch", {})
        st.session_state.scratch.update({
            "users": users,
            "interfaces": interfaces,
            "complexity": complexity,
            "timeline_weeks": timeline_weeks,
        })
    st.sidebar.markdown("---")
    st.sidebar.caption("Optional: set OPENAI_API_KEY in Secrets for richer text output
