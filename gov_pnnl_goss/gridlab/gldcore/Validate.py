import argparse
import sys
import shutil
import subprocess
import threading
import time

from gridlab.gldcore.Globals import global_validate_options, global_workdir, global_threadcount, VALIDATEOPTIONS

dirstack = None
next_id = 0
result_code = None
dirlock = 0
global_gl_executable = None


class DirList:
    def __init__(self, name, id, next=None):
        self.name = name
        self.id = id
        self.next = next


class Counters:
    def __init__(self):
        self._lock = threading.Lock()
        self.n_scanned = self.n_tested = self.n_passed = 0
        self.n_files = self.n_success = self.n_failed = self.n_exceptions = self.n_access = 0

        self.n_tested = 0
        self.n_passed = 0
        self.n_success = 0
        self.n_failed = 0
        self.n_exceptions = 0
        self.n_access = 0

    def __add__(self, other):
        with self._lock:
            self.n_scanned += other.n_scanned
            self.n_tested += other.n_tested
            self.n_passed += other.n_passed
            self.n_files += other.n_files
            self.n_success += other.n_success
            self.n_failed += other.n_failed
            self.n_exceptions += other.n_exceptions
        return self

    def __iadd__(self, other):
        self.__add__(other)
        return self

    def get_scanned(self):
        return self.n_scanned

    def get_tested(self):
        return self.n_tested

    def get_passed(self):
        return self.n_passed

    def inc_scanned(self):
        with self._lock:
            self.n_scanned += 1

    def inc_tested(self):
        with self._lock:
            self.n_tested += 1

    def inc_passed(self):
        with self._lock:
            self.n_passed += 1

    def get_nfiles(self):
        return self.n_files

    def get_nsuccess(self):
        return self.n_success

    def get_nfailed(self):
        return self.n_failed

    def get_nexceptions(self):
        return self.n_exceptions

    def inc_files(self, name):
        global global_debug_mode
        global global_verbose_mode
        if global_debug_mode or global_verbose_mode:
            print("processing %s" % name)
        else:
            len_ = 0
            blank = bytearray(1024)
            len_ = min(len_, 1023)
            blank[:len_] = b' ' * len_
            blank[len_] = 0
            print("\r%s\rProcessing %s..." % (blank.decode('utf-8'), name))

        with self._lock:
            self.n_files += 1

    def inc_access(self, name):
        print(f"{name} folder access failure")
        with self._lock:
            self.n_access += 1

    def inc_success(self, name, code, t):
        print(f"{name} success unexpected, code {code} in {t:.1f} seconds")
        with self._lock:
            self.n_success += 1

    def inc_failed(self, name, code, t):
        print("{} error unexpected, code {} ({}) in {:.1f} seconds".format(name, code, "-1", t))
        with self._lock:
            self.n_failed += 1

    def inc_exceptions(self, name, code, t):
        print(f"{name} exception unexpected, code {code} ({-1}) in {t:.1f} seconds")
        with self._lock:
            self.n_exceptions += 1

    def print(self):
        n_ok = self.n_files - self.n_success - self.n_failed - self.n_exceptions
        print("\nValidation report:")
        if self.n_access:
            print("%d directory access failures" % self.n_access)
        print("%d models tested" % self.n_files)
        if self.n_files != 0:
            if self.n_success:
                print("%d unexpected successes" % self.n_success)
            if self.n_failed:
                print("%d unexpected errors" % self.n_failed)
            if self.n_exceptions:
                print("%d unexpected exceptions" % self.n_exceptions)
            print("%d tests succeeded" % n_ok)
            print("%.0f%% success rate" % (100.0 * n_ok / self.n_files))


    def get_nerrors(self):
        return self.n_success + self.n_failed + self.n_exceptions + self.n_access
    #
    # def wlock(self):
    #     pass
    #
    # def wunlock(self):
    #     pass
    #
    # def rlock(self):
    #     pass
    #
    # def runlock(self):
    #     pass

    @staticmethod
    def destroy_dir(name):
        file_path = ""
        if not os.path.exists(name):
            return True  # Directory does not exist
        try:
            for filename in os.listdir(name):
                file_path = os.path.join(name, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            return True
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
            return False


    def run_test(self, file, elapsed_time=None):
        global global_gl_executable
        print(f"run_test(char *file='{file}') starting")
        result = Counters()

        is_err = "_err." in file or "_err_" in file
        is_exc = "_exc." in file or "_exc_" in file
        is_opt = "_opt." in file or "_opt_" in file

        # Assuming global_validateoptions and VO_* constants are defined elsewhere
        if is_err and not (global_validate_options() & VALIDATEOPTIONS.VO_TSTERR):
            return result
        if is_exc and not (global_validate_options() & VALIDATEOPTIONS.VO_TSTEXC):
            return result
        if is_opt and not (global_validate_options() & VALIDATEOPTIONS.VO_TSTOPT):
            return result
        if not is_err and not is_opt and not is_exc and not (global_validate_options() & VALIDATEOPTIONS.VO_TSTRUN):
            return result

        dir_name, file_name = os.path.split(file)
        name, ext = os.path.splitext(file_name)
        if ext != ".glm":
            print(f"run_test(char *file='{file}'): file is not a GLM")
            return result

        # Clean directory if necessary
        if clean and not self.destroy_dir(dir_name):
            print(f"run_test(char *file='{file}'): unable to destroy test folder {dir_name}")
            result.inc_access(file)
            return result

        # Create test folder
        try:
            if clean:
                os.makedirs(dir_name, exist_ok=True)
            print(f"created test folder '{dir_name}'")
        except OSError as e:
            print(f"run_test(char *file='{file}'): unable to create test folder {dir_name}")
            result.inc_access(file)
            return result

        # Copy file to test folder
        out = os.path.join(dir_name, f"{name}.glm")
        if not self.copyfile(file, out):
            print(f"run_test(char *file='{file}'): unable to copy to test folder {dir_name}")
            result.inc_access(file)
            return result

        # Execute command
        start_time = time.time()
        command = f"{global_gl_executable} -W {dir_name} {validate_cmd_args} {name}.glm"
        try:
            subprocess.run(command, check=True, shell=True)
            code = 0  # Assuming success corresponds to 0
        except subprocess.CalledProcessError as e:
            code = e.returncode

        elapsed = time.time() - start_time
        if elapsed_time is not None:
            elapsed_time[0] = elapsed  # Assuming elapsed_time is a list to mimic pointer behavior

        # Update counters based on command execution outcome
        # This section needs adaptation based on the handling of execution outcome in Python

        print(f"run_test(char *file='{file}') done")
        # Optionally destroy test directory after test execution
        if clean and not self.destroy_dir(dir_name):
            print(f"run_test(char *file='{file}'): unable to destroy test folder after the test {dir_name}")
            result.inc_access(file)

        return result


final = Counters()
clean = False

report_ext = None

report_cols = 0
report_rows = 0
report_lock = 0
import os

# Assuming global variables are defined at the module level in Python
report_file = "validate.txt"  # Default report file name
report_fp = None
report_col = "    "  # Default column separator
report_eol = "\n"   # End of line character
report_eot = "\f"   # End of transmission/page character
# Note: Python does not use locks in the same straightforward way, especially for file operations.

#
# def report_title(fmt, *args):
#     global report_fp, report_cols
#     len = 0
#     if report_fp:
#         # Python's file operations are inherently thread-safe for most use cases,
#         # but if you're using threads and need explicit locking, consider using threading.Lock
#         # Assuming wlock and wunlock are part of your threading mechanism
#         # wlock(report_lock)
#
#         if report_cols > 0:
#             report_fp.write(report_eol)
#             len += len(report_eol)
#         formatted_string = fmt.format(*args)  # Using str.format for formatting
#         report_fp.write(formatted_string)
#         len += len(formatted_string)
#
#         report_fp.flush()  # Ensure the output is written to the file
#         report_cols += 1
#
#         # wunlock(report_lock)
#     return len


# def report_title(fmt, *args):
#     len_ = 0
#     if report_fp:
#         wlock(report_lock)
#         if report_cols > 0:
#             len_ = fprintf(report_fp, "%s" % report_eol)
#         args_ptr = (ctypes.c_char_p * len(args))(*args)
#         len_ += vfprintf(report_fp, fmt, args_ptr)
#         fflush(report_fp)
#         wunlock(report_lock)
#     return len_


#
# def report_newtable(table):
#     len = 0
#     if report_fp:
#         wlock(report_lock)
#         report_rows += 1
#         if report_cols > 0:
#             len += fprintf(report_fp, "%s" % report_eol)
#         report_cols = 0
#         len = fprintf(report_fp, "%s%s%s" % (report_eot, table, report_eol))
#         fflush(report_fp)
#         wunlock(report_lock)
#     return len



# def Getvalidate_cmdargs():
#     validate_cmdargs = [1024]
#     return validate_cmdargs

# def vsystem(fmt, *args):
#     result = None
#     command = fmt % args
#     print(f"calling system('{command}')")  # Assuming output_debug prints to some debug log
#     try:
#         result = subprocess.run(command, shell=True, check=True)
#         print(f"system('{command}') returns code {result.returncode}")
#     except subprocess.CalledProcessError as e:
#         print(f"system('{command}') returns code {e.returncode}")
#     return result.returncode if result else None


class DirStack:
    """
    dir_stack = DirStack()
    dir_stack.push("directory_1")
    dir_stack.push("directory_2")

    top_item = dir_stack.peek()
    print(f"Top item on the stack: {top_item.name}, ID: {top_item.id}")

    popped_item = dir_stack.pop()
    print(f"Popped item: {popped_item.name}, ID: {popped_item.id}")

    if not is_stack_empty(dir_stack):
    print("Stack is not empty.")
    else:
    print("Stack is empty.")
    """
    def __init__(self):
        self.head = None
        self.next_id = 0

    def push(self, name):
        new_dir = DirList(name, self.next_id)
        new_dir.next = self.head
        self.head = new_dir
        self.next_id += 1

    def pop(self):
        if self.head is None:
            return None
        removed_dir = self.head
        self.head = self.head.next
        return removed_dir

    def peek(self):
        return self.head

    def pushdir(self, dir):
        global dirstack
        print(f"Adding {dir} to process stack")
        new_dir = DirList(dir, self.next_id)
        new_dir.next = self.head
        self.head = new_dir
        self.next_id += 1
        dirstack = new_dir

    def popdir(self):
        if self.head is None:
            return None
        removed_dir = self.head
        self.head = self.head.next
        print(f"Pulling {removed_dir.name} from process stack")
        return removed_dir

        # r_lock(dir_lock)
        # item = dir_stack
        # if dir_stack:
        #     dir_stack = dir_stack.next
        # r_unlock(dir_lock)
        # print("pulling %s from process stack" % item.name)
        # return item

    def sort_stack(self):
        # Convert stack to a list for sorting
        items = []
        while not self.is_empty():
            item = self.pop()
            items.append((item.id, item.name))

        # Sort by name
        items.sort(key=lambda x: x[1])

        # Rebuild the stack
        for item in reversed(items):
            self.push(item[1])  # Re-push items by sorted order

    def is_empty(self):
        return self.head is None

    def is_stack_empty(dir_stack):
        return dir_stack.head is None

    def sort_list(self):
        done = False
        while not done:
            done = True
            prev = None
            item = self.head
            while item is not None and item.next is not None:
                if item.name > item.next.name:
                    done = False
                    if prev is None:
                        tmp = item.next
                        item.next = tmp.next
                        tmp.next = item
                        self.head = tmp
                    else:
                        tmp = item.next
                        item.next = tmp.next
                        tmp.next = item
                        prev.next = tmp
                    # Swap completed, move back to previous node to continue correct iteration
                    item = tmp
                prev = item
                item = item.next if item else None

    def print_list(self):
        current = self.head
        while current is not None:
            print(f'{current.name} -> ', end='')
            current = current.next
        print('None')

# def report_new_row():
#     len = 0
#     if report_fp:
#         wlock(report_lock)
#         report_cols = 0
#         report_rows += 1
#         len = report_fp.write(report_eol)
#         report_fp.flush()
#         wunlock(report_lock)
#     return len



#
# def report_close():
#     wlock(report_lock)
#     if report_fp:
#         report_fp.close()
#     report_fp = None
#     wunlock(report_lock)
#     return report_rows




# def get_last_error_msg():
#     lock = threading.Lock()
#     lock.acquire()
#
#     szBuf = ctypes.create_unicode_buffer(256)
#     lpMsgBuf = ctypes.c_void_p
#     dw = ctypes.windll.kernel32.GetLastError()
#
#     ctypes.windll.kernel32.FormatMessageW(
#         0x00000100 | 0x00000200,
#         None,
#         dw,
#         0x0000,
#         ctypes.byref(lpMsgBuf),
#         0,
#         None
#     )
#
#     lpMsgBuf_str = ctypes.wstring_at(lpMsgBuf)
#     lpMsgBuf_str = lpMsgBuf_str.replace('\n', ' ').replace('\r', ' ')
#     szBuf.value = f'{lpMsgBuf_str} (error code {dw})'
#
#     ctypes.windll.kernel32.LocalFree(lpMsgBuf)
#     lock.release()
#     return szBuf.value



def copyfile(from_path, to_path):
    try:
        shutil.copyfile(from_path, to_path)
        return True
    except IOError as e:
        print(f"Unable to copy from {from_path} to {to_path}: {e}")
        return False

def encode_result(data):
    """
    # Example usage
        data = "hello"
        encoded_data = encode_result(data)
        print(encoded_data)
    :param data:
    :return:
    """
    sz = len(data)
    len_encoded = (sz + 1) // 2 + 1
    encoded = [0] * len_encoded  # Pre-fill with zeros

    # Encode data into half-bytes
    for i in range(sz):
        ndx = i // 2
        shft = (i % 2) * 2
        encoded[ndx] |= ord(data[i]) << shft  # Use ord to get byte value

    # Convert each half-byte into its hexadecimal character
    encoded_str = ''.join(['0123456789ABCDEF'[value] for value in encoded])

    return encoded_str


def find_executable(executable_name, fallback_dir, search_path):
    # Attempt to find the executable in the system's PATH
    executable_path = shutil.which(executable_name)
    if executable_path:
        return executable_path

    # If not found, attempt to search in the fallback directory
    fallback_path = os.path.join(os.path.dirname(fallback_dir), executable_name)
    if os.path.isfile(fallback_path):
        return fallback_path

    # Lastly, attempt to search in the PATH directories explicitly
    for dir_path in search_path.split(os.pathsep):
        potential_path = os.path.join(dir_path, executable_name)
        if os.path.isfile(potential_path):
            return potential_path

    return None

def process_dir(path, run_glms=False, result_code=None):
    # Check for block file
    global dirstack
    blockfile = os.path.join(path, 'validate.no')
    if os.path.exists(blockfile):  #  and not global_force_validate:
        print(f"Processing directory '{path}' blocked by presence of 'validate.no' file")
        return 0

    count = 0
    print(f"Processing directory '{path}' with run of GLMs {'enabled' if run_glms else 'disabled'}")
    # Assuming `final` is a global instance of `Counters` or similar class
    final.inc_scanned()
    if run_glms:
        final.inc_tested()

    if not os.path.isdir(path):
        return 0  # Nothing to do

    for entry in os.scandir(path):
        if entry.name.startswith('.'):
            continue  # Ignore anything that starts with a dot

        item_path = os.path.join(path, entry.name)
        if entry.is_dir():
            # Recursively process directories named "autotest" or any directory if not checking for name
            if entry.name == 'autotest' or not run_glms:
                count += process_dir(item_path, True if entry.name == 'autotest' else run_glms)
        else:
            _, ext = os.path.splitext(entry.name)
            if run_glms and '/test_' in item_path and ext == '.glm':
                dirstack.pushdir(item_path)  # Assuming pushdir adds the item to a processing list
                count += 1

    # Placeholder for reporting data, adjust according to your Python reporting mechanism
    if global_validate_options & VALIDATEOPTIONS.VO_RPTDIR:
        # report_data logic here
        pass

    return count



def report_close():
    global report_fp
    if report_fp:
        report_fp.close()
        report_fp = None
    return report_rows


# To mimic the report_data function:
def report_data(fmt="", *args):
    return report_write(fmt, *args, is_title=False)
#
# def report_data(fmt="", *args):
#     len = 0
#     if report_fp:
#         wlock(report_lock)
#         if report_cols > 0:
#             len = ctypes.cdll.msvcrt.fprintf(report_fp, ctypes.c_char_p(report_col.encode('utf-8')))
#         va_list_ptr = (ctypes.c_char_p * len)(*args)
#         len += ctypes.cdll.msvcrt.vfprintf(report_fp, fmt.encode('utf-8'), va_list_ptr)
#         wunlock(report_lock)
#     return len



def report_newrow():
    global report_cols, report_rows
    len_written = 0
    if report_fp:
        report_cols = 0
        report_rows += 1
        report_fp.write(report_eol)
        len_written = len(report_eol)
        report_fp.flush()
    return len_written




def report_newtable(table):
    global report_cols, report_rows
    len_written = 0
    if report_fp:
        report_rows += 1
        if report_cols > 0:
            report_fp.write(report_eol)
            len_written += len(report_eol)
        report_cols = 0
        table_header = f"{report_eot}{table}{report_eol}"
        report_fp.write(table_header)
        len_written += len(table_header)
        report_fp.flush()
    return len_written


def report_open():
    global report_fp, report_col, report_eot
    # Python does not have a direct equivalent of global_getvar, assuming it's handled elsewhere or using direct assignment

    if report_fp is None:
        report_ext = os.path.splitext(report_file)[1]
        if report_ext == ".csv":
            report_col = ","
            report_eot = "\n"
        elif report_ext == ".txt":
            report_col = "\t"
            report_eot = "\n"
        try:
            report_fp = open(report_file, "w")
            return True
        except IOError:
            return False
    return report_fp is not None


# To mimic the report_title function:
def report_title(fmt, *args):
    return report_write(fmt, *args, is_title=True)


def report_write(fmt, *args, is_title=False):
    global report_cols
    len_written = 0
    if report_fp:
        separator = report_eol if is_title else report_col
        if report_cols > 0:
            report_fp.write(separator)
            len_written += len(separator)
        formatted_str = fmt.format(*args)
        report_fp.write(formatted_str)
        len_written += len(formatted_str)
        report_fp.flush()
        report_cols += 1
    return len_written


def run_test_proc(id, dir_stack):
    """
    # Example of starting a thread
        dir_stack = DirStack()
        # Populate dir_stack as needed

        thread = threading.Thread(target=run_test_proc, args=(1, dir_stack))
        thread.start()
        thread.join()
    :param id:
    :param dir_stack:
    :return:
    """
    print(f"Starting run_test_proc id {id}")
    passed = True
    while True:
        item = dir_stack.popdir()
        if item is None:
            break
        print(f"Process {id} picked up '{item.name}'")
        # Simulate running a test and processing results
        # result = run_test(item.name, dt)
        # Example processing logic:
        # if result.get_nerrors() > 0: passed = False

        # Update result_code and generate a report as necessary
        # final += result

    if passed:
        pass  # Update the 'final' counter appropriately



def validate(argv):

    """
    # def validate(argc, argv):
    #     validate_cmdargs = validate_cmd_args(*argv)
    #     global_suppress_repeat_messages = 0
    #     print(f"Starting validation test in directory '{global_workdir}'")
    #     var = os.getenv("clean")
    #     clean = bool(var) if var and int(var) != 0 else False
    #     report_file = "report.txt"
    #     report_fp = open(report_file, "w")
    #     try:
    #         report_fp.write("VALIDATION TEST REPORT\n")
    #         report_fp.write(f"GridLAB-D {global_version_major}.{global_version_minor}.{global_version_patch}-{global_version_build} ({global_version_branch})\n")
    #         timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S %z')
    #         report_fp.write(f"Date: {timestamp}\n")
    #         user = os.getenv("USERNAME") if os.name == 'nt' else os.getenv("USER")
    #         report_fp.write(f"User: {user if user else '(NA)'}\n")
    #         host = os.getenv("COMPUTERNAME") if os.name == 'nt' else os.getenv("HOSTNAME")
    #         report_fp.write(f"Host: {host if host else '(NA)'}\n")
    #         report_fp.write(f"Platform: {8 * 8}-bit {global_platform} {'DEBUG' if _DEBUG else 'RELEASE'}\n")
    #         report_fp.write(f"Workdir: {global_workdir}\n")
    #         report_fp.write(f"Arguments: {validate_cmdargs}\n")
    #         report_fp.write(f"Clean: {'TRUE' if clean else 'FALSE'}\n")
    #         report_fp.write(f"Threads: {global_threadcount}\n")
    #         options = global_get_var("validate")
    #         report_fp.write(f"Options: {options if options else '(NA)'}\n")
    #         mailto = global_get_var("mailto")
    #         report_fp.write(f"Mailto: {mailto if mailto else '(NA)'}\n")
    #         if VALIDATEOPTIONS.VO_RPTDIR & global_validate_options:
    #             report_fp.write("DIRECTORY SCAN RESULTS\n")
    #             process_dir(global_workdir)
    #             sortlist()
    #         if VALIDATEOPTIONS.VO_RPTGLM & global_validate_options:
    #             report_fp.write("FILE TEST RESULTS\n")
    #         n_procs = global_threadcount or len(os.sched_getaffinity(0))
    #         n_procs = fmin(final.get_tested(), n_procs)
    #         pid = []
    #         for i in range(n_procs):
    #             pid.append(threading.Thread(target=run_test_proc, args=(i,)))
    #             pid[i].start()
    #         for i in range(n_procs):
    #             pid[i].join()
    #         final.print()
    #         dt = Exec.clock() / global_ms_per_second
    #         report_fp.write(f"Total validation elapsed time: {dt} seconds\n")
    #         if final.get_nerrors() == 0:
    #             Exec.setexitcode(XC_SUCCESS)
    #         else:
    #             Exec.setexitcode(XC_TSTERR)
    #         report_fp.write("OVERALL RESULTS\n")
    #         report_fp.write("Directory results\n")
    #         report_fp.write(f"Scanned: {final.get_scanned()}\n")
    #         report_fp.write(f"Denied: {final.get_naccess()}\n")
    #         report_fp.write(f"Tested: {final.get_tested()}\n")
    #         n_failed = final.get_tested() - final.get_passed()
    #         report_fp.write(f"Failed: {n_failed}\n")
    #         report_fp.write("File results\n")
    #         report_fp.write(f"Tested: {final.get_nfiles()}\n")
    #         report_fp.write(f"Passed: {final.get_nfiles() - final.get_nerrors()}\n")
    #         report_fp.write(f"Failed: {final.get_nerrors()}\n")
    #         report_fp.write("Unexpected results\n")
    #         report_fp.write(f"Successes: {final.get_nsuccess()}\n")
    #         report_fp.write(f"Errors: {final.get_nfailed()}\n")
    #         report_fp.write(f"Exceptions: {final.get_nexceptions()}\n")
    #         report_fp.write(f"Runtime: {dt} s\n")
    #         result_code = encode_result(result_code, next_id)
    #         report_fp.write(f"Result code: {result_code}\n")
    #     finally:
    #         report_fp.write("END TEST REPORT\n")
    #         report_fp.close()
    #
    #     if mailto and mailto != "":
    #         if os.name != 'nt':
    #             if os.uname().sysname == 'Darwin':
    #                 MAILER = "/usr/bin/mail"
    #             else:
    #                 MAILER = "/bin/mail"
    #             if os.system(f"{MAILER} -s 'GridLAB-D Validation Report ({final.get_nerrors()} errors)' {mailto} < {report_file}") == 0:
    #                 print(f"Mail message sent to {mailto}")
    #             else:
    #                 print(f"Error sending notification to {mailto}")
    #
    #     exit(XC_SUCCESS if final.get_nerrors() == 0 else XC_TSTERR)
    #
    #
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--redirect', action='store_true')
    parser.add_argument('--clean', action='clean')
    args, unknown_args = parser.parse_known_args(argv[1:])

    validate_cmdargs = " ".join(unknown_args)
    if not args.redirect:
        validate_cmdargs += " --redirect all"

    if args.clean:
        clean = True
    else:
        clean = False
    global_suppress_repeat_messages = 0
    dirstack = DirStack()
    print(f"Starting validation test in directory '{global_workdir}'")

    # Placeholder for report opening and title setting
    report_open()

    # Placeholder for report data collection and processing

    if global_validate_options & VALIDATEOPTIONS.VO_RPTDIR:
        process_dir(global_workdir, True)
        dirstack.sort_list()

    n_procs = global_threadcount if global_threadcount > 0 else os.cpu_count()
    threads = []
    for i in range(n_procs):
        thread = threading.Thread(target=run_test_proc, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    # Finalization and report generation

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

if __name__ == "__main__":
    script_directory = os.path.dirname(sys.argv[0])
    system_path = os.getenv('PATH')
    global_gl_executable = find_executable("gridlabd", script_directory, system_path)
    validate(sys.argv)