#!/usr/bin/env python3
"""
10-Day Metrics Tracker — Daily tracking loop
Day 5-10: signups, scans/actions, ARPC, discount rate, NRR
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

METRICS_DIR = Path(__file__).parent

def load_metrics(day: int) -> dict:
    """Load metrics for a specific day."""
    path = METRICS_DIR / f"day{day}.json"
    if path.exists():
        return json.loads(path.read_text())
    return None

def save_metrics(day: int, data: dict):
    """Save metrics for a specific day."""
    path = METRICS_DIR / f"day{day}.json"
    path.write_text(json.dumps(data, indent=2))

def get_current_day() -> int:
    """Get current day number (1-10)."""
    day1 = datetime(2026, 10, 7)
    today = datetime.now()
    delta = (today - day1).days + 1
    return min(max(delta, 1), 10)

def track_daily(day: int, signups: int = 0, scans: int = 0, arpc: float = 0, discount_rate: float = 0, nrr: float = 0):
    """Track daily metrics."""
    data = load_metrics(day) or {
        "day": day,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "metrics": {},
        "actions": {},
        "stars": {}
    }
    data["metrics"] = {
        "signups": signups,
        "scans_actions": scans,
        "arpc": arpc,
        "discount_rate": f"{discount_rate}%",
        "nrr": f"{nrr}%"
    }
    save_metrics(day, data)
    return data

def generate_report() -> dict:
    """Generate 10-day cumulative report."""
    report = {
        "period": "Day 1-10",
        "start_date": "2026-10-07",
        "end_date": "2026-10-16",
        "daily": [],
        "cumulative": {
            "total_signups": 0,
            "total_scans": 0,
            "avg_arpc": 0,
            "avg_discount_rate": 0,
            "avg_nrr": 0
        },
        "targets": {
            "day3_discount_rate": "< 3%",
            "day3_nrr": "> 90%",
            "day5_arpc": "> $280",
            "day7_revenue": "> $1,000",
            "day10_revaluation": "final report"
        }
    }
    
    for day in range(1, 11):
        data = load_metrics(day)
        if data:
            report["daily"].append(data)
            m = data.get("metrics", {})
            report["cumulative"]["total_signups"] += m.get("signups", 0)
            report["cumulative"]["total_scans"] += m.get("scans_actions", 0)
    
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        report = generate_report()
        print(json.dumps(report, indent=2))
    else:
        day = get_current_day()
        print(f"Current day: {day}")
        print(f"Metrics dir: {METRICS_DIR}")
        print(f"Files: {list(METRICS_DIR.glob('day*.json'))}")
