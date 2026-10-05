"""Archive log files older than N days. Run: python scripts/log_cleanup.py logs 7"""
import os, sys, time, gzip, shutil
folder, days = sys.argv[1], int(sys.argv[2])
cutoff = time.time() - days * 86400
for name in os.listdir(folder):
    p = os.path.join(folder, name)
    if os.path.isfile(p) and not name.endswith(".gz") and os.path.getmtime(p) < cutoff:
        with open(p, "rb") as src, gzip.open(p + ".gz", "wb") as dst:
            shutil.copyfileobj(src, dst)
        os.remove(p)
        print("Archived", name)
