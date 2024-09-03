import sys
import os
import atexit
from enum import Enum
from typing import TextIO


# Constants for output types
class OutputType(Enum):
    NONE = 0
    ERROR = 1
    STANDARD = 2
    VERBOSE = 3


# Structure for redirection
class Redirection:
    output = None
    error = None
    warning = None
    debug = None
    verbose = None
    profile = None
    progress = None


# Dictionary mapping names to redirection attributes
redirection_map = {
    "output": ("output", "gridlabd.out"),
    "error": ("error", "gridlabd.err"),
    "warning": ("warning", "gridlabd.wrn"),
    "debug": ("debug", "gridlabd.dbg"),
    "verbose": ("verbose", "gridlabd.inf"),
    "profile": ("profile", "gridlabd.pro"),
    "progress": ("progress", "gridlabd.prg"),
}

# Constants
CHECK = 0xcdcd
FAILED = -1
FS_ERR = 2

FS_IN = 0  # Define constants for file streams
FS_STD = 1
buffer = bytearray(65536)
flush = 0
last_out = OutputType.NONE

notify_error = None  # Function to notify error
output_lock = 0
overflow = CHECK
prefix = ""  # Replace with your message prefix

redirect_output = sys.stdout  # Replace with your output redirection, e.g., a file or sys.stdout
stderr_print_function = print
stdout_print_function = print  # Initialize print functions to default to Python's print function

# Global variables
global_debug_mode = True  # Replace with your actual debug mode setting
global_error_mode = True  # Replace with your actual error mode setting
global_fatal_mode = True  # Replace with your actual fatal error mode setting
global_quiet_mode = False  # Replace with your actual quiet mode setting
global_suppress_repeat_messages = True  # Replace with your actual suppress setting
global_verbose_mode = True  # Replace with your actual verbose mode setting
global_warning_mode = True  # Replace with your actual warning mode setting

# Function to set the print function for stdout
def output_set_stdout(call):
    global stdout_print_function
    stdout_print_function = call

# Function to set the print function for stderr
def output_set_stderr(call):
    global stderr_print_function
    stderr_print_function = call

# Function to initialize output
def output_init(argc, argv):
    atexit.register(output_cleanup)
    return 1


# Function to clean up output
def output_cleanup():
    output_verbose(None)
    output_warning(None)
    output_error(None)
    output_fatal(None)
    output_message(None)
    output_debug(None)


# Function to enable output prefix
def output_prefix_enable():
    global prefix, flush, last_out

    cpuid = os.sched_getcpuid(0)
    procid = os.sched_getprocid()

    last_out = OutputType.NONE
    print("reading cpuid()")

    print("reading procid()")

    print("sprintf'ing m/s name")
    global_multirun_mode = None  # Replace this with the actual global_multirun_mode value

    if global_multirun_mode == "MRM_STANDALONE":
        prefix = f"-{cpuid:02d}({procid:05d}): "
    elif global_multirun_mode == "MRM_MASTER":
        flush = 1
        prefix = f"M{cpuid:02d}({procid:05d}): "
    elif global_multirun_mode == "MRM_SLAVE":
        flush = 1
        prefix = f"S{cpuid:02d}({procid:05d}): "

    print("exiting output_prefix_enable")


# Function to send output to both stdout and stderr
def output_both_stdout():
    sys.stderr = sys.stdout

# Function to redirect the output stream
def output_set_stream(fs, newfp):
    if fs == FS_STD:
        sys.stdout = newfp
    elif fs == FS_ERR:
        sys.stderr = newfp

# Function to redirect output to a file
def output_redirect(name, path):
    try:
        if path:
            return open(path, "w")
        else:
            return open(name, "w")
    except Exception as e:
        print(f"Failed to redirect output: {e}")
        return None

# # Function to redirect an output stream to a file
# def output_redirect(name, path):
#     global redirection
#
#     if name in redirection_map:
#         attr_name, default_file = redirection_map[name]
#
#         mode = "w"
#
#         old_fp = getattr(redirection, attr_name)
#
#         if old_fp:
#             old_fp.close()
#
#         # Test for append mode, path led with +
#         if path is not None and path.startswith("+"):
#             mode = "a"
#             path = path[1:]
#
#         setattr(redirection, attr_name, open(path if path else default_file, mode))
#
#         if getattr(redirection, attr_name):
#             sys.stdout.flush()
#
#         return getattr(redirection, attr_name)
#     else:
#         return None



# Function for fatal output
def output_fatal(format, *args):
    stderr_print_function(format, *args)
    return -1  # Return an error code

# # Function to print fatal error messages and exit the program
# def output_fatal(format_str, *args):
#     # Print the fatal error message to stderr
#     print(f"Fatal Error: {format_str}" % args, file=sys.stderr)
#     # You can add additional cleanup or logging logic here if needed
#     sys.exit(1)  # Exit the program with a non-zero status code


# Function for error output
def output_error(format, *args):
    stderr_print_function(format, *args)
    return -1  # Return an error code

# # Function to print error messages
# def output_error(format_str, *args):
#     # Check if error mode is enabled
#     if global_error_mode:
#         # Print the error message to stderr
#         print(f"Error: {format_str}" % args, file=sys.stderr)
#     # You can add additional error-handling logic here if needed


# Function for raw error output
def output_error_raw(format, *args):
    stderr_print_function(format, *args)
    return -1  # Return an error code

# Function for warning output
def output_warning(format, *args):
    stderr_print_function(format, *args)
    return 0

# # Function to print warning messages
# def output_warning(format_str, *args):
#     # Check if warning mode is enabled
#     if global_warning_mode:
#         # Print the warning message to stderr
#         print(f"Warning: {format_str}" % args, file=sys.stderr)

