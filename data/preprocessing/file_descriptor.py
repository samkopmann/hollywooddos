def getTrainingDataFileName(resolution, window_size, scale):
    return "%s_resolution##%s_size##%s_scale.csv" % (str(resolution),str(window_size),str(scale))