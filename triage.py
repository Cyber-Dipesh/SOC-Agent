import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder"  # swap for llama3.1:8b or phi3 depending on your hardware


def generate_triage_report(alert, enrichment_data):
    prompt = f"""
You are a Junior SOC Analyst. Analyze this alert and enrichment data,
then produce a triage report with these exact sections:
1. Verdict (Malicious / Suspicious / Benign / Needs Investigation)
2. Confidence (Low/Medium/High)
3. Summary of what happened
4. Evidence supporting the verdict
5. Recommended next steps (playbook actions)

Alert:
{json.dumps(alert, indent=2)}

Enrichment Data:
{json.dumps(enrichment_data, indent=2)}
"""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300  # local models can be slow on larger prompts
    )
    return response.json()["response"]
