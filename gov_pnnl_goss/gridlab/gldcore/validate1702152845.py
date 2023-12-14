

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
class Counters:
    def __init__(self):
        self._lock = 0
        self.n_scanned = 0
        self.n_tested = 0
        self.n_passed = 0
        self.n_files = 0
        self.n_success = 0
        self.n_failed = 0
        self.n_exceptions = 0
        self.n_access = 0

    def __add__(self, a):
        self.wlock()
        self.n_scanned += a.get_scanned()
        self.n_tested += a.get_tested()
        self.n_passed += a.get_passed()
        self.n_files += a.get_nfiles()
        self.n_success += a.get_nsuccess()
        self.n_failed += a.get_nfailed()
        self.n_exceptions += a.get_nexceptions()
        self.wunlock()
        return self

    def __iadd__(self, a):
        self._lock = a._lock
        self.n_scanned += a.get_scanned()
        self.n_tested += a.get_tested()
        self.n_passed += a.get_passed()
        self.n_files += a.get_nfiles()
        self.n_success += a.get_nsuccess()
        self.n_failed += a.get_nfailed()
        self.n_exceptions += a.get_nexceptions()
        return self

    def get_scanned(self):
        return self.n_scanned

    def get_tested(self):
        return self.n_tested

    def get_passed(self):
        return self.n_passed

    def inc_scanned(self):
        self.wlock()
        self.n_scanned += 1
        self.wunlock()

    def inc_tested(self):
        self.wlock()
        self.n_tested += 1
        self.wunlock()

    def inc_passed(self):
        self.wlock()
        self.n_passed += 1
        self.wunlock()

    def get_nfiles(self):
        return self.n_files

    def get_nsuccess(self):
        return self.n_success

    def get_nfailed(self):
        return self.n_failed

    def get_nexceptions(self):
        return self.n_exceptions

    def inc_files(self, name):
        pass

    def inc_access(self, name):
        pass

    def inc_success(self, name, code, t):
        pass

    def inc_failed(self, name, code, t):
        pass

    def inc_exceptions(self, name, code, t):
        pass

    def print(self):
        pass

    def get_nerrors(self):
        pass

    def wlock(self):
        pass

    def wunlock(self):
        pass

    def rlock(self):
        pass

    def runlock(self):
        pass

class FinalCounters(Counters):
    pass

final = FinalCounters()
clean = False
report_fp = None
report_file = "validate.txt"
report_ext = None
report_col = "    "
report_eol = "\n"
report_eot = "\f"
report_cols = 0
report_rows = 0
report_lock = 0

def report_open():
    pass

def report_title(fmt, *args):
    pass

def report_data(fmt="", *args):
    pass

def report_newrow():
    pass

def report_newtable(table):
    pass

def report_close():
    pass

class Dirent:
    pass

class DIR:
    pass

def GetLastErrorMsg():
    pass

def opendir(dirname):
    pass

def Getvalidate_cmdargs():
    validate_cmdargs = [1024]
    return validate_cmdargs

def vsystem(fmt, *args):
    pass

def destroy_dir(name):
    return True

def copyfile(from, to):
    pass

def run_test(file, elapsed_time=None):
    counters = FinalCounters()
    return counters

class DirStack:
    pass

dirstack = None
next_id = 0
result_code = None
dirlock = 0

def pushdir(dir):
    pass

def sortlist():
    pass

def popdir():
    pass

def run_test_proc(arg):
    pass

def process_dir(path, runglms=False):
    pass

def encode_result(data, sz):
    pass

def validate(*args):
    pass


def get_scanned():
    return n_scanned

def get_tested():
    return n_tested

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def get_passed():
    return n_passed


Here's the Python equivalent of the provided C++ function using snake_case function names:

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def inc_scanned():
    wlock()
    global n_scanned
    n_scanned += 1
    wunlock()


Here's the equivalent python function using snake_case:

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def inc_tested():
    wlock()
    global n_tested
    n_tested += 1
    wunlock()


