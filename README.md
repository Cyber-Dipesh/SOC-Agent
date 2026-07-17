DEMO:
                                                               **CLI usage:**
<img width="1918" height="938" alt="Debian 12 x 64-bit-2026-07-17-13-39-56" src="https://github.com/user-attachments/assets/31490183-5bac-4c9c-b434-5b9d594d5c3a" />
                                                           **Web UI (Streamlit):**
<img width="907" height="662" alt="Screenshot 2026-07-17 233328" src="https://github.com/user-attachments/assets/5600c1f3-bba4-4e09-b287-8c6dcb6a18bf" />


# SOC Agent (ARIA AI) — AI-Assisted SOC Triage Agent

ARIA AI is a lightweight junior SOC analyst agent that takes a suspicious IP address, enriches it against multiple threat-intel sources, and uses a **local, offline LLM (via Ollama)** to generate a structured triage report — verdict, confidence, evidence, and recommended playbook actions.

Built as a hands-on project to demonstrate SOC automation and AI-assisted alert triage, two of the highest-leverage skills a fresher analyst can show on a resume.

## Why this project

L1 SOC analysts spend a large share of their day manually pivoting between AbuseIPDB, VirusTotal, and WHOIS to decide whether an alert is worth escalating. ARIA AI automates that first pass: it pulls the enrichment data itself and asks a local LLM to reason over it in a consistent, repeatable format — the same way a human analyst would, but in seconds.

Because it runs on a local Ollama model instead of a paid API, the whole pipeline is free to run and doesn't send data to a third-party LLM provider.

## Architecture
<img width="1440" height="1280" alt="image" src="https://github.com/user-attachments/assets/04f40f18-358e-4f2e-ac6f-a06c61abead3" />


## Features

- **Multi-source enrichment** — AbuseIPDB reputation score, VirusTotal detections, WHOIS org/country, gathered in parallel
- **Local LLM reasoning** — runs entirely on-device via [Ollama](https://ollama.com), no per-request API cost, no data leaves your machine
- **Structured triage output** — every report follows the same 5-part format: verdict, confidence, summary, evidence, recommended next steps
- **CLI and web UI** — run one-off lookups from the command line (`main.py`) or use the Streamlit app for live demos
- **Resilient by design** — each enrichment call is wrapped so a single API failure (rate limit, timeout) doesn't crash the run
- **IP validation and live progress feedback** in the Streamlit UI, plus a downloadable `.txt` report

## Tech stack

| Layer | Tool |
|---|---|
| Enrichment | AbuseIPDB API, VirusTotal API, python-whois |
| Reasoning | Ollama (local LLM — llama3.1:8b / qwen2.5-coder / phi3) |
| UI | Streamlit |
| Language | Python 3 |

## Project structure

```
aria-ai/
├── main.py          # CLI entry point — orchestrates enrichment + triage
├── triage.py         # builds the prompt and calls the local Ollama model
├── enrich.py         # AbuseIPDB / VirusTotal / WHOIS lookup functions
├── app.py            # Streamlit web UI
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com) installed and running locally

### 2. Clone and install

```bash
git clone https://github.com/Cyber-Dipesh/SOC-Agent.git
cd SOC-Agent.git
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Pull a local model

```bash
ollama pull llama3.1:8b
# lower-RAM machines:
ollama pull phi3
```

### 4. Add your API keys

Copy `.env.example` to `.env` and fill in your own free-tier keys:

```bash
cp .env.example .env
```

- [AbuseIPDB](https://www.abuseipdb.com) — free API key, no card required
- [VirusTotal](https://www.virustotal.com) — free API key, no card required

### 5. Run it

CLI:
```bash
python main.py --ip 45.33.32.156
```

Web UI:
```bash
streamlit run app.py
```

## Sample output

```
=== TRIAGE REPORT ===
1. Verdict: Malicious
2. Confidence: High
3. Summary: Source IP has a high AbuseIPDB reputation score with
   multiple recent abuse reports, consistent with brute-force login activity.
4. Evidence: AbuseIPDB score 100/100 with 25 reports in the last 90 days;
   VirusTotal flags the IP as malicious across multiple vendors.
5. Recommended next steps: Block the source IP at the firewall,
   review authentication logs for the targeted account, and escalate
   to Tier 2 if repeated attempts are observed.
```


## Disclaimer

This is a learning/portfolio project. It is not a production security tool — always validate AI-generated verdicts against your own analysis before taking action on a real alert.

## License

MIT — see [LICENSE](LICENSE).
