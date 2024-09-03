import sys
from pathlib import Path
import os

from gridlab.gldcore import Save, Legal
from gridlab.gldcore.Class import DynamicClass
from gridlab.gldcore.CmdArg import cmdarg_load
from gridlab.gldcore.Kill import kill_starthandler, kill_stophandler
from gridlab.gldcore.GldRandom import random_init
from gridlab.gldcore.Globals import global_check_version, FAILED, XC_SUCCESS, XC_ENVERR, XC_USRERR, XC_PRCERR, \
    global_pidfile, global_environment, global_savefile, global_kmlfile, global_profiler, global_pauseatexit, XC_ARGERR, \
    XC_INIERR, global_workdir, global_dumpall, global_start_time, global_stop_time, global_thread_count
from gridlab.gldcore.Instance import Exec
from gridlab.gldcore.Kml import Kml
from gridlab.gldcore.Legal import check_version
from gridlab.gldcore.Local import locale_pop
from gridlab.gldcore.Module import Module
from gridlab.gldcore.Output import output_verbose, output_fatal, output_error, output_message, output_init
from gridlab.gldcore.Realtime import realtime_runtime, realtime_starttime
from gridlab.gldcore.Schedule import Schedule
from gridlab.gldcore.ThreadPool import processor_count
from gridlab.gldcore.TimeStamp import timestamp_set_tz, TS_NEVER

import atexit
import os
import signal


def terminate_process(pid=None):
    if pid is not None:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Terminated process {pid}")
        except OSError as e:
            print(f"Error terminating process {pid}: {e}")
    else:
        print(f"Terminated process {os.getpid()}")


# Register the cleanup function to be called at exit
atexit.register(terminate_process)

def find_executable(name, exec_name, path_string):
    """
    Example usage
        name = "gridlabd"  # Example executable name
        exec_name = "gridlabd"  # Example executable path
        path_string = os.getenv("PATH")  # Use system's PATH environment variable
        try:
            exec_path = find_executable(name, exec_name, path_string)
            print(f"Executable path: {exec_path}")
        except RuntimeError as e:
            print(e)


    :param name: Example executable name
    :param exec_name: Example executable path
    :param path_string: Use system's PATH environment variable
    :return:
    """

    exec_path = Path(exec_name)
    if exec_path.is_absolute():
        return exec_path
    elif exec_path.is_relative_to('.') or exec_name.startswith('.'):
        return exec_path.resolve()
    else:
        # Split the path string based on the operating system's path delimiter
        sys_path = path_string.split(os.pathsep)

        # Define a function to check if the path exists
        def check_exists(gldpath, gldpath_exe):
            if gldpath.exists():
                return gldpath
            elif gldpath_exe.exists():
                return gldpath_exe
            return None

        # Iterate through the system path to find the executable
        for path in sys_path:
            gldpath = Path(path) / name
            gldpath_exe = Path(path) / f"{name}.exe"  # Append .exe for Windows compatibility
            check_path = check_exists(gldpath, gldpath_exe)
            if check_path is not None:
                return check_path

    raise RuntimeError("Unable to determine executable path")



