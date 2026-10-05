# SRE Observability Project
3 Python microservices + Redis, monitored with Prometheus & Grafana, with alert rules,
Python reporting/log-cleanup automation, and GitHub Actions CI.

## Run
    docker compose up --build -d
- Prometheus: http://localhost:9090  (Status > Targets, Alerts)
- Grafana:    http://localhost:3000  (admin / admin)
- Services:   http://localhost:8001/work , 8002 , 8003

## Automation
    pip install requests
    python scripts/report.py
    python scripts/log_cleanup.py logs 7
