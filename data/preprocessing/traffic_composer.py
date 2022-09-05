import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ipaddress
import csv
import os
import json
from pathlib import Path

mawi_dir = "../datasets/mawi/"
caida_dir = "../datasets/ddos-2007/"

mawi_files = [0, 1, 2, 3, 4, 5]
caida_files = [-1, -1, 11, 12, 13, -1]

resolution_max = 32
factor = 2**32 / resolution_max

#sizes in seconds
sizes = [1]


dir = os.getcwd()
#intensity_scales = [1.0, 0.05, 0.04, 0.03, 0.02, 0.01]
intensity_scales = [1.0]

resolutions = [8]
#resolutions = [32, 16, 8, 4]

caida_factor_larger_than_mawi = 1.5516415989110433
#Shift for /7 subnets
caida_shift_x = 66
caida_shift_y = 4

for size in sizes:
    for res in resolutions:
        Path("../training/%s_resolution/%s_window_size/" % (res, size)).mkdir(parents=True, exist_ok=True)


def increment_pixel(aggregation_map, ip_src, ip_dst, resolution):
    x = int(ip_dst / (2**32 / resolution)) % resolution
    y = int(ip_src / (2**32 / resolution)) % resolution
    aggregation_map[y*resolution + x] = aggregation_map[y*resolution + x] + 1

for i in range(6):

    mawi_file = "mawi_background-%s.csv" % mawi_files[i]
    mawi = pd.read_csv(mawi_dir+mawi_file).dropna()


    mawi["ip.src"] = mawi["ip.src"].apply(lambda x: int(ipaddress.IPv4Address(x.split(",")[0])))
    mawi["ip.dst"] = mawi["ip.dst"].apply(lambda x: int(ipaddress.IPv4Address(x.split(",")[0])))
    
    caida = []
    if caida_files[i] != -1:
        file = "ddos-%d.csv" % caida_files[i]
        caida = pd.read_csv(caida_dir+file).dropna()
        caida["ip.src"] = caida["ip.src"].apply(lambda x: int(ipaddress.IPv4Address(x.split(",")[0])))
        caida["ip.dst"] = caida["ip.dst"].apply(lambda x: int(ipaddress.IPv4Address(x.split(",")[0])))

    for size in sizes:
        for window in range(int(149/size)):

            benign_images = {}
            attack_images = {}
            for resolution in resolutions:
                benign_images[resolution] = np.zeros(resolution**2)
                attack_images[resolution] = np.zeros(resolution**2)

            mawi_filtered = mawi[(mawi["frame.time_relative"] > (window*size)) & (mawi["frame.time_relative"] < ((window+1)*size))]
            for index, row in mawi_filtered.iterrows():
                for res in benign_images:
                    increment_pixel(benign_images[res], row["ip.src"], row["ip.dst"], res)

            if caida_files[i] != -1:
                caida_filtered = caida[(caida["frame.time_relative"] > (window*size)) & (caida["frame.time_relative"] < ((window+1)*size))]
                for index, row in caida_filtered.iterrows():
                    for res in attack_images:
                        increment_pixel(attack_images[res], row["ip.src"]+caida_shift_x, row["ip.dst"]+caida_shift_y, res)

            for scale in intensity_scales:
                for res in attack_images:
                    with open("../training/" + str(res) + "_resolution/" + str(size) + "_window_size/" + str(scale) + "_scale" + ".csv", "a") as csvfile:

                        writer = csv.writer(csvfile, delimiter=";")
                        attack_image_scaled = attack_images[res] * (scale/caida_factor_larger_than_mawi)
                        final_image = np.add(attack_image_scaled, benign_images[res])
                        
                        label = [1,0] if caida_files[i] != -1 else [0,1]
                        writer.writerow(list(final_image) + label)

                        csvfile.close()
