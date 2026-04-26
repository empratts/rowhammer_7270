seeds=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
hammers=(1 2 4)
hit_rate=50000
rows=50

for hc in "${hammers[@]}"; do
    for sd in "${seeds[@]}"; do
        hits=$((hc * hit_rate))
        trr_rows=$((rows * 3))
        time=$((hits * rows * 44 * 5))
        mkdir -p "./outputs/rh_${rows}x${hits}_${sd}"
        ./build/dramsim3main ./configs/DDR4_8Gb_x8_3200.ini --vuln 1.638408e-6 --seed "${sd}" -c ${time} -t "./trace/rh_${rows}x${hits}_${sd}_trace" -o "./outputs/rh_${rows}x${hits}_${sd}" --threshold 25000
        # Run again with TRR on
        mkdir -p "./outputs/rh_${rows}x${hits}_${sd}_trr"
        ./build/dramsim3main ./configs/DDR4_8Gb_x8_3200.ini --vuln 1.638408e-6 --seed "${sd}" -c ${time} -t "./trace/rh_${rows}x${hits}_${sd}_trace" -o "./outputs/rh_${rows}x${hits}_${sd}_trr" --threshold 25000 --trr ${trr_rows} --ratio 0.25
    done
    wait
done