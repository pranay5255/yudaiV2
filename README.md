# Yudai V2 — **Lean MVP (4‑Week) Roadmap & PRD**

> **Goal:** Ship a demo‑ready, fully‑local version of Yudai V2 that turns a **CSV + prompt** into a tested dbt model and an interactive dashboard rendered with **echarts‑for‑react**.

---

## 0 · Strategic Changes ("Ruthless Subtraction")

|✅ **Keep**|❌ **Cut**|➕ **Add**|
|---|---|---|
|Next.js + React frontend|Manual Python DAG logic|**dbt‑Core (+ DuckDB adapter)** as the single transformation layer|
|`echarts-for-react` chart wrapper|Spark & BigQuery connectors|**Python Subprocess Orchestrator** 👉 executes dbt commands based on prompt|
|Solo‑Server Docker for on‑board LLM|Streaming (Kafka/Kinesis)|**Dataset versioning** via dbt snapshots & hashed file paths|
|Python EDA agents (Dask optional)|Slack / Monte‑Carlo observability|**/api/dashboards** endpoint that returns a JSON payload each chart slice consumes|

The result is a lighter stack that fits on a laptop yet proves the full prompt→pipeline→chart loop.

---

## 1 · One‑Month Roadmap (Week‑by‑Week)

|Week|Theme|Must‑Do Tasks|Deliverables|
|---|---|---|---|
|**W‑1**|**Repo Cleanup + Scaffold**|– Delete manual DAG code.– Add `dbt_project.yml` (duckdb profile).– Implement a Python script (`orchestrate_dbt.py`) that can execute `dbt seed → run → test` using subprocesses.– Ensure `echarts-for-react` + Tailwind compile.|Monorepo boots via `./dev_up.sh`; Python script successfully runs dbt commands; React page renders a static ECharts demo.|
|**W‑2**|**Prompt→dbt Codegen**|– Extend Orchestrator agent: emits dbt model SQL + `tests.yml` + snapshot when user submits prompt.– Store files in `/models/generated/` and trigger the `orchestrate_dbt.py` script with necessary parameters.– Version incoming CSV with `<sha256>.csv`.|Prompt produces passing dbt tests; table appears in DuckDB; Python orchestration script runs successfully.|
|**W‑3**|**API + Chart Generator**|– Define `/api/dashboards/:id` that returns `{ charts: [ { id, echartsOptions } ], data: {...} }`.– LLM agent also returns `EChartsOption` JSON per chart.– React `ChartCard` consumes options + slices data.– Add hook to refresh when dbt run (via Python script) completes.|Live dashboard on localhost after prompt with at least 3 chart types (bar, line, pie).|
|**W‑4**|**Hardening & Pilot Demo**|– Add dbt snapshot tests for slowly‑changing dims.– CLI `yudai backfill` for historical re‑runs (utilizing the Python orchestrator).– Polish UX, write README install guide.– Collect feedback from 10 PMs.|Tag `v0.1.0‑mvp`; demo video + zip for testers.|

---

## 2 · Product Requirements Document (MVP)

### 2.1 Problem Statement

PMs need reliable metrics fast, without sending data to the cloud. Yudai V2 should let them ingest a CSV, type a question, and receive a tested dashboard — **entirely offline**.

### 2.2 Success Metrics

|Metric|Target|
|---|---|
|Prompt→dashboard success rate|≥ 80 %|
|Cold install time|≤ 10 min|
|Local inference only|0 external calls|
|Pilot SUS score|≥ 75|

### 2.3 In Scope

- Solo‑Server LLM container
    
- Python-orchestrated dbt pipelines on DuckDB
    
- ECharts dashboards in React
    
- Single `/api/dashboards` JSON contract
    
- Data versioning via dbt snapshots
    

### 2.4 Out‑of‑Scope

- Spark / BigQuery / Streaming connectors
    
- Monte‑Carlo, Slack alerts, Spark executor
    
- Multi‑tenant auth
    

### 2.5 Key User Stories

1. **Upload & Ask** — PM uploads `sales.csv`, types “Show quarterly revenue & top‑5 products”. System builds dbt model + dashboard.
    
2. **Iterate** — PM edits prompt “Segment by region too”; only the transformed layer is rerun.
    
3. **Backfill** — PM runs `yudai backfill --id qtr_revenue --start 2022‑01‑01` to regenerate old metrics.
    

### 2.6 Functional Requirements

- **FR‑1**: `docker compose up` starts Solo‑Server, DuckDB, Next.js (Python orchestrator will be part of the backend logic or a simple script).
    
- **FR‑2**: Orchestrator agent writes dbt SQL + tests to `models/generated`.
    
- **FR‑3**: Python orchestrator script executes `dbt seed|run|test` and sets status.
    
- **FR‑4**: `/api/dashboards/:id` returns chart options & data.
    
- **FR‑5**: React dashboard renders ≤ 3 s for ≤ 500 k rows.
    

### 2.7 Non‑Functional

- Works on macOS ARM & Linux.
    
- All data stored in `~/yudai/data` with file hash directories.
    

### 2.8 Milestones

|Day|Milestone|
|---|---|
|**0**|Kick‑off & repo cleanup|
|**7**|Scaffold passes CI, ECharts demo up|
|**14**|Prompt→dbt pipeline green|
|**21**|API + dashboard live|
|**28**|MVP release & pilot demo|

### 2.9 Dependencies

- `echarts-for-react` (MIT) – see docs: [https://github.com/hustcc/echarts-for-react](https://github.com/hustcc/echarts-for-react)
    
- `dbt-core`, `dbt-duckdb`
    

---


    

_Updated May 23 2025 — Pranay K._