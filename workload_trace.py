import argparse
import configparser
import numpy as np

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', type=str, required=True, help="DRAM configuration file")
    parser.add_argument('-n', '--access_count', type=int, default=100000, help="Number of times to access memory")
    parser.add_argument('-r', '--row_count', type=int, default=3000, help="Number of rows to spread accesses across")
    parser.add_argument('-d', '--duration', type=int, default=1000000000, help="Duration of the trace (in ticks)")
    parser.add_argument('-a', '--zipf_alpha', type=float, default=0.9, help="Zipfian distribution skew parameter")
    parser.add_argument('-o', '--output', type=str, default='./trace', help="Output file")
    
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
    shift_bits = np.log2(request_size_bytes)
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


    rng = np.random.default_rng()

    weights = np.array([1.0 / (i ** args.zipf_alpha) for i in range(1, args.row_count + 1)])
    weights /= weights.sum()
    access_rows = rng.choice(args.row_count, size=args.access_count, p=weights)
    clock = 0

    access_spacing = args.duration / args.access_count

    outfile = open(args.output, 'w')

    # For simplicity, the accesses will target channel, rank, bg, and bank 0, only the row
    # and column will change 
    for r in access_rows:
        c = int(rng.random() * (columns >> col_low_bits))
        address = (r << ro_pos) | (c << co_pos)
        access_type = "READ"
        if (rng.random() > 0.7):
            access_type = "WRITE"

        command = f'0x{address:08x} {access_type} {int(clock)}\n'
        outfile.write(command)

        clock += access_spacing



if __name__ == "__main__":
    main()