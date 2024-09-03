from gridlab.gldcore.TimeStamp import TimeStamp


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
class Locale:
    def __init__(self):
        self.stack = []

    def locale_push(self):
        pass

    def locale_pop(self):
        pass


def locale_push(stack=None):
    tz = TimeStamp.timestamp_current_timezone()
    locale = Locale()
    if locale is None:
        print("locale push failed; no memory")
        return
    else:
        locale.next = stack
        stack = locale
        if tz is None:
            print("locale TZ is empty")
            """
            TROUBLESHOOT
            This warning indicates that the TZ environment variable has not been set.  
            This variable is used to specify the default timezone to use while
            GridLAB-D is running.  Supported timezones are listed in the 
            <a href="http://gridlab-d.svn.sourceforge.net/viewvc/gridlab-d/trunk/core/tzinfo.txt?view=markup">tzinfo.txt</a>
            file.
            """
        locale.tz = tz if tz else ""

def locale_pop():
    global stack
    if stack is None:
        print("locale pop failed; stack empty")
        return
    else:
        next_locale = stack
        tz = "TZ=" + next_locale.tz
        stack = stack.next
        if TimeStamp.putenv(tz) != 0:
            print("locale pop failed")
            # TROUBLESHOOT: This is an internal error causes by a corrupt locale stack.
        else:
            TimeStamp.tzset()
        del next_locale