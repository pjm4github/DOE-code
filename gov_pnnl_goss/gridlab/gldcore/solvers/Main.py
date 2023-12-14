# Copyright (C) 2012 Battelle Memorial Institute
# DP Chassin

# Assuming gridlabd.py contains definitions for EXPORT, CALLBACKS, and callback
from GridLabD import EXPORT, CALLBACKS, callback

# Define the do_kill function
@EXPORT
def do_kill(data):
    return 0

# Define the init_solvers function
@EXPORT
def init_solvers(fntable):
    global callback  # Assuming callback is a global variable
    callback = fntable
    return 1
