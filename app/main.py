import os, time, random, json, logging
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, make_asgi_app
import redis

SERVICE = os.getenv("SERVICE_NAME", "demo")
ERROR_RATE = float(os.getenv("ERROR_RATE", "0.05"))   # 5% of requests fail
MAX_DELAY = float(os.getenv("MAX_DELAY", "0.3"))      # random latency up to 300ms

# JSON logging (easy to ship to ELK/Loki later)
class JsonFmt(logging.Formatter):
    def format(self, r):
        return json.dumps({"ts": self.formatTime(r), "service": SERVICE,
                           "level": r.levelname, "msg": r.getMessage()})
h = logging.StreamHandler(); h.setFormatter(JsonFmt())
log = logging.getLogger(SERVICE); log.addHandler(h); log.setLevel(logging.INFO)

REQS = Counter("http_requests_total", "Total requests", ["service", "endpoint", "status"])
LAT = Histogram("http_request_duration_seconds", "Latency", ["service", "endpoint"])

app = FastAPI()
app.mount("/metrics", make_asgi_app())
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, socket_connect_timeout=1)

@app.get("/health")
def health():
    return {"service": SERVICE, "status": "ok"}

@app.get("/work")
def work():
    start = time.time()
    try:
        time.sleep(random.uniform(0, MAX_DELAY))
        r.incr(f"{SERVICE}:hits")                      # touch Redis
        if random.random() < ERROR_RATE:
            raise HTTPException(500, "simulated failure")
        REQS.labels(SERVICE, "/work", "200").inc()
        log.info("work ok")
        return {"service": SERVICE, "result": "done"}
    except HTTPException:
        REQS.labels(SERVICE, "/work", "500").inc()
        log.error("work failed")
        raise
    except Exception as e:
        REQS.labels(SERVICE, "/work", "500").inc()
        log.error(f"redis/other error: {e}")
        raise HTTPException(500, "dependency error")
    finally:
        LAT.labels(SERVICE, "/work").observe(time.time() - start)
