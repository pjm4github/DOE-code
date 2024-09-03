import gridlabd

def init(fntable, module, argc, argv):
    if gridlabd.set_callback(fntable) is None:
        errno = gridlabd.EINVAL
        return None

    g_assert = gridlabd.GAssert(module)
    double_assert = gridlabd.DoubleAssert(module)
    complex_assert = gridlabd.ComplexAssert(module)
    enum_assert = gridlabd.EnumAssert(module)
    int_assert = gridlabd.IntAssert(module)

    # Always return the first class registered
    return g_assert.owner_class

def do_kill(ptr):
    # If global memory needs to be released, this is a good time to do it
    return 0

def check():
    # If any assert objects have bad filenames, they'll fail on init()
    return 0
