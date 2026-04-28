seeds=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
hammers=(1 2 4)
hit_rate=50000
rows=50
time=300000000
trr_rows=150

for sd in "${seeds[@]}"; do
    mkdir -p "./outputs/wl_${sd}"
    ./build/dramsim3main ./configs/DDR4_8Gb_x8_3200.ini --vuln 3.276816384e-6 --seed "${sd}" -c ${time} -t "./trace/wl_${sd}_trace" -o "./outputs/wl_${sd}" --threshold 25000 &
    # Run again with TRR on
    mkdir -p "./outputs/wl_${sd}_trr"
    ./build/dramsim3main ./configs/DDR4_8Gb_x8_3200.ini --vuln 3.276816384e-6 --seed "${sd}" -c ${time} -t "./trace/wl_${sd}_trace" -o "./outputs/wl_${sd}_trr" --threshold 25000 --trr ${trr_rows} --ratio 0.25 &
done

wait