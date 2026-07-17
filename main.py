import argparse
from enrich import check_abuseipdb, check_virustotal, check_whois
from triage import generate_triage_report


def safe_call(func, ip):
    try:
        return func(ip)
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="ARIA AI — SOC triage tool")
    parser.add_argument("--ip", help="IP address to analyze", required=True)
    args = parser.parse_args()

    alert = {
        "alert_id": "alert-001",
        "src_ip": args.ip,
        "type": "Suspicious Activity",
        "username": "unknown"
    }

    enrichment = {
        "abuseipdb": safe_call(check_abuseipdb, args.ip),
        "virustotal": safe_call(check_virustotal, args.ip),
        "whois": safe_call(check_whois, args.ip)
    }

    report = generate_triage_report(alert, enrichment)
    print("\n=== TRIAGE REPORT ===\n")
    print(report)

    with open(f"report_{alert['alert_id']}.txt", "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()
