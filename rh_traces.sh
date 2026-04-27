seeds=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
hammers=(1 2 4)
hit_rate=50000
rows=20

for hc in "${hammers[@]}"; do
    for sd in "${seeds[@]}"; do
        hits=$((hc * hit_rate))
        trr_rows=$((rows * 3))
        time=$((hits * rows * 44 * 5))
        python3 ./make_trace.py -c configs/DDR4_8Gb_x8_3200.ini -s "$sd" -n ${hits} -t ${rows} -o "./trace/rh_${rows}x${hits}_${sd}_trace" &
    done
    wait
done