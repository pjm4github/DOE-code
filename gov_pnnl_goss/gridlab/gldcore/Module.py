import io
import threading
import subprocess
from errno import ENOENT, ENOMEM, ENOEXEC
import os
from typing import Any

from gov_pnnl_goss.gridlab.gldcore import Property
from gov_pnnl_goss.gridlab.gldcore.Class import Class
from gov_pnnl_goss.gridlab.gldcore.Globals import SUCCESS, SIGINT, global_start_time, global_stop_time
from gov_pnnl_goss.gridlab.gldcore.Output import output_debug, output_message, output_error, output_verbose, \
    output_fatal, output_warning

from gridlab.gldcore import Load, Globals
from gridlab.gldcore.Find import Find
from gridlab.gldcore.GridLabD import global_setvar, DLSYM
from gridlab.gldcore.Transform import Transform
from gridlab.gldcore.Version import Version

MAGIC = 0x012BB0B9
lock_count = 0
lock_spin = 0

malloc_lock = threading.Lock()


cc_verbose = 0
cc_debug = 0
cc_clean = 0
cc_keepwork = 0
#
# class MODULE:
#     def __init__(self, hLib, id, name, oclass, major, minor, getvar, setvar, import_file, export_file, check,
#                  deltadesired, preupdate, interupdate, deltaClockUpdate, postupdate, clockupdate, cmdargs,
#                  kmldump, test, subload, globals, term, stream, next):
#         self.hLib = hLib
#         self.id = id
#         self.name = name
#         self.oclass = oclass
#         self.major = major
#         self.minor = minor
#         self.getvar = getvar
#         self.setvar = setvar
#         self.import_file = import_file
#         self.export_file = export_file
#         self.check = check
#         self.deltadesired = deltadesired
#         self.preupdate = preupdate
#         self.interupdate = interupdate
#         self.deltaClockUpdate = deltaClockUpdate
#         self.postupdate = postupdate
#         self.clockupdate = clockupdate
#         self.cmdargs = cmdargs
#         self.kmldump = kmldump
#         self.test = test
#         self.subload = subload
#         self.globals = globals
#         self.term = term
#         self.stream = stream
#         self.next = next

# # Function prototypes can be represented as standalone functions in Python.
# def module_get_exe_path(buf, len):
#     pass  # Implement functionality
#
# def module_get_path(buf, len, mod):
#     pass  # Implement functionality
#
# def module_find(module_name):
#     pass  # Implement functionality
#
# # ... and so on for other function prototypes
#
# # For simplicity, I've represented function pointers as callable attributes in the class.
# # In a real implementation, you would provide the actual callable functions.


#
procs = []  # processor map
n_procs = 0  # number of processors in map

MAPNAME = "gridlabd-pmap-3" # TODO: change the pmap number each time the structure changes */

class GLDPROCINFO:
    lock = None		# field lock */
    pid = None			# process id */
    progress = None		# current simtime */
    starttime = None		# sim starttime */
    stoptime = None		# sim stoptime */
    status = None		# current status */
    model = None			# model name */
    start = None			# wall time of start */


process_map = GLDPROCINFO() # global process map */

class MYPROCINFO:
    n_procs= 0  # number of processors used by this process */
    list = []  # list of processors assigned to this process */

my_proc = MYPROCINFO() # processors assigned to this process */
PROCERR = -1


class ExternalFunction:
    def __init__(self):
        self.fname = ""
        self.libname=""
        self.lib = None
        self.call = None
        self.next = None

external_function_list = ExternalFunction()


def get_exe_path(buf, length, mod):
    rv = 0
    i = 0
    if buf is None:
        return 0
    if length < 1:
        return 0
    if mod is None:
        pass
    else:
        pass
    return rv


def free_args(args):
    n = 0
    while n < args.n:
        del args.arg[n]
        n += 1
    del args.arg
    del args


def is_defunct(pid):
    if pid != 0:
        return os.kill(pid, 0) == -1
    else:
        return False


