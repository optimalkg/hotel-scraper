from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from config_manager import DEFAULT_CONFIG, load_config, save_config
from scraper import run_analysis

app = Flask(__name__)


@app.get("/")
def index():
    config = load_config()
    return render_template("index.html", config=config)


@app.get("/api/config")
def get_config():
    return jsonify(load_config())


@app.post("/api/config")
def update_config():
    payload = request.get_json(silent=True) or {}
    hotels = payload.get("hotels", [])
    dates = payload.get("dates", {})

    normalized_hotels = []
    for hotel in hotels:
        name = str(hotel.get("name", "")).strip()
        url = str(hotel.get("url", "")).strip()
        if name and url:
            normalized_hotels.append({"name": name, "url": url})

    config = {
        "hotels": normalized_hotels or DEFAULT_CONFIG["hotels"],
        "dates": {
            "check_in": dates.get("check_in") or DEFAULT_CONFIG["dates"]["check_in"],
            "check_out": dates.get("check_out") or DEFAULT_CONFIG["dates"]["check_out"],
        },
    }
    save_config(config)
    return jsonify({"status": "ok", "config": config})


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    config = payload if payload else load_config()
    save_config(config)
    summary = run_analysis(config)
    return jsonify({"status": "ok", "summary": summary})


if __name__ == "__main__":
    app.run(debug=True)
