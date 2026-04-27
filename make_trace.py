import argparse
import configparser
import numpy as np

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', type=str, required=True, help="DRAM configuration file")
    parser.add_argument('-n', '--hammer_count', type=int, default=30000, help="Number of times to hammer each victim")
    parser.add_argument('-t', '--target_count', type=int, default=1, help="Number of rows to target")
    parser.add_argument('-o', '--output', type=str, default='./trace', help="Output file")
    parser.add_argument('-s', '--seed', type=int, default=0, help="Seed for the RNG. 0 = random (default)")
    
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    rows = int(config['dram_structure']['rows'])
    columns = int(config['dram_structure']['columns'])
    channels = int(config['system']['channels'])
    channel_size = int(config['system']['channel_size'])
    bankgroups = int(config['dram_structure']['bankgroups'])
    banks_per_group = int(config['dram_structure']['banks_per_group'])
    tRCD = int(config['timing']['tRCD'])        # minimum timing to open a row and access it
    tRP = int(config['timing']['tRP'])          # precharge time - time required to close a row
    hammer_spacing = tRCD + tRP                 # Minimum spacing of hammer strikes. Row must be opened, accessed, and closed
    tick_time_ns = float(config['timing']['tCK'])
    BL = int(config['dram_structure']['BL'])
    bus_width = int(config['system']['bus_width'])
    device_width = int(config['dram_structure']['device_width'])
    address_mapping = config['system']['address_mapping']

    banks = bankgroups * banks_per_group
    devices_per_rank = bus_width / device_width
    page_size = columns * device_width / 8  # page size in bytes
    megs_per_bank = page_size * (rows / 1024) / 1024
    megs_per_rank = megs_per_bank * banks * devices_per_rank

    ranks = channel_size / megs_per_rank

    request_size_bytes = bus_width / 8 * BL
    shift_bits = int(np.log2(request_size_bytes))
    col_low_bits = int(np.log2(BL))
    actual_col_bits = int(np.log2(columns)) - col_low_bits

    field_widths = {}
    field_widths["ch"] = int(np.log2(channels))
    field_widths["ra"] = int(np.log2(ranks))
    field_widths["bg"] = int(np.log2(bankgroups))
    field_widths["ba"] = int(np.log2(banks_per_group))
    field_widths["ro"] = int(np.log2(rows))
    field_widths["co"] = actual_col_bits

    fields = []
    field_pos = {}

    for i in range(len(address_mapping.strip())//2):
        fields.append(address_mapping[2*i:2*i+2])
    
    pos = 0
    while fields != []:
        token = fields.pop()
        field_pos[token] = pos
        pos += field_widths[token]
    
    ch_pos = field_pos["ch"]
    ra_pos = field_pos["ra"]
    bg_pos = field_pos["bg"]
    ba_pos = field_pos["ba"]
    ro_pos = field_pos["ro"]
    co_pos = field_pos["co"]

    ch_mask = (1 << field_widths["ch"]) - 1
    ra_mask = (1 << field_widths["ra"]) - 1
    bg_mask = (1 << field_widths["bg"]) - 1
    ba_mask = (1 << field_widths["ba"]) - 1
    ro_mask = (1 << field_widths["ro"]) - 1
    co_mask = (1 << field_widths["co"]) - 1

    if args.seed != 0:
        rng = np.random.default_rng(args.seed)
    else:
        rng = np.random.default_rng()

    if args.target_count > rows // 8:
        tc = rows // 8
    else:
        tc = args.target_count

    victim_rows = rng.choice(rows // 8, size=tc, replace=False)
    print(f"Generating trace hitting {tc} rows {args.hammer_count} times each.")
    victim_columns = rng.integers(low=0, high=columns >> col_low_bits, size=args.hammer_count)
    clock = 0

    outfile = open(args.output, 'w')

    # For simplicity, the attack will target channel, rank, bg, and bank 0, only the row
    # and column will change 
    for r in victim_rows:
        for c in victim_columns:
            rt = r * 8 + 4  #this is to prevent target rows from being adjacent
            address = ((rt - 1) << (ro_pos + shift_bits)) | (c << (co_pos + shift_bits))
            command = f'0x{address:08x} READ {clock}\n'
            outfile.write(command)

            address = ((rt + 1) << (ro_pos + shift_bits)) | (c << (co_pos + shift_bits))
            command = f'0x{address:08x} READ {clock + 1}\n'
            outfile.write(command)
            clock += hammer_spacing * 3



if __name__ == "__main__":
    main()