def dlload_error(filename):
    error = "unknown error"
    output_debug(f"{filename}: {error} (LD_LIBRARY_PATH={os.getenv('LD_LIBRARY_PATH')})")


def file_modtime(file):
    try:
        file_stats = os.stat(file)
        return file_stats.st_mtime
    except:
        return 0


def execf(format_str, *args):
    global global_verbose_mode
    command = format_str % args
    if cc_verbose or global_verbose_mode:
        output_message(command)
    else:
        output_debug("command: %s" % command)
    rc = subprocess.call(command, shell=True)
    output_debug("return code=%d" % rc)
    return rc


def DLLOAD(tpath):
    pass


def LIBINIT(param):
    pass


class Module:
    def __init__(self, *args: Any, **kw: Any):
        super().__init__(*args, **kw)
        self.hLib = None
        self.id: int = 0
        self.name: str = ""
        self.oclass: Class = Class()
        self.major: int = 0
        self.minor: int = 0
        self.getvar = None
        self.setvar = None
        self.import_file = None
        self.export_file = None
        self.check = None
        self.deltadesired = None
        self.preupdate = None
        self.interupdate = None
        self.deltaClockUpdate = None
        self.deltadesired = None # a parameter deltadesired
        self.postupdate = None
        self.clockupdate = None
        self.cmdargs = None
        self.kmldump = None
        self.test = None
        self.subload = None
        self.globals = None
        self.term = None
        self.stream = io.BytesIO()
        self.next = None
        self.callbacks = SCallbacks()
        self.module_count = 0
        self.first_module: Module = None
        self.last_module: Module = None
        self.errno = 0

    def module_callbacks(self, ):
        return self.callbacks

    def module_check(self, mod):
        if mod.check is None:
            return 0
        return mod.check() if callable(mod.check) else 0

    def module_check_all(self, ):
        mod = self.first_module
        count = 0
        while mod is not None:
            count += self.module_check(mod)
            mod = mod.next
        return count

    def module_cmdargs(self, argc, argv):
        mod = self.first_module
        while mod is not None:
            if mod is not None and mod.cmdargs is not None:
                return mod.cmdargs(argc, argv)
            mod = mod.next
        return 0

    def module_depends(self, name, major, minor, build):
        mod = self.first_module
        while mod is not None:
            if mod.name == name:
                if major > 0 and mod.major > 0:
                    if mod.major == major and mod.minor >= minor:
                        return 1
                    else:
                        return 0
                else:
                    return 1
            mod = mod.next
        return self.module_load(self, name, 0, None) is not None

    def module_dumpall(self, ):
        mod = self.first_module
        count = 0
        while mod is not None:
            if mod.export_file is not None:
                count += self.module_save(mod, None)
            mod = mod.next
        return count

    def module_export(self, mod, filename):
        if mod.export_file is None:
            self.errno = ENOENT
            return 0
        return mod.export_file(filename)

    def module_find(self, modname):
        mod = None
        mod = self.first_module
        while mod is not None:
            if mod.name == modname:
                break
            mod = mod.next
        return mod

    def module_find_transform_function(self, transform_function):
        global external_function_list
        item = external_function_list
        while item is not None:
            if item.call == self.function:
                return item.fname
            item = item.next
        errno = ENOENT
        return None

    def module_free(self, ptr):
        malloc_lock.acquire()
        del ptr
        malloc_lock.release()

    def module_get_exe_path(self, buf, length):
        return get_exe_path(buf, length, None)

    def module_get_first(self, ):
        return self.first_module

    def module_get_next(self, module):
        return module.next

    def module_get_path(self, buf, length, mod):
        return get_exe_path(buf, length, mod.h_lib)

    def module_get_transform_function(self, function):
        global external_function_list
        item = external_function_list
        while item is not None:
            if item.fname == function:
                item.call = Transform.TRANSFORMFUNCTION()
                return item.call
            item = item.next
        self.errno = ENOENT
        return None

    def module_getcount(self, ):
        return self.module_count

    def module_import(self, mod, filename):
        if mod.import_file is None:
            errno = ENOENT
            return 0
        return mod.import_file(filename)

    def module_list(self):
        pass

    def module_load(self, file, argc, argv):
        mod = self.module_find(file)
        buffer = ""
        isforeign = False
        pathname = ""
        from_char, to_char = '\\', '/'

        if self.callbacks.magic != MAGIC:
            output_fatal("callback function table alignment error (magic number position mismatch)")
            return None

        if mod is not None:
            output_verbose(f"{__file__}(): module '{file}' already loaded")
            return mod
        else:
            output_verbose(f"{__file__}(): module '{file}' not yet loaded")

        buffer = file.encode('utf-8')
        fmod, modname = buffer.split("::")  # This splits the buffer by "::" and assigns the first result to fmod
        if fmod is not None and fmod != file.encode('utf-8'):
            parent_mod = self.module_find(fmod)
            if parent_mod is None:
                parent_mod = self.module_load(fmod, 0, None)
            previous = Class.class_get_last_class()
            if parent_mod is not None and parent_mod.subload is not None:
                if self.module_find(fmod) is None:
                    self.module_load(fmod, 0, None)
                child_mod = parent_mod.subload(modname, mod, self.previous if self.previous else None, argc, argv)
                if child_mod is None:
                    # Failure
                    output_error(f"module_load(file='{fmod}::{modname}'): subload failed")
                    # TROUBLESHOOT
                    # A module is unable to load a submodule require for operation.
                    # Check that the indicated submodule is installed and try again.
                    #
                    return None
                if mod is not None:
                    # if we want to register another module
                    self.last_module.next = mod
                    self.last_module = mod
                    mod.oclass = previous.next if previous else Class.class_get_first_class()
                return self.last_module
            else:
                fmap = [
                    {"name": b"matlab", "loader": None},
                    {"name": b"java", "loader": Load.load_java_module},
                    {"name": b"python", "loader": Load.load_python_module},
                    {"name": None, "loader": None},
                ]
                p = None
                for p in fmap:
                    if p["name"] == fmod:
                        isforeign = True
                        if p["loader"] is not None:
                            return p["loader"](modname, argc, argv)
                        args = [modname]
                        argv = args
                        argc = 1
                        file = buffer
                        break
                if p is None:
                    output_error(
                        f"module_load(file='{file}',...): foreign module type {fmod.decode('utf-8')} not recognized or supported")
                    return None
        #  create a new module entry
        mod = Module()
        if mod is None:
            output_verbose(f"{__file__}(): module '{file}' memory allocation failed")
            self.errno = ENOMEM
            return None
        else:
            output_verbose(f"{__file__}(): module '{file}' memory allocated")
        DLEXT = ".dll"
        pathname.value = f"{file.decode('utf-8')}{DLEXT}".encode('utf-8')
        tpath = ""
        if Find.find_file(pathname.value, None, os.X_OK | os.R_OK, tpath, 0) is None:
            output_verbose(f"unable to locate {pathname.value.decode('utf-8')} in GLPATH, using library loader instead")
            tpath.value = pathname.value
        else:
            if tpath.value[0] != b'/'[0]:
                buf = os.stat(tpath.value)
                if buf is not None:
                    buffer.value = f"./{tpath.value.decode('utf-8')}".encode('utf-8')
                    tpath.value = buffer.value
            output_verbose(f"full path to library '{file.decode('utf-8')}' is '{tpath.value.decode('utf-8')}'")

        for i in range(len(tpath.value)):
            if tpath.value[i] == from_char:
                tpath[i] = to_char

        hLib = DLLOAD(tpath)
        if hLib is None:
            output_error(f"{__file__}(): module '{file}' load failed - ")
            output_debug(f"{__file__}(): path to module is '{tpath.value.decode('utf-8')}'")
            dlload_error(pathname.value)
            errno = ENOENT
            mod = None
            return None
        else:
            output_verbose(f"{__file__}(): module '{file}' loaded ok")

        init = LIBINIT(DLSYM(hLib, b"init"))
        if init is None:
            output_error(f"{__file__}(): module '{file}' does not export init()")
            dlload_error(pathname.value)
            errno = ENOEXEC
            mod = None
            return None
        else:
            output_verbose(f"{__file__}(): module '{file}' exports init()")

        mod.hLib = hLib
        pMajor = DLSYM(hLib, b"gld_major")
        pMinor = DLSYM(hLib, b"gld_minor")
        mod.major = pMajor.contents.value if pMajor is not None else 0
        mod.minor = pMinor.contents.value if pMinor is not None else 0
        mod.import_file = DLSYM(hLib, b"import_file")
        mod.export_file = DLSYM(hLib, b"export_file")
        mod.setvar = DLSYM(hLib, b"setvar")
        mod.getvar = DLSYM(hLib, b"getvar")
        mod.check = DLSYM(hLib, b"check")
        mod.deltadesired = DLSYM(hLib, b"deltamode_desired")

        mod.preupdate = DLSYM(hLib, b"preupdate")
        mod.interupdate = DLSYM(hLib, b"interupdate")
        mod.deltaClockUpdate = DLSYM(hLib, b"deltaClockUpdate")
        mod.postupdate = DLSYM(hLib, b"postupdate")
        mod.clockupdate = DLSYM(hLib, b"clock_update")
        mod.cmdargs = DLSYM(hLib, b"cmdargs")
        mod.kmldump = DLSYM(hLib, b"kmldump")
        mod.subload = DLSYM(hLib, b"subload")
        mod.test = DLSYM(hLib, b"test")
        mod.stream = DLSYM(hLib, b"stream")
        mod.globals = None
        mod.term = DLSYM(hLib, b"term")

        mod.name = file.encode('utf-8')
        mod.next = None

        if mod.major != Version.REV_MAJOR or mod.minor != Version.REV_MINOR:
            output_error(f"Module version {mod.major}.{mod.minor} mismatch from core version {Version.REV_MAJOR}.{Version.REV_MINOR}")
            return None

        errno = 0
        mod.oclass = init(self.callbacks, mod, argc, argv)
        if mod.oclass is None and errno != 0:
            return None

        for c in mod.oclass:
            fname = ""

            map = [
                {"func": c.create, "name": "create", "optional": False},
                {"func": c.init, "name": "init", "optional": True},
                {"func": c.precommit, "name": "precommit", "optional": True},
                {"func": c.sync, "name": "sync", "optional": True},
                {"func": c.commit, "name": "commit", "optional": True},
                {"func": c.finalize, "name": "finalize", "optional": True},
                {"func": c.notify, "name": "notify", "optional": True},
                {"func": c.isa, "name": "isa", "optional": True},
                {"func": c.plc, "name": "plc", "optional": True},
                {"func": c.recalc, "name": "recalc", "optional": True},
                {"func": c.update, "name": "update", "optional": True},
                {"func": c.heartbeat, "name": "heartbeat", "optional": True},
            ]

            lib_name = Find.find_library("your_library_name")  # Replace "your_library_name" with the actual library
            if lib_name:
                hLib = lib_name
            else:
                raise Exception("Library not found.")

            for item in map:
                fname = f"{item['name']}_{fmod if isforeign else c.name}"
                try:
                    func_addr = getattr(hLib, fname)
                    item['func'] = func_addr
                    if not item['optional']:
                        output_verbose(f"{__file__}(): module '{file}' intrinsic {fname} found")
                except AttributeError:
                    if not item['optional']:
                        output_fatal("intrinsic %s is not defined in class %s", fname, file)
                        return None

            for m in map:
                fname = f"{m[1]}_{fmod.decode('utf-8') if isforeign else c.name.decode('utf-8')}".encode('utf-8')
                m[0] = DLSYM(hLib, fname)
                if m[0] is None and not m[2]:
                    output_fatal(
                        f"intrinsic {fname.decode('utf-8')} is not defined in class {file.decode('utf-8')}")
                    errno = Globals.EINVAL
                    return None
                elif not m[2]:
                    output_verbose(
                        f"{__file__}(): module '{file}' intrinsic {fname.decode('utf-8')} found")

        if self.first_module is None:
            mod.id = 0
            first_module = mod
        else:
            self.last_module.next = mod
            mod.id = self.last_module.id + 1
        last_module = mod
        self.module_count += 1

        if mod.stream is not None:
            self.stream_register(mod.stream)

        return last_module

    def module_malloc(self, size):
        malloc_lock.acquire()
        ptr = None
        malloc_lock.release()
        return ptr

    def module_save(self, mod, filename):
        if mod.export_file is None:
            self.errno = ENOENT
            return 0
        return mod.export_file(filename)

    def module_setvar(self, mod, var_name, value):
        mod_var_name = "{}::{}".format(mod.name, var_name)
        return global_setvar(mod_var_name, value) == SUCCESS

    def module_term_all(self, ):
        mod = self.first_module
        while mod is not None:
            if mod.term:
                mod.term()
            mod = mod.next


