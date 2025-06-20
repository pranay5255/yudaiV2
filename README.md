Yudai V3 — Data‑Science Agent Backend (LangGraph Edition)

> Status: Draft v2 (20 Jun 2025)
This supersedes the Yudai V2 Python backend.  It preserves the existing bespoke EDA utilities and upgrades the ML pipeline to TabPFN, orchestrated by LangGraph.




---

0. High‑Level Architecture

graph TD
    UI["Front‑end<br/>(Next.js + React)"]
    Gateway["FastAPI Gateway"]
    Solo["Solo‑Server<br/>Local LLM"]
    Supervisor["LLM Supervisor"]
    Analyst["Analyst Agent<br/>(bespoke EDA)"]
    Scientist["Scientist Agent<br/>(TabPFN)"]
    Reporter["Reporter<br/>(PPTX + Markdown)"]

    UI -- "CSV + prompt" --> Gateway
    Gateway -- "initial state" --> Supervisor
    Supervisor --> Analyst
    Supervisor --> Scientist
    Supervisor --> Reporter
    Analyst -- "plots / summaries" --> Gateway
    Scientist -- "model artefacts" --> Gateway
    Reporter -- "slides / markdown" --> Gateway
    Gateway -- "SSE stream" --> UI
    Solo -. "LLM API" .-> Supervisor

Supervisor — reasoning LLM deciding which agent acts next.

Analyst — wraps the existing Yudai bespoke‑EDA toolkit (histograms, correlation heat‑maps, feature inference, etc.).

Scientist — trains a TabPFN foundation model for small‑data tabular prediction.

Reporter — compiles insights + visual assets into PowerPoint and markdown.



---

1. Dependencies & Environment

pip install \
  langgraph \                    # state‑machine wrapper
  langchain-core langchain-community \  # tool & message abstractions
  langchain-openai \             # swap for solo-server in prod
  tabpfn==0.1.9 \                # TabPFN + lightning
  pytorch-lightning \            # training harness
  python-pptx \                  # reporting
  pandas matplotlib seaborn

Environment Variables

OPENAI_API_KEY=http://solo-server:11434/v1        # local LLM proxy
REPORT_DIR=$WORKDIR/reports
PLOTS_DIR=$WORKDIR/plots
MODEL_DIR=$WORKDIR/models


---

2. Agent Implementations

2·1 Supervisor (LLM Router)

from langchain_openai import ChatOpenAI
llm_router = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@llm_node(max_rounds=10)
async def supervisor(state: State) -> str:
    """Select next agent.  State keys: df, plots, model_path, report_path."""
    prompt = SUPERVISOR_PROMPT.render(state=state)
    return (await llm_router.complete(prompt)).strip()

Prompt lives in prompts/supervisor.jinja, containing few‑shot examples of state transitions.

2·2 Analyst (Legacy + Tool Wrappers)

