"""Quick self-test: python test_app.py"""
import os
import app as scalepilot

client = scalepilot.app.test_client()

def check(name, cpu, mem, req, expect):
    r = client.post("/", data={"cpu": cpu, "memory": mem, "requests": req})
    ok = r.status_code == 200 and expect in r.get_data(as_text=True)
    print(("PASS" if ok else "FAIL"), "-", name)
    return ok

results = [
    check("High load -> scale up", 80, 60, 600, "Scale up"),
    check("High memory -> scale up", 40, 90, 200, "Scale up"),
    check("Low load -> scale down", 10, 20, 50, "Scale down"),
    check("Normal load -> no change", 45, 50, 250, "No change needed"),
]
bad = client.post("/", data={"cpu": 150, "memory": 10, "requests": 10})
print("PASS" if bad.status_code == 400 else "FAIL", "- Invalid input rejected")
results.append(bad.status_code == 400)
print("\nALL TESTS PASSED" if all(results) else "\nSOME TESTS FAILED")