class SCallbacks:
    def __init__(self):
        self.global_clock = None
        self.global_delta_curr_clock = None
        self.global_exit_code = None
        self.global_stoptime = None
        self.output_verbose = None
        self.output_message = None
        self.output_warning = None
        self.output_error = None
        self.output_fatal = None
        self.output_debug = None
        self.output_test = None
        self.register_class = None
        self.create_single = None
        self.create_array = None
        self.create_foreign = None
        self.define_map = None
        self.loadmethod = None
        self.class_getfirst = None
        self.class_getname = None
        self.class_add_extended_property = None
        self.function_define = None
        self.function_get = None
        self.define_enumeration_member = None
        self.define_set_member = None
        self.object_get_first = None
        self.object_set_dependent = None
        self.object_set_parent = None
        self.object_set_rank = None
        self.object_get_property = None
        self.object_set_value_by_addr = None
        self.object_get_value_by_addr = None
        self.object_set_value_by_name = None
        self.object_get_value_by_name = None
        self.object_get_reference = None
        self.object_get_unit = None
        self.object_get_addr = None



class Sched:
    def __init__(self):
        pass

    def sched_clear(self,void):
        pass

    def sched_finish(self, ):
        if my_proc is None or my_proc.list is None:
            return
        for t in range(my_proc.n_procs):
            n = my_proc.list[t]
            n.sched_lock()
            process_map[n].status = Globals.MLS_DONE
            n.sched_unlock()

    def sched_controller(self,void):
        pass

    def sched_get_cpuid(self, n):
        if my_proc is None or my_proc.list is None or n >= my_proc.n_procs:
            return PROCERR
        return my_proc.list[n]

    def sched_get_procid(self, ):
        cpuid = self.sched_get_cpuid(0)
        if PROCERR == cpuid:
            output_warning("proc_map %x, myproc not assigned", process_map, self.sched_get_cpuid(0))
            return 0
        output_debug("proc_map %x, myproc %ui", process_map, self.sched_get_cpuid(0))
        return process_map[cpuid].pid

    def sched_init(self, readonly: int):
        pass

    def sched_lock(self, proc: int) -> None:
        if process_map:
            process_map[proc].lock

    def sched_pkill(self, pid):
        if process_map is not None and process_map[pid].pid != 0:
            os.kill(process_map[pid].pid, SIGINT)

    def sched_print(self, flags: int):
        pass

    def sched_signal(self, sig):
        print("\n*** SIGINT ***\n")
        sched_stop = 1

    def sched_unlock(self, proc):
        if process_map:
            process_map[proc].unlock

    def sched_update(self, clock, status):

        if my_proc is None or my_proc.list is None:
            return
        for t in range(my_proc.n_procs):
            n = my_proc.list[t]
            n.scedule_lock()
            process_map[n].status = status
            process_map[n].progress = clock
            process_map[n].starttime = global_start_time
            process_map[n].stoptime = global_stop_time
            n.scedule_unlock()