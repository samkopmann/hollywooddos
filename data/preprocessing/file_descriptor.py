def getTrainingDataFileName(resolution, window_size, scale):
    return "%s_resolution##%s_size##%s_scale" % (str(resolution),str(window_size),str(scale))