class Main:
    """
    This script implements the main entry point of GridLAB-D.

    Returns:
    Exit codes XC_SUCCESS, etc. (see gridlabd.h)
    """

    def __init__(self):
        pass

    @staticmethod
    def pause_at_exit(self):
        pass

    @staticmethod
    def delete_pidfile(self):
        pass

    def split_path(self, path, sep):
        """
        Splits the given path using the specified separator and returns the list of tokens
        """
        tokens = path.split(sep)
        return tokens


    def main(self, argc, argv):
        WIN32 = True
        _DEBUG = True
        _WIN32 = True
        LEGAL_NOTICE = True
        DUMP_SCHEDULES = True
        global global_stop_time
        global global_pidfile
        # global_start_time, global_thread_count
        global_gl_executable = find_executable("gridlabd", argv[0], os.getenv("PATH"))
        root_path = global_gl_executable.parent_path().parent_path()
        global_gl_share = root_path / "share"
        global_gl_include = root_path / "include"
        global_gl_lib = root_path / "lib"
        global_gl_bin = root_path / "bin"
        global_gl_path = (os.getenv("GLPATH", "") + os.sep + global_gl_lib.string() + os.sep +
                          global_gl_share.string() + os.sep +
                          global_gl_include.string() + os.sep +
                          global_gl_bin.string())
        browser = os.getenv("GLBROWSER")
        # set the default timezone
        timestamp_set_tz(None)

        Exec.exec_clock() # initialize the wall clock
        realtime_starttime() # mark start

        # set the process info
        global_process_id = os.getpid()

        # specify the default browser
        if browser != None:
            global_browser = browser

        if WIN32 and _DEBUG:
            exit(pause_at_exit)

        if _WIN32:
            kill_starthandler()
            atexit(kill_stophandler)

        # capture the execdir
        global_execname = argv[0]
        global_execdir = argv[0]
        pd1 = global_execdir.find('/')
        pd2 = global_execdir.find('\\')
        if pd1 > pd2:
            pd1 = ""
        elif pd2 > pd1:
            pd2 = ""

        # determine current working directory
        result = os.getcwd(global_workdir)

        # capture the command line
        global_command_line = " ".join(sys.argv[1:])

        # main initialization
        if not output_init(argc, argv) or not self.exec_init():
            raise Exception(XC_INIERR)

        # set thread count equal to processor count if not passed on command-line
        if global_thread_count == 0:
            global_threadcount = processor_count()
        output_verbose("detected %d processor(s)", processor_count())
        output_verbose("using %d helper thread(s)", global_threadcount)

        # process command line arguments
        if cmdarg_load(argc, argv) == FAILED:
            output_fatal("shutdown after command line rejected")
            #	TROUBLESHOOT
            #    The command line is not valid and the system did not
            #    complete its startup procedure.  Correct the problem
            #    with the command line and try again.
            #
            raise Exception(XC_ARGERR)


        # stitch clock
        global_clock = global_start_time

        # Check to see if stoptime is set - if not, set to 1-year later
        if global_stop_time == TS_NEVER:
            global_stop_time = global_start_time + 31536000


        # initialize scheduler
        self.sched_init(0)

        # recheck threadcount in case user set it 0
        if global_threadcount == 0:
            global_threadcount = processor_count()
            output_verbose("using %d helper thread(s)", global_threadcount)

        # see if newer version is available
        if global_check_version:
            check_version(1)

        # setup the random number generator
        random_init()

        # pidfile
        if global_pidfile:
            fp = open(global_pidfile, "w")
            if fp == None:
                output_fatal("unable to create pidfile '%s'", global_pidfile)
                #	TROUBLESHOOT
                #    The system must allow creation of the process id file at
                #    the location indicated in the message.  Create and/or
                #    modify access rights to the path for that file and try again.
                #
                exit(XC_PRCERR)

            getpid_ = os.getpid()

            fp.write("%d\n".format(getpid_))
            output_verbose("process id %d written to %s".format(getpid_, global_pidfile))
            fp.close()
            exit(delete_pidfile)


        # do legal stuff
        if LEGAL_NOTICE:
            if global_pidfile == "" and Legal.legal_notice() == FAILED:
                raise Exception(XC_USRERR)

        # start the processing environment
        output_verbose("load time: %d sec".format(realtime_runtime()))
        output_verbose("starting up %s environment".format(global_environment))
        if self.environment_start(argc, argv) == FAILED:
            output_fatal("environment startup failed: %s".format("-1"))
            #	TROUBLESHOOT
            #    The requested environment could not be started.  This usually
            #    follows a more specific message regarding the startup problem.
            #    Follow the recommendation for the indicated problem.
            #
            if self.exec_getexitcode() == XC_SUCCESS:
                self.exec_setexitcode(XC_ENVERR)


        # save the model
        if global_savefile:
            if Save.saveall(global_savefile) == FAILED:
                output_error("save to '%s' failed".format(global_savefile))

        # do module dumps
        if global_dumpall != False:
            output_verbose("dumping module data")
            Module.module_dumpall()

        # KML output
        if global_kmlfile:
            Kml.kml_dump(global_kmlfile)

        # terminate
        Module().module_termall()

        # wrap up
        output_verbose("shutdown complete")

        # profile results
        if global_profiler:
            DynamicClass.class_profiles()
            Module.module_profiles()

        if DUMP_SCHEDULES:
            # dump a copy of the schedules for reference
            Schedule.schedule_dumpall("schedules.txt")

        # restore locale
        locale_pop()

        # if pause enabled
        if not WIN32:
            if _DEBUG:
                if global_pauseatexit:
                    output_verbose("pausing at exit")

                    # Replicate "pause" on Windows
                    output_message("Press Enter to continue . . .")
                    input("Waiting until press Enter to continue")

        # compute elapsed runtime
        output_verbose("elapsed runtime %d seconds", realtime_runtime())
        output_verbose("exit code %d", self.exec_getexitcode())
        print("exiting main")
        exit()  # exec_getexitcode())



    @staticmethod
    def check_exists(gldpath, gldpath_exe):
        if os.path.exists(gldpath):
            return gldpath
        elif os.path.exists(gldpath_exe):
            return gldpath_exe
        return ""

    @staticmethod
    def signal_handler(signum, frame):
        pass

    @staticmethod
    def exec_clock():
        pass

    @staticmethod
    def realtime_starttime():
        pass

    @staticmethod
    def exec_getexitcode():
        pass

    @staticmethod
    def exec_setexitcode(exit_code):
        pass

    @staticmethod
    def output_init(args_count, args):
        pass

    @staticmethod
    def exec_init():
        pass

    @staticmethod
    def processor_count():
        pass

    @staticmethod
    def cmdarg_load(args_count, args):
        pass

    @staticmethod
    def sched_init(arg):
        pass

    @staticmethod
    def check_version(arg):
        pass

    @staticmethod
    def random_init():
        pass

    @staticmethod
    def environment_start(args_count, args):
        pass

    @staticmethod
    def save_all(save_file):
        pass

    @staticmethod
    def module_termall():
        pass

    @staticmethod
    def kml_dump(kml_file):
        pass

    @staticmethod
    def schedule_dumpall(schedule_file):
        pass

    @staticmethod
    def locale_pop():
        pass


def pause_at_exit():
    global global_pause_at_exit
    if global_pause_at_exit:
        os.system("pause")

def delete_pidfile():
    os.unlink(global_pidfile)