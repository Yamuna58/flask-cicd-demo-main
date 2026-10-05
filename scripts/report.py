"""Daily health report from the Prometheus API -> CSV. Run: python scripts/report.py"""
import csv, datetime, requests
PROM = "http://localhost:9090/api/v1/query"

def q(expr):
    res = requests.get(PROM, params={"query": expr}, timeout=10).json()["data"]["result"]
    return {r["metric"].get("service", r["metric"].get("instance")): float(r["value"][1]) for r in res}

req = q("sum by (service) (rate(http_requests_total[5m]))")
err = q('sum by (service) (rate(http_requests_total{status="500"}[5m]))')
p95 = q("histogram_quantile(0.95, sum by (le, service) (rate(http_request_duration_seconds_bucket[5m])))")

fn = f"report_{datetime.date.today()}.csv"
with open(fn, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["service", "req_per_sec", "error_pct", "p95_latency_ms", "status"])
    for s in sorted(req):
        e = (err.get(s, 0) / req[s] * 100) if req[s] else 0
        lat = p95.get(s, 0) * 1000
        status = "ALERT" if e > 5 or lat > 500 else "OK"
        w.writerow([s, round(req[s], 2), round(e, 2), round(lat, 1), status])
print("Saved", fn)
