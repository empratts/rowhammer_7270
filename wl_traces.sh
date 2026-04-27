seeds=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")

for sd in "${seeds[@]}"; do
    hits=$((hc * hit_rate))
    trr_rows=$((rows * 3))
    time=$((hits * rows * 44 * 5))
    python3 ./workload_trace.py -n 1000000 -c configs/DDR4_8Gb_x8_3200.ini -s "$sd" -o "./trace/wl_${sd}_trace" &
done
wait