import random, time, requests
TARGETS = ["http://orders:8000", "http://payments:8000", "http://inventory:8000"]
time.sleep(10)
while True:
    try:
        requests.get(random.choice(TARGETS) + "/work", timeout=3)
    except Exception:
        pass
    time.sleep(random.uniform(0.02, 0.15))
