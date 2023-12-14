
def timestamp_current_timezone():
    return current_tzname

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def local_tzoffset(timestamp):
    use_ts_cache = False

    if use_ts_cache:
        old_t = 0
        old_tzoffset = 0
        if old_t == 0 or old_t != timestamp:
            old_tzoffset = tzoffset + isdst(timestamp) * 3600 if isdst(timestamp) else 0
            old_t = timestamp
        return old_tzoffset
    else:
        return int(tzoffset + (isdst(timestamp) * 3600 if isdst(timestamp) else 0))
