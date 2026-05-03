import matplotlib.pyplot as plt
import numpy as np

rh_50k = [0.05, 0.05, 0.3, 0.1, 0.15, 0.1, 0.1, 0.2, 0.3, 0.15, 0.14, 0.08, 0.18, 0.18, 0.18, 0.1, 0.1, 0.2, 0.24, 0.2]
rh_100k = [0.7, 0.45, 0.8, 0.95, 0.65, 0.5, 0.5, 0.7, 0.95, 0.8, 0.62, 0.44, 0.64, 0.82, 0.62, 0.52, 0.6, 0.66, 0.84, 0.8]
rh_200k = [1.35, 1.2, 1.55, 1.6, 1.4, 1.2, 1.45, 1.55, 1.6, 1.8, 1.6, 1.28, 1.44, 1.46, 1.36, 1.32, 1.5, 1.36, 1.42, 1.66]

rh_hits = [50000, 100000, 200000]
rh_points = [np.mean(rh_50k)*100, np.mean(rh_100k)*100, np.mean(rh_200k)*100]
rh_errors = [np.std(rh_50k)*100/np.sqrt(len(rh_50k)), np.std(rh_100k)*100/np.sqrt(len(rh_100k)), np.std(rh_200k)*100/np.sqrt(len(rh_200k))]


fig, ax = plt.subplots()             # Create a figure containing a single Axes.
fig.suptitle("Raw Rowhammer Traces")
ax.errorbar(rh_hits, rh_points, yerr=rh_errors, fmt='o', capsize=5)
ax.set_xlabel("Hammers")
ax.set_xscale('log')
ax.set_ylabel("Percentage of target rows flipped")


# rh_50k_2x = [0.05, 0.05, 0.3, 0.1, 0.15, 0.1, 0.1, 0.2, 0.3, 0.15, 0.14, 0.06, 0.18, 0.18, 0.16, 0.1, 0.08, 0.2, 0.22, 0.2]
# rh_100k_2x = [0.6, 0.25, 0.7, 0.7, 0.65, 0.5, 0.65, 0.7, 0.8, 0.8, 0.66, 0.34, 0.68, 0.72, 0.6, 0.56, 0.52, 0.68, 0.72, 0.84]
# rh_200k_2x = [1.15, 1.05, 1.55, 1.6, 1.4, 1.2, 1.4, 1.5, 1.65, 1.45, 1.48, 1.22, 1.3, 1.54, 1.4, 1.18, 1.24, 1.42, 1.58, 1.46]

# rh_points = [np.mean(rh_50k_2x)*100, np.mean(rh_100k_2x)*100, np.mean(rh_200k_2x)*100]
# rh_errors = [np.std(rh_50k_2x)*100/np.sqrt(len(rh_50k_2x)), np.std(rh_100k_2x)*100/np.sqrt(len(rh_100k_2x)), np.std(rh_200k_2x)*100/np.sqrt(len(rh_200k_2x))]


# fig, ax = plt.subplots()             # Create a figure containing a single Axes.
# fig.suptitle("2x Refresh Rowhammer Traces")
# ax.errorbar(rh_hits, rh_points, yerr=rh_errors, fmt='o', capsize=5)
# ax.set_xlabel("Hammers")
# ax.set_xscale('log')
# ax.set_ylabel("Percentage of target rows flipped")


rh_50k_16x = [0, 0, 0.2, 0.05, 0.1, 0.05, 0.1, 0.05, 0.1, 0.05, 0.04, 0, 0.12, 0.1, 0.1, 0.04, 0.06, 0.06, 0.12, 0.1]
rh_100k_16x = [0.1, 0.05, 0.3, 0.3, 0.25, 0.15, 0.15, 0.2, 0.4, 0.4, 0.22, 0.04, 0.22, 0.32, 0.22, 0.18, 0.1, 0.2, 0.4, 0.34]
rh_200k_16x = [0.6, 0.15, 0.45, 0.75, 0.6, 0.3, 0.3, 0.6, 0.9, 0.7, 0.64, 0.4, 0.38, 0.68, 0.58, 0.38, 0.34, 0.52, 0.68, 0.64]

rh_points_16x = [np.mean(rh_50k_16x)*100, np.mean(rh_100k_16x)*100, np.mean(rh_200k_16x)*100]
rh_errors_16x = [np.std(rh_50k_16x)*100/np.sqrt(len(rh_50k_16x)), np.std(rh_100k_16x)*100/np.sqrt(len(rh_100k_16x)), np.std(rh_200k_16x)*100/np.sqrt(len(rh_200k_16x))]


