import re
import streamlit as st
from enrich import check_abuseipdb, check_virustotal, check_whois
from triage import generate_triage_report


def safe_call(func, ip):
    try:
        return func(ip)
    except Exception as e:
        return {"error": str(e)}


def is_valid_ip(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return bool(pattern.match(ip))


st.title("🔍 ARIA AI — SOC Triage")

ip = st.text_input("Enter IP address to analyze")

if st.button("Analyze"):
    if not is_valid_ip(ip):
        st.error("❌ Invalid IP address format. Please enter a valid IPv4 address.")
    else:
        progress = st.progress(0)

        st.info("📡 Sending to WHOIS…")
        whois_data = safe_call(check_whois, ip)
        progress.progress(25)

        st.info("🛡️ Checking AbuseIPDB…")
        abuse = safe_call(check_abuseipdb, ip)
        progress.progress(50)

        st.info("🔬 Querying VirusTotal…")
        vt = safe_call(check_virustotal, ip)
        progress.progress(75)

        st.info("🤖 AI analyzing…")
        enrichment = {
            "abuseipdb": {
                "score": abuse.get("score"),
                "reports": abuse.get("reports")
            },
            "virustotal": {
                "malicious": vt.get("malicious"),
                "suspicious": vt.get("suspicious")
            },
            "whois": {
                "org": whois_data.get("org"),
                "country": whois_data.get("country")
            }
        }

        alert = {
            "alert_id": "alert-001",
            "src_ip": ip,
            "type": "Suspicious Activity",
            "username": "unknown"
        }

        report = generate_triage_report(alert, enrichment)
        progress.progress(100)

        st.success("✅ Analysis complete!")
        st.subheader("Triage Report")
        st.text(report)

        st.download_button(
            label="⬇️ Download Report",
            data=report,
            file_name=f"report_{alert['alert_id']}.txt",
            mime="text/plain"
        )