# Function for debug output
def output_debug(format, *args):
    stderr_print_function(format, *args)
    return 0
#
# # Function to output a debug message with printf-style formatting
# def output_debug(format_str, *args):
#     global global_debug_mode
#
#     if global_debug_mode:
#         # Check if there's a format provided
#         if format_str:
#             va_args = args
#             message = format_str % va_args if va_args else format_str
#
#             # Output the debug message
#             print("[DEBUG] " + message)


# Function for verbose output
def output_verbose(format, *args):
    stdout_print_function(format, *args)
    return 0

# # Function to print verbose messages
# def output_verbose(format_str, *args):
#     global last_out
#
#     # Check if verbose mode is enabled
#     if global_verbose_mode:
#         # Prepare the stream
#         prep_stream()
#
#         # Check if the last output was not verbose
#         if last_out != OutputType.VERBOSE:
#             # Print a newline character to separate verbose messages from others
#             print()
#
#         # Print the verbose message
#         print(format_str % args)
#
#         # Update the last output global_property_types
#         last_out = OutputType.VERBOSE


# Function for regular message output
def output_message(format, *args):
    stdout_print_function(format, *args)
    return 0

# # Function to output a message with printf-style formatting
# def output_message(format_str, *args):
#     global global_quiet_mode
#     global global_suppress_repeat_messages
#     global global_verbose_mode
#     global prefix
#     global redirect_output
#
#     if not global_quiet_mode:
#         # Check for repeated message
#         lastfmt = [None]  # Use a list to store the last format
#         count = [0]  # Use a list to store the count
#         format_str = format_str or ""
#
#         def unlock():
#             pass
#
#         def wlock(lock):
#             pass
#
#         try:
#             wlock(output_lock)
#
#             # Check if the message is the same as the last one
#             if format_str and lastfmt[0] == format_str and global_suppress_repeat_messages and not global_verbose_mode:
#                 count[0] += 1
#                 return
#
#             else:
#                 va_args = args
#                 len_msg = 0
#
#                 # Save the current format as the last format
#                 lastfmt[0] = format_str
#
#                 # If count is greater than 0, it means the last message was repeated
#                 if count[0] > 0 and global_suppress_repeat_messages and not global_verbose_mode:
#                     len_msg = len(f"{prefix}last message was repeated {count[0]} times\n")
#                     count[0] = 0
#
#                 if not format_str:
#                     # Skip if there's no format provided
#                     return
#
#                 # Start building the message
#                 va_args = args
#                 message = format_str % va_args if va_args else format_str
#
#                 # Output the message to the defined destination
#                 if redirect_output:
#                     result = redirect_output.write(f"{prefix}{message}\n")
#                     redirect_output.flush()
#                 else:
#                     result = sys.stdout.write(f"{prefix}{message}\n")
#                     sys.stdout.flush()
#
#         finally:
#             unlock()
#


# Function for raw output
def output_raw(format, *args):
    stdout_print_function(format, *args)
    return 0

# Function for test output
def output_test(format, *args):
    stdout_print_function(format, *args)
    return 0

# Function for progress output
def output_progress():
    # Implement progress output logic here
    return 0

# Function for profile output
def output_profile(format, *args):
    # Implement profile output logic here
    return 0

# # Function to notify an error
# def output_notify_error(callback):
#     # Implement notification of error callback here
#     return 0

def output_notify_error(notify_func):
    global notify_error
    notify_error = notify_func
    return 0


# Function to set the time context
def output_set_time_context(ts):
    # Implement setting of time context logic here
    pass

# Function to set the delta time context
def output_set_delta_time_context(ts, delta_ts):
    # Implement setting of delta time context logic here
    pass

# Function to get the time context
def output_get_time_context():
    # Implement getting of time context logic here
    return ""

# Function for xsd output
def output_xsd(spec):
    # Implement xsd output logic here
    return 0

# Function for xsl output
def output_xsl(fname, n_mods, p_mods):
    # Implement xsl output logic here
    return 0


# Function to redirect an output stream
def output_redirect_stream(name, fp):
    global redirection

    if name in redirection_map:
        attr_name, default_file = redirection_map[name]

        old_fp = getattr(redirection, attr_name)
        setattr(redirection, attr_name, fp)

        if getattr(redirection, attr_name):
            sys.stdout.flush()

        return old_fp
    else:
        return None



# Function to print to standard output
def default_printstd(format, *args):
    global last_out

    prep_stream()

    if last_out != OutputType.STANDARD:
        print()
        last_out = OutputType.STANDARD

    sys.stdout.write(format % args)

    if flush:
        sys.stdout.flush()

    return len(format % args)


# Initialize current streams
curr_stream = [TextIO] * 3
stream_prep = False


# Function to prepare streams
def prep_stream():
    global stream_prep
    global curr_stream
    if stream_prep:
        return

    stream_prep = 1

    if curr_stream[0] is None:
        curr_stream[0] = sys.stdin
        if global_verbose_mode:
            print("    ... prep_stream() set FS_IN to stdin")

    if curr_stream[1] is None:
        curr_stream[1] = sys.stdout
        if global_verbose_mode:
            print("    ... prep_stream() set FS_STD to stdout")

    if curr_stream[2] is None:
        curr_stream[2] = sys.stderr
        if global_verbose_mode:
            print("    ... prep_stream() set FS_ERR to stderr")



# Additional code:
# You would need to define global_verbose_mode and atexit, as they are not included in the provided code.

# Example usage:
if __name__ == "__main__":
    output_prefix_enable()
    print("This is a test message.")
    output_redirect("output", "output.txt")
    print("This message is redirected to output.txt.")
