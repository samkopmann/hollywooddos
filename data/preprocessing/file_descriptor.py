def getTrainingDataFileName(resolution, window_size, scale):
    return "./training/res-%s##win-%s##scale-%s.csv" % (str(resolution),str(window_size),str(scale))