def inc_passed():
    wlock()
    n_passed += 1
    wunlock()

def w_lock():
    wlock(_lock)

def wunlock():
    wunlock(_lock)

def rlock():
    _rlock(_lock)

def runlock():
    runlock(_lock)

def get_n_files():
    return n_files

def get_nsuccess():
    return n_success

def get_nfailed():
    return n_failed

def get_n_exceptions():
    return n_exceptions

def get_naccess():
    return n_access

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def inc_files(name):
    global global_debug_mode
    global global_verbose_mode
    if global_debug_mode or global_verbose_mode:
        output_debug("processing %s" % name)
    else:
        len_ = 0
        blank = bytearray(1024)
        len_ = min(len_, 1023)
        blank[:len_] = b' ' * len_
        blank[len_] = 0
        output_raw("\r%s\rProcessing %s..." % (blank.decode('utf-8'), name))
        len_ = len(output_raw("", blank.decode('utf-8'), name)) - len_
    wlock() 
    n_files += 1
    wunlock() 


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def inc_access(name):
    output_debug(f"{name} folder access failure")
    wlock()
    n_access += 1
    wunlock()


Here's the converted python function using snake_case function names:

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def inc_success(name, code, t):
    output_error(f"{name} success unexpected, code {code} in {t:.1f} seconds")
    wlock()
    n_success += 1
    wunlock()


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def inc_failed(name, code, t):
    output_error("{} error unexpected, code {} ({}) in {:.1f} seconds".format(name, code, exec_getexitcodestr(code), t)
    wlock()
    global n_failed
    n_failed += 1
    wunlock()


Here's the Python version of the given CPP function using snake_case function names:

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def inc_exceptions(name, code, t):
    output_error(f"{name} exception unexpected, code {code} ({exec_getexitcodestr(code)}) in {t:.1f} seconds")
    wlock()
    global n_exceptions
    n_exceptions += 1
    wunlock()


def print_validation_report():
    rlock()
    n_ok = n_files - n_success - n_failed - n_exceptions
    output_message("\nValidation report:")
    if n_access:
        output_message("%d directory access failures" % n_access)
    output_message("%d models tested" % n_files)
    if n_files != 0:
        if n_success:
            output_message("%d unexpected successes" % n_success)
        if n_failed:
            output_message("%d unexpected errors" % n_failed)
        if n_exceptions:
            output_message("%d unexpected exceptions" % n_exceptions)
        output_message("%d tests succeeded" % n_ok)
        output_message("%.0f%% success rate" % (100.0 * n_ok / n_files))
    runlock()

def get_n_errors():
    return n_success + n_failed + n_exceptions + n_access

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import ctypes

def report_title(fmt, *args):
    len_ = 0
    if report_fp:
        wlock(report_lock)
        if report_cols > 0:
            len_ = fprintf(report_fp, "%s" % report_eol)
        args_ptr = (ctypes.c_char_p * len(args))(*args)
        len_ += vfprintf(report_fp, fmt, args_ptr)
        fflush(report_fp)
        wunlock(report_lock)
    return len_


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import ctypes

def report_data(fmt="", *args):
    len = 0
    if report_fp:
        wlock(report_lock)
        if report_cols > 0:
            len = ctypes.cdll.msvcrt.fprintf(report_fp, ctypes.c_char_p(report_col.encode('utf-8')))
        va_list_ptr = (ctypes.c_char_p * len)(*args)
        len += ctypes.cdll.msvcrt.vfprintf(report_fp, fmt.encode('utf-8'), va_list_ptr)
        wunlock(report_lock)
    return len


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def report_new_row():
    len = 0
    if report_fp:
        wlock(report_lock)
        report_cols = 0
        report_rows += 1
        len = report_fp.write(report_eol)
        report_fp.flush()
        wunlock(report_lock)
    return len


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def report_newtable(table):
    len = 0
    if report_fp:
        wlock(report_lock)
        report_rows += 1
        if report_cols > 0:
            len += fprintf(report_fp, "%s" % report_eol)
        report_cols = 0
        len = fprintf(report_fp, "%s%s%s" % (report_eot, table, report_eol))
        fflush(report_fp)
        wunlock(report_lock)
    return len


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def report_close():
    wlock(report_lock)
    if report_fp:
        report_fp.close()
    report_fp = None
    wunlock(report_lock)
    return report_rows


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import ctypes
import threading

def get_last_error_msg():
    lock = threading.Lock()
    lock.acquire()
    
    szBuf = ctypes.create_unicode_buffer(256)
    lpMsgBuf = ctypes.c_void_p
    dw = ctypes.windll.kernel32.GetLastError()
    
    ctypes.windll.kernel32.FormatMessageW(
        0x00000100 | 0x00000200,
        None,
        dw,
        0x0000,
        ctypes.byref(lpMsgBuf),
        0,
        None
    )

    lpMsgBuf_str = ctypes.wstring_at(lpMsgBuf)
    lpMsgBuf_str = lpMsgBuf_str.replace('\n', ' ').replace('\r', ' ')
    szBuf.value = f'{lpMsgBuf_str} (error code {dw})'
    
    ctypes.windll.kernel32.LocalFree(lpMsgBuf)
    lock.release()
    return szBuf.value


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import ctypes
import ctypes.util

def vsystem(fmt, *args):
    libc = ctypes.CDLL(ctypes.util.find_library('c'))
    vsprintf = libc.vsprintf
    vsprintf.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
    vsprintf.restype = ctypes.c_int
    vsnprintf = libc.vsnprintf
    vsnprintf.argtypes = (ctypes.c_char_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_ulong)
 
    command = ctypes.create_string_buffer(1024)
    vsprintf(command, fmt, args)
    output_debug('calling system(\'%s\')' % command.value)
    rc = libc.system(command)
    output_debug('system(\'%s\') returns code %x' % (command.value, rc))
    return rc


def push_dir(dir):
    output_debug("adding %s to process stack" % dir)
    item = DIRLIST()
    item.name = dir[:sizeof(item.name)-1]
    wlock(dirlock)
    item.next = dirstack
    item.id = next_id
    dirstack = item
    wunlock(dirlock)

def pop_dir():
    r_lock(dir_lock)
    item = dir_stack
    if dir_stack:
        dir_stack = dir_stack.next
    r_unlock(dir_lock)
    output_debug("pulling %s from process stack" % item.name)
    return item

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import ctypes

def encode_result(data, sz):
    len = (sz+1)//2+1
    code = ctypes.create_string_buffer(len)
    for i in range(sz):
        ndx = i//2
        shft = (i%2)*2
        code[ndx] |= (data[i]<<shft).to_bytes(1, byteorder='big')
    t = "0123456789ABCDEF"
    code = bytes([t[c] for c in code.raw])
    return code.decode('utf-8')


Here's the equivalent Python function using snake_case function names:

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import os
import time
from datetime import datetime
from math import fmin
import threading

def validate_cmd_args(*args):
    validate_cmd_args = ""
    redirect_found = False
    for arg in args:
        if arg == "--redirect":
            redirect_found = True
        validate_cmd_args += arg + " "
    if not redirect_found:
        validate_cmd_args += " --redirect all"
    return validate_cmd_args

def validate(argc, argv):
    validate_cmdargs = validate_cmd_args(*argv)
    global_suppress_repeat_messages = 0
    print(f"Starting validation test in directory '{global_workdir}'")
    var = os.getenv("clean")
    clean = bool(var) if var and int(var) != 0 else False
    report_file = "report.txt"
    report_fp = open(report_file, "w")
    try:
        report_fp.write("VALIDATION TEST REPORT\n")
        report_fp.write(f"GridLAB-D {global_version_major}.{global_version_minor}.{global_version_patch}-{global_version_build} ({global_version_branch})\n")
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S %z')
        report_fp.write(f"Date: {timestamp}\n")
        user = os.getenv("USERNAME") if os.name == 'nt' else os.getenv("USER")
        report_fp.write(f"User: {user if user else '(NA)'}\n")
        host = os.getenv("COMPUTERNAME") if os.name == 'nt' else os.getenv("HOSTNAME")
        report_fp.write(f"Host: {host if host else '(NA)'}\n")
        report_fp.write(f"Platform: {sizeof(void) * 8}-bit {global_platform} {'DEBUG' if _DEBUG else 'RELEASE'}\n")
        report_fp.write(f"Workdir: {global_workdir}\n")
        report_fp.write(f"Arguments: {validate_cmdargs}\n")
        report_fp.write(f"Clean: {'TRUE' if clean else 'FALSE'}\n")
        report_fp.write(f"Threads: {global_threadcount}\n")
        options = global_getvar("validate")
        report_fp.write(f"Options: {options if options else '(NA)'}\n")
        mailto = global_getvar("mailto")
        report_fp.write(f"Mailto: {mailto if mailto else '(NA)'}\n")
        if VO_RPTDIR & global_validateoptions:
            report_fp.write("DIRECTORY SCAN RESULTS\n")
            process_dir(global_workdir)
            sortlist()
        if VO_RPTGLM & global_validateoptions:
            report_fp.write("FILE TEST RESULTS\n")
        n_procs = global_threadcount or len(os.sched_getaffinity(0))
        n_procs = fmin(final.get_tested(), n_procs)
        pid = []
        for i in range(n_procs):
            pid.append(threading.Thread(target=run_test_proc, args=(i,)))
            pid[i].start()
        for i in range(n_procs):
            pid[i].join()
        final.print()
        dt = exec_clock() / global_ms_per_second
        report_fp.write(f"Total validation elapsed time: {dt} seconds\n")
        if final.get_nerrors() == 0:
            exec_setexitcode(XC_SUCCESS)
        else:
            exec_setexitcode(XC_TSTERR)
        report_fp.write("OVERALL RESULTS\n")
        report_fp.write("Directory results\n")
        report_fp.write(f"Scanned: {final.get_scanned()}\n")
        report_fp.write(f"Denied: {final.get_naccess()}\n")
        report_fp.write(f"Tested: {final.get_tested()}\n")
        n_failed = final.get_tested() - final.get_passed()
        report_fp.write(f"Failed: {n_failed}\n")
        report_fp.write("File results\n")
        report_fp.write(f"Tested: {final.get_nfiles()}\n")
        report_fp.write(f"Passed: {final.get_nfiles() - final.get_nerrors()}\n")
        report_fp.write(f"Failed: {final.get_nerrors()}\n")
        report_fp.write("Unexpected results\n")
        report_fp.write(f"Successes: {final.get_nsuccess()}\n")
        report_fp.write(f"Errors: {final.get_nfailed()}\n")
        report_fp.write(f"Exceptions: {final.get_nexceptions()}\n")
        report_fp.write(f"Runtime: {dt} s\n")
        result_code = encode_result(result_code, next_id)
        report_fp.write(f"Result code: {result_code}\n")
    finally:
        report_fp.write("END TEST REPORT\n")
        report_fp.close()

    if mailto and mailto != "":
        if os.name != 'nt':
            if os.uname().sysname == 'Darwin':
                MAILER = "/usr/bin/mail"
            else:
                MAILER = "/bin/mail"
            if os.system(f"{MAILER} -s 'GridLAB-D Validation Report ({final.get_nerrors()} errors)' {mailto} < {report_file}") == 0:
                print(f"Mail message sent to {mailto}")
            else:
                print(f"Error sending notification to {mailto}")

    exit(XC_SUCCESS if final.get_nerrors() == 0 else XC_TSTERR)
