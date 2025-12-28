from flask import Flask, render_template, request, jsonify
import json, os, time, hashlib

app = Flask(__name__)

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "logs.json")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_logs():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_log(entry):
    logs = load_logs()
    logs.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def make_device_id(ip, ua):
    return hashlib.sha256(f"{ip}|{ua}".encode()).hexdigest()[:16]

@app.route("/")
def admin():
    return render_template("admin.html")

@app.route("/track")
def consent():
    return render_template("consent.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json or {}
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "Unknown")

    entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "device": ua,
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "battery": data.get("battery"),
        "device_id": make_device_id(ip, ua)
    }
    save_log(entry)
    return jsonify({"status": "ok"})

@app.route("/api/logs")
def api_logs():
    return jsonify(load_logs())

if __name__ == "__main__":
    print(r"""
===========================================
   ______ _   _ _   _ _____ ____  
  |  ____| \ | | \ | |_   _/ __ \ 
  | |__  |  \| |  \| | | || |  | |
  |  __| | . ` | . ` | | || |  | |
  | |____| |\  | |\  |_| || |__| |
  |______|_| \_|_| \_|_____\____/ 

   F-VIRUS LOCATION TRACKER (CONSENT DEMO)
   Tool coded by Tanzanian hacker Mr.virus
   From Tanzania 🇹🇿
   Any problem visit my IG profile:
   @uknown_virus4040x
===========================================
Admin Dashboard : http://127.0.0.1:5000
Consent Link    : http://127.0.0.1:5000/track
""")
    app.run(host="0.0.0.0", port=5000)

