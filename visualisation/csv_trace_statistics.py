import ipaddress

def packetCountPerInterval(dataframe, start, end, interval):
    local_start = start
    local_end = local_start + interval
    packet_count = []
    while local_end <= end:
        new_dataframe = dataframe[(dataframe["frame.time_relative"] >= local_start) & (dataframe["frame.time_relative"] < local_end)]
        packet_count.append(new_dataframe.shape[0])
        local_start = local_start + interval
        local_end = local_start + interval
    return packet_count


def histogramOfTargetSubnetFrequency(dataframe, resolution):
    factor = 2**32 / resolution
    histogram = [0] * resolution
    dataframe["ip.dst"] = dataframe["ip.dst"].apply(lambda x: int(int(ipaddress.IPv4Address(x.split(",")[0]))/factor) )

    for i in range(resolution):
        histogram[i] = len(dataframe[dataframe["ip.dst"]==i].index)
    return histogram

def histogramOfSourceSubnetFrequency(dataframe, resolution):
    factor = 2**32 / resolution
    histogram = [0] * resolution
    dataframe["ip.src"] = dataframe["ip.src"].apply(lambda x: int(int(ipaddress.IPv4Address(x.split(",")[0]))/factor) )
    for i in range(resolution):
        histogram[i] = len(dataframe[dataframe["ip.src"]==i].index)
    return histogram