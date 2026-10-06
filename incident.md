\# Incident Report — Payments Service Outage



\## Incident Summary



A failure-injection test was performed against the payments microservice to verify that Prometheus could detect service unavailability.



The payments Docker container was intentionally stopped while the orders and inventory services remained running.



\## Impact



The payments service became unavailable.



Orders and inventory remained healthy.



\## Detection



Prometheus detected that the payments target was DOWN.



Prometheus targets showed:



\- orders: UP

\- payments: DOWN

\- inventory: UP



The payments metrics endpoint was:



`http://payments:8000/metrics/`



Prometheus reported a DNS/service-resolution error because the payments container had been stopped.



\## Failure Injection



The payments container was stopped using:



```powershell

docker stop sre-observability-payments-1

