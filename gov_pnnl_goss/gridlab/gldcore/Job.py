import subprocess
from gov_pnnl_goss.gridlab.gldcore.Output import output_debug, output_error, output_raw
from enum import Enum


class JOBOPTIONS(Enum):
    JO_NONE = 0x0000
    JO_SORTA = 0x0001
    JO_SORTN = 0x0002
    JO_SUBDIR = 0x0004
    JO_CLEAN = 0x0008
    JO_DEFAULT = JO_SORTA


class JobManager:
    clean = False
    def __init__(self):
        pass

    @staticmethod
    def get_last_error_msg():
        pass

    @staticmethod
    def open_dir(dirname):
        pass

    @staticmethod
    def destroy_dir(name):
        pass

    @staticmethod
    def copy_file(from_file, to_file):
        pass

    @staticmethod
    def run_job(file, elapsed_time=None):
        pass

    @staticmethod
    def push_job(dir):
        pass

    @staticmethod
    def pop_job():
        pass

    @staticmethod
    def process_dir(path):
        pass

    @staticmethod
    def job(argc, argv):
        pass


def get_last_error_msg():
    pass
    # lock = 0
    # wlock(lock)
    # sz_buf = ctypes.create_unicode_buffer(256)
    # lp_msg_buf = ctypes.c_void_p()
    # dw = ctypes.windll.kernel32.GetLastError()
    #
    # ctypes.windll.kernel32.FormatMessageW(
    #     0x00001000 | 0x00000800,
    #     None,
    #     dw,
    #     0,
    #     ctypes.by_ref(lp_msg_buf),
    #     0, None
    # )
    #
    # lp_msg_buf_str = ctypes.wstring_at(lp_msg_buf)
    # lp_msg_buf_str = lp_msg_buf_str.replace('\n', ' ').replace('\r', ' ')
    # sz_buf.value = f"{lp_msg_buf_str} (error code {dw})"
    #
    # ctypes.windll.kernel32.LocalFree(lp_msg_buf)
    # wunlock(lock)
    # return sz_buf.value


def vsystem(fmt, *args):
    command = fmt % args
    output_debug("calling system('%s')" % command)
    rc = subprocess.call(command, shell=True)
    output_debug("system('%s') returns code %x" % (command, rc))
    return rc


def run_job(file, elapsed_time=None):
    pass
    # output_debug("run_job(char *file='%s') starting", file)
    #
    # dir = file[:file.rfind('.')]
    # ext = file[file.rfind('.'):]
    # name = file[file.rfind('/')+1:]
    #
    # if ext is None or ext != ".glm":
    #     output_error("run_job(char *file='%s'): file is not a GLM", file)
    #     return False
    # else:
    #     len = 0
    #     blank = " " * len
    #     len = output_raw("%s\rProcessing %s...\r", blank, name) - len
    #
    # dt = exec_clock()
    # code = vsystem("%s %s %s ",
    #                _pgmptr if _WIN32 else global_gl_executable,
    #                job_cmdargs, name)
    # dt = exec_clock() - dt
    # t = dt / global_ms_per_second
    # if elapsed_time is not None:
    #     elapsed_time = t
    # if code != 0:
    #     output_error("exit code %d received from %s", code, name)
    #     return False
    # output_debug("run_test(char *file='%s') done", file)
    # return True


def push_job(dir):
    pass
    # output_debug("adding %s to job list", dir)
    # item = JOBLIST()
    # item.name = dir[:sizeof(item.name)-1]
    # wlock(joblock)
    # item.next = jobstack
    # jobstack = item
    # wunlock(joblock)


def pop_job():
    pass
    # r_lock(joblock)
    # item = job_stack
    # if job_stack:
    #     job_stack = job_stack.next
    # r_unlock(joblock)
    # output_debug("pulling {} from job list".format(item.name))
    # return item



def job(argc, argv):
    pass
    # i = 0
    # redirect_found = 0
    # job_cmdargs = ""
    # for i in range(1, len(argv)):
    #     if argv[i] == "--redirect":
    #         redirect_found = 1
    #     job_cmdargs += argv[i]
    #     job_cmdargs += " "
    #
    # if not redirect_found:
    #     job_cmdargs += " --redirect all"
    #
    # global_suppress_repeat_messages = 0
    # print("Starting job in directory '{}'".format(global_workdir))
    # var = ctypes.create_string_buffer(64)
    # if ctypes.string_at(global_getvar("clean", var, len(var))) != None and int(var.value) != 0:
    #     clean = True
    #
    # mailto = ctypes.create_string_buffer(1024)
    # global_getvar("mailto", mailto, len(mailto))
    #
    # count = len(os.listdir(global_workdir))
    # if count == 0:
    #     print("no models found to process job in workdir '{}'".format(global_workdir))
    #     exit(XC_RUNERR)
    #
    # n_procs = global_thread_count
    # if n_procs == 0:
    #     n_procs = os.cpu_count()
    # pid = []
    # print("starting job with cmdargs '{}' using {} threads".format(job_cmdargs, n_procs))
    # for i in range(min(count, n_procs)):
    #     t = threading.Thread(target=run_job_proc, args=(i,))
    #     pid.append(t)
    #     t.start()
    #
    # print("begin waiting process")
    # for thread in pid:
    #     thread.join()
    #     print("process {} done".format(i))
    #
    # dt = time.process_time()
    # print("Total job elapsed time: {:.1f} seconds".format(dt))
    # if final_result == 0:
    #     exec_setexitcode(XC_SUCCESS)
    # else:
    #     exec_setexitcode(XC_RUNERR)
    #
    # exit(XC_SUCCESS if final_result == 0 else XC_TSTERR)
