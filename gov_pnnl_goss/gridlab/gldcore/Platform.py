import math
import sys

# Equivalent of int64
def to_int64(value):
    return int(value)

# Equivalent of atoi64
def atoi64(s):
    return int(s)

# Case-insensitive string comparisons
def stricmp(s1, s2):
    return s1.lower() == s2.lower()

def strnicmp(s1, s2, n):
    return s1.lower()[:n] == s2.lower()[:n]

# Tokenizing strings
def strtok_s(string, delimiters):
    return string.split(delimiters)

# Not-a-Number (NaN)
QNAN = math.nan

# Check if the platform is 64-bit
X64 = sys.maxsize > 2**32
NATIVE = 'int64' if X64 else 'int32'

