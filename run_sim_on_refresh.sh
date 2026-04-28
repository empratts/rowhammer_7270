seeds=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
refresh=(2 4 8 16)
hammers=(1 2 4)
hit_rate=50000
rows=(20 50)

for hc in "${hammers[@]}"; do
    for rf in "${refresh[@]}"; do
        for r in "${rows[@]}"; do
            hits=$((hc * hit_rate))
            echo "Starting Pass - Refresh: ${rf}, Hammers: ${hits}, Rows: ${r}"
            for sd in "${seeds[@]}"; do
                mkdir -p "./outputs/rh_${r}x${hits}_${sd}_${rf}xtREFI"
                ./build/dramsim3main ./configs/DDR4_8Gb_x8_3200_${rf}xREFI.ini --vuln 3.276816384e-6 --seed "${sd}" -t "./trace/rh_${r}x${hits}_${sd}_trace" -o "./outputs/rh_${r}x${hits}_${sd}_${rf}xtREFI" --threshold 25000 &
                
            done
            wait
        done
    done
done