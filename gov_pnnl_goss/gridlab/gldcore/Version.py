# Version information

# Versions of notice
# 2.0:1:1135
# 2.1:2:2157
# 2.2:1:3063
# 2.3:0:4233
# 3.0:0:3356
# 3.1:0:5355
# 3.2:0:5400

# Define constants
BRANCH = "Navajo"  # Update this from legal.h each time trunk is branched
BUILDNUM = 0
REV_YEAR = 2023  # You should set the appropriate year here

def version_copyright():
    return f"Copyright (C) 2004-{REV_YEAR}\nBattelle Memorial Institute\nAll Rights Reserved"

def version_major():
    return 3  # Replace with the actual major version number

def version_minor():
    return 0  # Replace with the actual minor version number

def version_patch():
    return 1  # Replace with the actual patch version number

def version_build():
    return BUILDNUM

def version_branch():
    return BRANCH


class Version:
    REV_MAJOR = version_major()
    REV_MINOR = version_minor()
    REV_PATCH = version_patch()

