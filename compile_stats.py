from pathlib import Path
import re
import json

output = open("stats.csv", 'w')

for p in Path("./outputs/").iterdir():
    m = re.match(r"rh_(\d{2})x(\d+)_(\d+)$", p.name)
    if m:
        seed = int(m.group(3))
        rows = int(m.group(1))
        hits = int(m.group(2))
        stats_file = open(p / 'dramsim3.json')
        stats = json.load(stats_file)['0']
        print(f'{rows}, {hits}, {seed}, {stats["total_energy"]}, {stats["ref_energy"]}, {stats["write_energy"]}, {stats["read_energy"]}, {stats["act_energy"]}, {stats["average_read_latency"]}')
