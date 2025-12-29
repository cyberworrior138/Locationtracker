#!/usr/bin/env python3
# ==================================================
# F-VIRUS LOCATION TRACKER
# Tool coded by Mr. Virus - Tanzania 🇹🇿
# IG: @uknown_virus404x
# Consent-based location tracking demo
# ==================================================

from flask import Flask, render_template, request, jsonify
import json, os, uuid, datetime

app = Flask(__name__)
DATA_FILE = "data/logs.json"

# Ensure data folder/file exists
if not os.path.exists("data"):
    os.mkdir("data")
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Load logs
def load_logs():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save logs
def save_logs(logs):
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f, indent=4)

# Generate device id
def get_device_id(ip, ua):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, ip + ua))

# Admin dashboard
@app.route("/")
def admin():
    logs = load_logs()
    return render_template("admin.html", logs=logs)

# Consent page
@app.route("/track")
def track():
    return render_template("consent.html")

# Receive user data
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    if not data: return jsonify({"status":"error"}), 400
    ip = request.remote_addr
    ua = data.get("user_agent", "")
    device_id = get_device_id(ip, ua)
    entry = {
        "time": str(datetime.datetime.now()),
        "ip": ip,
        "device": ua,
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "battery": data.get("battery"),
        "device_id": device_id
    }
    logs = load_logs()
    logs.append(entry)
    save_logs(logs)
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    PORT = 5000  # Badilisha port kama inashindikana
    print(f"""
===========================================
F-VIRUS LOCATION TRACKER (CONSENT DEMO)
Tool coded by Mr. Virus - Tanzania 🇹🇿
IG: @uknown_virus404x
Admin Dashboard : http://127.0.0.1:{PORT}
Consent Link    : http://127.0.0.1:{PORT}/track
===========================================
""")
    app.run(host="0.0.0.0", port=PORT, threaded=True)