fig, ax = plt.subplots()
fig.suptitle("Raw vs. 16x Refresh Rowhammer Traces")
ax.errorbar(rh_hits, rh_points, yerr=rh_errors, fmt='bo', capsize=5)
ax.errorbar(rh_hits, rh_points_16x, yerr=rh_errors_16x, fmt='ro', capsize=5)
ax.set_xlabel("Hammers")
ax.set_xscale('log')
ax.set_ylabel("Percentage of target rows flipped")


wl_total_energy = [312797101430.4, 312886000051.2, 312676416355.2, 312790860470.4, 312696448521.6, 313163074454.4, 312926769772.8, 312947143555.2, 312839353286.4, 312874973760]
wl_total_energy_2x = [347274320870.4, 347204351155.2, 347153587699.2, 347363793110.4, 347296505817.6, 347410869206.4, 347103594892.8, 347245727971.2, 347277070262.4, 347254354080, ]
wl_total_energy_4x = [436048086134.4, 436046378371.2, 436034455843.2, 436027538774.4, 436058587593.6, 436061636054.4, 436007572204.8, 436023677011.2, 435999041750.4, 435991851168, ]
wl_total_energy_8x = [631255149446.4, 631249262755.2, 631242562051.2, 631260195398.4, 631250777817.6, 631282602662.4, 631237363420.8, 631242393955.2, 631259671094.4, 631245951360, ]
wl_total_energy_16x = [1035139707398.4, 1035138031123.2, 1035128415235.2, 1035140536310.4, 1035141706089.6, 1035146055926.4, 1035139513948.8, 1035138259459.2, 1035139178150.4, 1035137561904]

wl_energy_points = [np.mean(wl_total_energy), np.mean(wl_total_energy_2x), np.mean(wl_total_energy_4x), np.mean(wl_total_energy_8x), np.mean(wl_total_energy_16x)]
wl_energy_errors = [np.std(wl_total_energy)/np.sqrt(len(wl_total_energy)),
                    np.std(wl_total_energy_2x)/np.sqrt(len(wl_total_energy_2x)),
                    np.std(wl_total_energy_4x)/np.sqrt(len(wl_total_energy_4x)),
                    np.std(wl_total_energy_8x)/np.sqrt(len(wl_total_energy_8x)),
                    np.std(wl_total_energy_16x)/np.sqrt(len(wl_total_energy_16x))]


fig, ax = plt.subplots()
fig.suptitle("Workload Energy Increase with Refresh Rate")
ax.errorbar([1,2,4,8,16], wl_energy_points, yerr=wl_energy_errors, fmt='bo', capsize=5),
ax.set_xlabel("Refresh Multiplier")
ax.set_ylabel("Energy Consumption (pJ)")


wl_read_latency = [65.0571061093248, 65.3761042307968, 65.6286815817007, 65.4404465791806, 65.4205977313638, 65.4338436537804, 65.285190489831, 65.2416679784205, 65.5379472275116, 65.3038083379846, ]
wl_read_latency_2x = [80.6159056806002, 81.0985467821605, 81.7810614421051, 81.473010835692, 81.5045858453099, 81.5257868628122, 80.33351475222, 81.0148824430103, 80.7474623104786, 81.3881470668212, ]
wl_read_latency_4x = [111.9081100393, 111.648994201446, 111.95052527482, 112.033564914086, 112.568187662505, 112.181049720607, 112.104525923804, 111.666847927191, 111.319426747033, 111.85818556524, ]
wl_read_latency_8x = [155.262979635584, 155.654907294724, 156.339744600347, 156.069731537868, 155.954684419555, 157.034724598016, 156.1351475222, 155.861493109715, 155.8940111959, 156.187840796874, ]
wl_read_latency_16x = [256.181822079314, 256.637883885747, 254.945595000932, 255.039368728021, 255.642818366239, 254.991019500513, 256.287969063306, 256.761966772084, 255.612367030796, 254.240049804646, ]

wl_energy_points = [np.mean(wl_read_latency), np.mean(wl_read_latency_2x), np.mean(wl_read_latency_4x), np.mean(wl_read_latency_8x), np.mean(wl_read_latency_16x)]
wl_energy_errors = [np.std(wl_read_latency)/np.sqrt(len(wl_read_latency)),
                    np.std(wl_read_latency_2x)/np.sqrt(len(wl_read_latency_2x)),
                    np.std(wl_read_latency_4x)/np.sqrt(len(wl_read_latency_4x)),
                    np.std(wl_read_latency_8x)/np.sqrt(len(wl_read_latency_8x)),
                    np.std(wl_read_latency_16x)/np.sqrt(len(wl_read_latency_16x))]


fig, ax = plt.subplots()
fig.suptitle("Workload Read Latency with Refresh Rate")
ax.errorbar([1,2,4,8,16], wl_energy_points, yerr=wl_energy_errors, fmt='bo', capsize=5),
ax.set_xlabel("Refresh Multiplier")
ax.set_ylabel("Average Read Latency (cycles)")


plt.show()

