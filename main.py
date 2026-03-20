from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests, os

app = Flask(__name__, static_folder='static')
CORS(app)

BASE  = "https://paper-api.alpaca.markets"
DATA  = "https://data.alpaca.markets"

def hdrs(req):
    return {
        "APCA-API-KEY-ID":     req.headers.get("X-API-Key", ""),
        "APCA-API-SECRET-KEY": req.headers.get("X-API-Secret", ""),
        "Content-Type": "application/json",
        "accept":       "application/json",
    }

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/account")
def account():
    r = requests.get(f"{BASE}/v2/account", headers=hdrs(request))
    return jsonify(r.json()), r.status_code

@app.route("/api/positions")
def positions():
    r = requests.get(f"{BASE}/v2/positions", headers=hdrs(request))
    return jsonify(r.json()), r.status_code

@app.route("/api/positions/<sym>", methods=["DELETE"])
def close_pos(sym):
    r = requests.delete(f"{BASE}/v2/positions/{sym}", headers=hdrs(request))
    return (jsonify(r.json()), r.status_code) if r.content else ("", 204)

@app.route("/api/positions", methods=["DELETE"])
def close_all():
    r = requests.delete(f"{BASE}/v2/positions", headers=hdrs(request))
    return (jsonify(r.json()), r.status_code) if r.content else ("", 204)

@app.route("/api/orders", methods=["GET"])
def get_orders():
    r = requests.get(f"{BASE}/v2/orders", headers=hdrs(request), params=request.args)
    return jsonify(r.json()), r.status_code

@app.route("/api/orders", methods=["POST"])
def place_order():
    r = requests.post(f"{BASE}/v2/orders", headers=hdrs(request), json=request.get_json())
    return jsonify(r.json()), r.status_code

@app.route("/api/orders/<oid>", methods=["DELETE"])
def cancel_order(oid):
    r = requests.delete(f"{BASE}/v2/orders/{oid}", headers=hdrs(request))
    return ("", 204) if r.status_code == 204 else (jsonify(r.json()), r.status_code)

@app.route("/api/snapshot/<sym>")
def snapshot(sym):
    r = requests.get(f"{DATA}/v2/stocks/{sym}/snapshot", headers=hdrs(request))
    return jsonify(r.json()), r.status_code

@app.route("/api/bars/<sym>")
def bars(sym):
    r = requests.get(f"{DATA}/v2/stocks/{sym}/bars", headers=hdrs(request), params=request.args)
    return jsonify(r.json()), r.status_code

@app.route("/api/latest/<sym>")
def latest(sym):
    r = requests.get(f"{DATA}/v2/stocks/{sym}/quotes/latest", headers=hdrs(request))
    return jsonify(r.json()), r.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
