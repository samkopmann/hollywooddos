def getTrainingDataFileName(resolution, window_size, scale):
    return "%s_resolution##%0.4f_size##%0.4f_scale" % (resolution,window_size,scale)