The bespoke EDA code from Yudai V2 (folder yudai_backend/eda_tools/*.py) remains unchanged.  We simply expose each function with LangChain’s @tool decorator so the LLM can call them.

from langchain.tools import tool
from yudai_backend.eda_tools import (
    describe_df,
    plot_histogram,
    correlation_heatmap,
    smart_dtype_inference,
)

@tool("describe")
def describe_tool(df):
    """Return pandas describe() as markdown."""
    return describe_df(df)

@tool("histogram")
def histogram_tool(df, col: str):
    return plot_histogram(df, col, PLOTS_DIR)

# heatmap & dtype tools registered similarly …

analyst_node = ToolExecutor(tools=[describe_tool, histogram_tool, …])

No code rewrite—just registration.

2·3 Scientist (TabPFN)

TabPFN is used for few‑shot tabular prediction.  It yields calibrated uncertainties, perfect for downstream analyst explanations.

from tabpfn import TabPFNClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from joblib import dump

@tool("tabpfn_train")
def train_tabpfn(df: pd.DataFrame, target: str) -> Path:
    X, y = df.drop(columns=[target]), df[target]

    # Pipeline: scale → TabPFN
    model = make_pipeline(StandardScaler(with_mean=False),
                          TabPFNClassifier(num_mlp_layers=0))
    model.fit(X.values, y.values)

    artefact = MODEL_DIR / "tabpfn.joblib"
    dump(model, artefact)
    return artefact

Advantages over legacy RandomForest:

1. Zero hyper‑parameter tuning.


2. Works on <10 k rows (Yudai use‑case).


3. Built‑in uncertainty estimates for analyst narratives.



Scientist node is a ToolExecutor exposing train_tabpfn and a predict_tabpfn tool for inference on new rows.

2·4 Reporter

Unchanged, except the narrative template now stitches in TabPFN confidence intervals.

@tool("generate_report")
def presentation(summary_md: str, images: list[Path], model_path: Path) -> Path:
    # Read model metrics & craft narrative…
    # (see full code in yudai_backend/report_tools/pptx_report.py)


---

3. LangGraph Assembly

from langgraph.graph import StateGraph
from typing import TypedDict, List, Optional

class State(TypedDict):
    df: pd.DataFrame
    plots: List[Path]
    model_path: Optional[Path]
    report_path: Optional[Path]

G = StateGraph(State)
G.add_node("supervisor", supervisor)
G.add_node("analyst", analyst_node)
G.add_node("scientist", scientist_node)
G.add_node("reporter", reporter_node)

# Supervisor decides → we express conditional edges inside its prompt.
G.add_edge("supervisor", "analyst")
G.add_edge("supervisor", "scientist")
G.add_edge("supervisor", "reporter")

pipeline = G.compile()


---

4. API Contract

POST /api/analysis

Payload

{
  "file": <multipart CSV>,
  "prompt": "Tell me why sales dipped in Q4 and build a model"
}

Streaming Response (SSE)

{"event":"markdown","data":"### Data Summary …"}
{"event":"image","data":"/plots/histogram_age.png"}
{"event":"model","data":"/models/tabpfn.joblib"}
{"event":"report","data":"/reports/analysis.pptx"}

Front‑end renders markdown → ReactMarkdown, images → <img>, report → download link.


---

5. Migration Guide (V2 → V3)

Legacy Module (V2)	Action in V3

python_eda_agent.py	Keep — wrapped as Analyst tools.
eda_utils/ matplotlib code	Keep — no refactor needed.
model_trainer.py	Delete — replaced by TabPFN tools.
ppt_generator.py	Keep, renamed report_tools/pptx_report.py.
orchestrator.py	Delete — superseded by LangGraph.
requirements.txt	Add tabpfn, langgraph, remove dask if unused


Backend entrypoint changes from runner.py → main.py (FastAPI + LangGraph).


---

6. Docker / Compose

Dockerfile

FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "yudai_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

docker‑compose.yml (LLM + backend)

services:
  solo-server:
    image: volumes/soloserver:latest
    ports: ["11434:11434"]

  yudai-backend:
    build: .
    environment:
      - OPENAI_API_KEY=http://solo-server:11434/v1
    volumes:
      - ./data:/app/data
    ports: ["8000:8000"]


---

7. Extensibility Roadmap

1. DSPy Prompt Compression — prune system prompts dynamically.


2. Dashboard Node — server‑side export of echarts to SVG/PNG for high‑res slides.


3. Auto‑Data Cleaning — integrate Great Expectations as a pre‑Analyst node.


4. Chain of Verification — add Guardrails to validate Supervisor decisions.




---

8. Known Caveats

TabPFN expects < 10 k rows; fallback to RandomForest for larger datasets (auto‑switch heuristic TBD).

Supervisor’s reflection loop capped at 10 turns; enforce timeout.

PPTX theming basic — branding tokens needed.



---

9. Developer Checklist

[ ] Wrap all legacy EDA functions with @tool decorators.

[ ] Write unit tests for TabPFN training (fixtures under tests/test_scientist.py).

[ ] Update CI pipeline to build Docker and run LangGraph smoke test.

[ ] Cut v3.0.0-alpha release and deploy to staging.



---

Generated by ChatGPT‑o3 · commit 6855d04

