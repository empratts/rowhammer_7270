seeds=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
hammers=(1 2 4)
N_thresh=50000
rows=100

for sd in "${seeds[@]}"; do
    for hc in "${hammers[@]}"; do
        hits=$((hc * N_thresh))
        trr_rows=$((rows * 3))
        time=$((hits * rows * 44))
        python3 ./make_trace.py -c configs/DDR4_8Gb_x8_3200.ini -s "$sd" -n ${hits} -t ${rows} -o "./trace/rh_${rows}x${hits}_${sd}_trace"
        mkdir -p "./outputs/rh_${rows}x${hits}_${sd}"
        ./build/dramsim3main ./configs/DDR4_8Gb_x8_3200.ini --vuln 1.638408e-6 --seed "${sd}" -c 30000000 -t "./trace/rh_${rows}x${hits}_${sd}_trace" -o "./outputs/rh_${rows}x${hits}_${sd}" --threshold 25000
        # Run again with TRR on
        mkdir -p "./outputs/rh_${rows}x${hits}_${sd}_trr"
        ./build/dramsim3main ./configs/DDR4_8Gb_x8_3200.ini --vuln 1.638408e-6 --seed "${sd}" -c 30000000 -t "./trace/rh_${rows}x${hits}_${sd}_trace" -o "./outputs/rh_${rows}x${hits}_${sd}_trr" --threshold 25000 --trr ${trr_rows} --ratio 0.25
        rm -f "./trace/rh_${rows}x${hits}_${sd}_trace"
    done
done