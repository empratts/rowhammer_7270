from pathlib import Path
import re
import json

output = open("stats.csv", 'w')

output.write("Raw RH Runs\n")
output.write(f'Rows,Hits,Seed,Flips,TRR Commands,Total Energy,Refresh Energy,TRR Energy,Write Energy,Read Energy,Activation Energy,Average Read Latency\n')
for p in Path("./outputs/").iterdir():
    m = re.match(r"rh_(\d{2})x(\d+)_(\d+)$",p.name)
    if m:
        seed = int(m.group(3))
        rows = int(m.group(1))
        hits = int(m.group(2))
        stats_file = open(p / 'dramsim3.json')
        stats = json.load(stats_file)['0']
        output.write(f'{rows},{hits},{seed},{stats["flips"]},{stats["num_trr_cmds"]},{stats["total_energy"]},{stats["ref_energy"]},{stats["trr_energy"]},{stats["write_energy"]},{stats["read_energy"]},{stats["act_energy"]},{stats["average_read_latency"]}\n')


output.write("\nRH Runs with TRR\n")
output.write(f'Rows,Hits,Seed,Flips,TRR Commands,Total Energy,Refresh Energy,TRR Energy,Write Energy,Read Energy,Activation Energy,Average Read Latency\n')
for p in Path("./outputs/").iterdir():
    m = re.match(r"rh_(\d{2})x(\d+)_(\d+)_trr$",p.name)
    if m:
        seed = int(m.group(3))
        rows = int(m.group(1))
        hits = int(m.group(2))
        stats_file = open(p / 'dramsim3.json')
        stats = json.load(stats_file)['0']
        output.write(f'{rows},{hits},{seed},{stats["flips"]},{stats["num_trr_cmds"]},{stats["total_energy"]},{stats["ref_energy"]},{stats["trr_energy"]},{stats["write_energy"]},{stats["read_energy"]},{stats["act_energy"]},{stats["average_read_latency"]}\n')


output.write("\nRH Runs with Increased Refresh Rate\n")
output.write(f'Rows,Hits,Seed,Refresh Multiplier,Flips,TRR Commands,Total Energy,Refresh Energy,TRR Energy,Write Energy,Read Energy,Activation Energy,Average Read Latency\n')
for p in Path("./outputs/").iterdir():
    m = re.match(r"rh_(\d{2})x(\d+)_(\d+)_(\d+)xtREFI$",p.name)
    if m:
        seed = int(m.group(3))
        rows = int(m.group(1))
        hits = int(m.group(2))
        refresh_multi = int(m.group(4))
        stats_file = open(p / 'dramsim3.json')
        stats = json.load(stats_file)['0']
        output.write(f'{rows},{hits},{seed},{refresh_multi},{stats["flips"]},{stats["num_trr_cmds"]},{stats["total_energy"]},{stats["ref_energy"]},{stats["trr_energy"]},{stats["write_energy"]},{stats["read_energy"]},{stats["act_energy"]},{stats["average_read_latency"]}\n')


output.write("\nRaw Workload Runs\n")
output.write(f'Seed,Flips,TRR Commands,Total Energy,Refresh Energy,TRR Energy,Write Energy,Read Energy,Activation Energy,Average Read Latency\n')
for p in Path("./outputs/").iterdir():
    m = re.match(r"wl_(\d+)$",p.name)
    if m:
        seed = int(m.group(1))
        stats_file = open(p / 'dramsim3.json')
        stats = json.load(stats_file)['0']
        output.write(f'{seed},{stats["flips"]},{stats["num_trr_cmds"]},{stats["total_energy"]},{stats["ref_energy"]},{stats["trr_energy"]},{stats["write_energy"]},{stats["read_energy"]},{stats["act_energy"]},{stats["average_read_latency"]}\n')


output.write("\nWorkload Runs with TRR\n")
output.write(f'Seed,Flips,TRR Commands,Total Energy,Refresh Energy,TRR Energy,Write Energy,Read Energy,Activation Energy,Average Read Latency\n')
for p in Path("./outputs/").iterdir():
    m = re.match(r"wl_(\d+)_trr$",p.name)
    if m:
        seed = int(m.group(1))
        stats_file = open(p / 'dramsim3.json')
        stats = json.load(stats_file)['0']
        output.write(f'{seed},{stats["flips"]},{stats["num_trr_cmds"]},{stats["total_energy"]},{stats["ref_energy"]},{stats["trr_energy"]},{stats["write_energy"]},{stats["read_energy"]},{stats["act_energy"]},{stats["average_read_latency"]}\n')


output.write("\nWorkload Runs with Increased Refresh Rate\n")
output.write(f'Seed,Refresh Multi,Flips,TRR Commands,Total Energy,Refresh Energy,TRR Energy,Write Energy,Read Energy,Activation Energy,Average Read Latency\n')
for p in Path("./outputs/").iterdir():
    m = re.match(r"wl_(\d+)_(\d+)xtREFI$$",p.name)
    if m:
        seed = int(m.group(1))
        refresh_multi = int(m.group(2))
        stats_file = open(p / 'dramsim3.json')
        stats = json.load(stats_file)['0']
        output.write(f'{seed},{refresh_multi},{stats["flips"]},{stats["num_trr_cmds"]},{stats["total_energy"]},{stats["ref_energy"]},{stats["trr_energy"]},{stats["write_energy"]},{stats["read_energy"]},{stats["act_energy"]},{stats["average_read_latency"]}\n')