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


dir = os.getcwd()

size = 1
intensity_scale = 1.0
resolution = 8

images = np.zeros((int(900/size), (resolution**2 + 2)))

def increment_pixel(row, ip_src, ip_dst):
    x = int(ip_dst) % resolution
    y = int(ip_src) % resolution
    images[row][y*resolution + x] = images[row][y*resolution + x] + 1

for i in range(6):
    print("Progress %d/5" % i)
    mawi_file = "mawi_background-%s.csv" % mawi_files[i]
    mawi = pd.read_csv(mawi_dir+mawi_file).dropna()


    mawi["ip.src"] = mawi["ip.src"].apply(lambda x: int( int(ipaddress.IPv4Address(  x.split(",")[0]  )) / (2**32 / resolution))   )
    mawi["ip.dst"] = mawi["ip.dst"].apply(lambda x: int( int(ipaddress.IPv4Address(  x.split(",")[0]  )) / (2**32 / resolution))   )
    mawi["frame.time_relative"] = mawi["frame.time_relative"].apply(lambda x: int(x/size) + int(i * (150/size)))
    
    caida = []
    if caida_files[i] != -1:
        file = "ddos-%d.csv" % caida_files[i]
        caida = pd.read_csv(caida_dir+file).dropna()
        caida["ip.src"] = caida["ip.src"].apply(lambda x: int( int(ipaddress.IPv4Address(  x.split(",")[0]  )) / (2**32 / resolution))   )
        caida["ip.dst"] = caida["ip.dst"].apply(lambda x: int( int(ipaddress.IPv4Address(  x.split(",")[0]  )) / (2**32 / resolution))   )
        caida["frame.time_relative"] = caida["frame.time_relative"].apply(lambda x: int(x/size) + int(i * (150/size)))

    for index, row in mawi.iterrows():
        increment_pixel(row["frame.time_relative"], row["ip.src"], row["ip.dst"])

    if caida_files[i] != -1:
        for index, row in caida.iterrows():
            increment_pixel(row["frame.time_relative"], row["ip.src"], row["ip.dst"])

dataframe = pd.DataFrame(images)
dataframe.to_pickle("../training/%d_resolution##%d_size##%d_scale.pkl" % (resolution, size, intensity_scale))
dataframe.to_csv("../training/%d_resolution##%d_size##%d_scale.csv" % (resolution, size, intensity_scale))
