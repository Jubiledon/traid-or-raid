import csv
import os

logs_dir = "logs/runs"

for condition in os.listdir(logs_dir):
    condition_path = os.path.join(logs_dir, condition)
    if not os.path.isdir(condition_path):
        continue
    
    print(f"\n── {condition} ──")
    
    for fname in sorted(os.listdir(condition_path)):
        if not fname.endswith(".csv"):
            continue

        with open(os.path.join(condition_path, fname)) as f:
            rows = list(csv.DictReader(f))

        if not rows:
            continue

        raids = [r for r in rows if r.get("action_type") == "raid" 
                 and "stole" in r.get("result", "")]
        broadcasts = [r for r in rows if r.get("action_type") == "broadcast"
                     and r.get("message", "").strip()]
        
        scores = {}
        for r in rows:
            scores[r["agent_id"]] = int(r["inventory"])
        
        spread = max(scores.values()) - min(scores.values()) if scores else 0

        print(f"  {fname:45s} | raids={len(raids):3d} | "
              f"broadcasts={len(broadcasts):3d} | spread={spread:3d}")