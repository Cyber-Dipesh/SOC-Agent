import os
import requests
import whois
from dotenv import load_dotenv

load_dotenv()

VT_KEY = os.getenv("VT_API_KEY")
ABUSE_KEY = os.getenv("ABUSEIPDB_KEY")


def check_abuseipdb(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": ABUSE_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}
    r = requests.get(url, headers=headers, params=params, timeout=10)
    return r.json()


def check_virustotal(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": VT_KEY}
    r = requests.get(url, headers=headers, timeout=10)
    return r.json()


def check_whois(ip):
    try:
        return whois.whois(ip)
    except Exception as e:
        return {"error": str(e)}
