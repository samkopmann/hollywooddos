def getTrainingDataFileName(resolution, window_size, scale):
    return "./training/res-%s##win-%s##scale-%s.npz" % (str(resolution),str(window_size),str(scale))