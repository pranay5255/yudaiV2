# Yudai v2&#x20;

> **Local, private & lightning‑fast analytics.** Drop your CSV ☞ chat with your data ☞ ship the deck before your next stand‑up.

---

## 🎯 Why Yudai v2?

Product & Growth Managers shouldn’t have to beg for SQL snippets or wait a sprint for a dashboard. Yudai v2 turns **plain‑English questions into interactive charts** right on your laptop—no cloud bill, no data leaks, no setup nightmares.

***TL;DR***\*: Clone → **`pnpm dev`** → upload → insight.\*

---

## 📚 Table of Contents

* [Key Features](#key-features)
* [Quick Start](#quick-start)
* [How It Works](#how-it-works)
* [Roadmap & Status](#roadmap--status)
* [Contributing](#contributing)
* [License](#license)
* [Go to Top](#TOP)

---

## Key Features

| Status | Feature                                                                     | For you, PM!                           |
| ------ | --------------------------------------------------------------------------- | -------------------------------------- |
| ✅      | **Chat‑first Analytics** — ask *“Which cohort retains best?”* & get a chart | Skip SQL; stay strategic               |
| ✅      | **Drag‑&‑Drop CSV Upload**                                                  | Zero config, zero friction             |
| ✅      | **Auto‑Generated Insights**                                                 | Instantly share hot‑takes in Slack     |
| ✅      | **Interactive Dashboard Layout**                                            | Rearrange, resize, export to PNG       |
| 🛠️    | **Prompt → Full Dashboard Code‑Gen**                                        | One‑click PR for an embeddable app     |
| 🛠️    | **TabPFN Auto‑ML Forecasts**                                                | Push‑button predictive power           |
| 🛠️    | **Real‑Time Data Connectors**                                               | Mixpanel, GA4, Amplitude, Snowflake    |
| 🛠️    | **Role‑Based Collaboration**                                                | Comment threads, @mentions, versioning |

> 🗒️ *Legend*: ✅ Implemented  |  🛠️ In‑progress  |  🚧 Planned

---

## Quick Start&#x20;

```bash
# 1 – Clone & install deps
$ git clone https://github.com/yourname/yudai-v2.git && cd yudai-v2
$ pnpm i                                  # Node deps
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r codegen/requirements.txt # Python agents

# 2 – Add your OpenRouter or OpenAI key
a$ cp .env.example .env && $EDITOR .env

# 3 – Run dev servers
$ pnpm dev     # http://localhost:3000
```

> **Time to first insight:** \~2 minutes on a fresh laptop. ⏱️💨

---

## How It Works&#x20;

1. **Upload** csv → saved to `codegen/uploads/`
2. **Python DatasetProfilerAgent** inspects schema & quality
3. **InsightGenAgent** crafts bullet‑point stories
4. **Orchestrator** streams chat replies back to Next.js via `api/conversation`
5. **React Dashboard** renders charts with Recharts + ShadCN UI

*All agent logic is LangChain‑free, so you can read the 200 loc orchestration with morning coffee.*

---

## Roadmap & Status&#x20;

### 🚀 Implemented

* Chat interface, drag‑&‑drop uploads
* Python EDA & insight agents (OpenRouter LLM)
* Recharts‑powered interactive dashboard

### 🚧 Not yet implemented

* **Code‑gen service** that spits out a standalone Next.js dashboard repo
* **Auto‑ML (TabPFN)** for time‑series forecasting
* **Streaming connectors**: Snowflake, GA4, Amplitude
* **RBAC & collaboration canvas**

### 🔭 Upcoming 🌟

| ETA     | Feature                                | Why you’ll care                             |
| ------- | -------------------------------------- | ------------------------------------------- |
| 2025‑06 | `/scratchpad → slide‑deck` auto‑export | Turn insights → exec‑ready PDF in one click |
| 2025‑07 | "Ask my metrics" NL‑SQL                | Talk to Mixpanel like you talk to me        |
| 2025‑08 | Slack daily KPI digest                 | Wake up to actionable deltas                |

*Star the repo to follow the journey & drop feedback in Issues—your vote steers the backlog!* \:rocket:

---

## Contributing&#x20;

Pull requests are welcome! Check `CONTRIBUTING.md` (WIP) for setup, coding standards, and the agent eval harness.

*

We ❤️ PRs that improve docs, UX copy, and onboarding scripts just as much as hardcore code.

---

## License&#x20;

MIT — because sharing multiplies impact.

---

[Go To TOP](#TOP)
