from datetime import datetime
from math import sqrt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ipaddress
import csv
import os
import json
from pathlib import Path
import skimage.measure


mawi_dir = "../datasets/mawi/"
caida_dir = "../datasets/ddos-2007/"

mawi_files = [0, 1, 2, 3, 4, 5]
caida_files = [-1, -1, 11, 12, 13, -1]

caida_factor_larger_than_mawi = 1.5516415989110433

shift_attack_sources = 4* (2**25)
shift_attack_destinations = 66* (2**25)

def reduce_map_array(array):
    counter_values = array[:-1]
    resolution = int(sqrt(len(counter_values)))
    aggregation_map = counter_values.reshape((resolution, resolution))
    aggregation_map = skimage.measure.block_reduce(aggregation_map, (2,2), np.sum)
    aggregation_map = aggregation_map.reshape(int(resolution*resolution/4))
    new_array = np.concatenate((aggregation_map, [array[-1]]))
    return new_array

dir = os.getcwd()

def increment_pixel(images, resolution, row, ip_src, ip_dst, is_attack):
    x = int(ip_dst) % resolution
    y = int(ip_src) % resolution
    images[row][y*resolution + x] = images[row][y*resolution + x] + 1
    if is_attack:
        images[row][-1] = 1

def compose_dataset(size, resolutions, intensity_scales):
    resolution = max(resolutions)
    benign_images = np.zeros((int(len(mawi_files)*150/size), (resolution**2 + 1)))
    attack_images = np.zeros((int(len(mawi_files)*150/size), (resolution**2 + 1)))

    for i in range(len(mawi_files)):
        print("Progress %d/%d" % (i, len(mawi_files)))
        mawi_file = "mawi_background-%s.csv" % mawi_files[i]
        mawi = pd.read_csv(mawi_dir+mawi_file).dropna()


        mawi["ip.src"] = mawi["ip.src"].apply(lambda x: int( int(ipaddress.IPv4Address(  x.split(",")[0]  )) / (2**32 / resolution))   )
        mawi["ip.dst"] = mawi["ip.dst"].apply(lambda x: int( int(ipaddress.IPv4Address(  x.split(",")[0]  )) / (2**32 / resolution))   )
        mawi["frame.time_relative"] = mawi["frame.time_relative"].apply(lambda x: int(x/size) + int(i * (150/size)))
        
        caida = []
        if caida_files[i] != -1:
            file = "ddos-%d.csv" % caida_files[i]
            caida = pd.read_csv(caida_dir+file).dropna()
            caida["ip.src"] = caida["ip.src"].apply(lambda x: int( ((int(ipaddress.IPv4Address(  x.split(",")[0]  )) + shift_attack_sources)%(2**32)) / (2**32 / resolution))   )
            caida["ip.dst"] = caida["ip.dst"].apply(lambda x: int( ((int(ipaddress.IPv4Address(  x.split(",")[0]  )) + shift_attack_destinations)%(2**32)) / (2**32 / resolution))   )
            caida["frame.time_relative"] = caida["frame.time_relative"].apply(lambda x: int(x/size) + int(i * (150/size)))

        for index, row in mawi.iterrows():
            increment_pixel(benign_images, resolution, row["frame.time_relative"], row["ip.src"], row["ip.dst"], False)

        if caida_files[i] != -1:
            for index, row in caida.iterrows():
                increment_pixel(attack_images, resolution, row["frame.time_relative"], row["ip.src"], row["ip.dst"], True)

    while resolution > 2:
        if resolution in resolutions:
            for scale in intensity_scales:
                print("Start - %0.4f size # resolution %s # scale %0.4f   %s" % (size, resolution, scale, datetime.now().strftime("%Y%m%d-%H:%M")))
                scaled_attack = np.copy(attack_images)
                scaled_attack[:,:-1] = scaled_attack[:, :-1]*(scale/caida_factor_larger_than_mawi)
                composed_maps = np.add(benign_images, scaled_attack)
                dataframe = pd.DataFrame(composed_maps)
                dataframe.to_pickle("../training/%d_resolution##%0.4f_size##%0.4f_scale.pkl" % (resolution, size, scale))
                print("Done")
        resolution = resolution / 2
        benign_images = np.apply_along_axis(reduce_map_array, 1, benign_images)
        attack_images = np.apply_along_axis(reduce_map_array, 1, attack_images)

for size in [1, 0.1, 0.01, 0.001]:
    resolutions = [32, 16, 8, 4]
    scales = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.001]
    print("Creating dataset - %s size - %s res - %s scales" % (size, resolutions, scales))
    compose_dataset(size, resolutions, scales)

