import threading
import subprocess
import ctypes
from errno import ENOENT, ENOMEM
import os
from typing import Any

from gov_pnnl_goss.gridlab.gldcore import Property
from gov_pnnl_goss.gridlab.gldcore.Class import Class
from gov_pnnl_goss.gridlab.gldcore.Globals import global_setvar, SUCCESS
from gov_pnnl_goss.gridlab.gldcore.Output import output_debug, output_message, output_error, output_verbose, \
    output_fatal

MAGIC = 0x012BB0B9
lock_count = 0
lock_spin = 0

malloc_lock = threading.Lock()


cc_verbose = 0
cc_debug = 0
cc_clean = 0
cc_keepwork = 0


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


class Module(ctypes.Structure):
    def __init__(self, *args: Any, **kw: Any):
        super().__init__(*args, **kw)
        self.hLib = ctypes.c_void_p()
        self.id = ctypes.c_uint()
        self.name = ctypes.c_char * 1024
        self.oclass = ctypes.POINTER(Class)
        self.major = ctypes.c_ushort()
        self.minor = ctypes.c_ushort()
        self.getvar = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint)
        self.setvar = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)
        self.import_file = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.export_file = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.check = ctypes.CFUNCTYPE(ctypes.c_int)
        self.deltadesired = ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.POINTER(ctypes.c_uint))
        self.preupdate = ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_int64, ctypes.c_uint64)
        self.interupdate = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_int64, ctypes.c_uint64, ctypes.c_ulong, ctypes.c_uint)
        self.deltaClockUpdate = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_double, ctypes.c_ulong, ctypes.c_int)
        self.postupdate = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_int64, ctypes.c_uint64)
        self.clockupdate = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_int64))
        self.cmdargs = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
        self.kmldump = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p), ctypes.POINTER(OBJECT))
        self.test = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p))
        self.subload = ctypes.CFUNCTYPE(ctypes.POINTER(Module), ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(MODULE)), ctypes.POINTER(ctypes.POINTER(CLASS)), ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
        self.globals = ctypes.POINTER(Property)
        self.term = ctypes.CFUNCTYPE(None)
        self.stream = Streamcall
        self.next = ctypes.POINTER(Module)
        self.callbacks - SCallbacks()
        self.module_count = 0
        self.first_module: Module = None
        self.last_module: Module = None
        self.errno = 0

    def get_transform_function(self, function):
        item = external_function_list
        while item is not None:
            if item.fname == function:
                return ctypes.cast(item.call, TRANSFORMFUNCTION())
            item = item.next
        self.errno = ENOENT
        return None

    def module_get_exe_path(self, buf, length):
        return get_exe_path(buf, length, None)

    def module_get_path(self, buf, length, mod):
        return get_exe_path(buf, length, mod.h_lib)

    def module_malloc(self, size):
        malloc_lock.acquire()
        ptr = ctypes.c_void_p(ctypes.windll.kernel32.LocalAlloc(0x40, size))
        malloc_lock.release()
        return ptr

    def module_free(self, ptr):
        malloc_lock.acquire()
        del ptr
        malloc_lock.release()

    def module_callbacks(self, ):
        return self.callbacks

    def module_getcount(self, ):
        return self.module_count

    def module_load(self, file, argc, argv):
        mod = self.module_find(file)
        buffer = ctypes.create_string_buffer(FILENAME_MAX + 1)
        # fmod = None
        isforeign = False
        pathname = ctypes.create_string_buffer(1024)
        tpath = ctypes.create_string_buffer(1024)
        from_char, to_char = '\\', '/'
        # p = None
        # hLib = None
        # init = None
        # pMajor = None
        # pMinor = None
        # previous = None
        # c = None

        if self.callbacks.magic != MAGIC:
            output_fatal("callback function table alignment error (magic number position mismatch)")
            return None

        if mod is not None:
            output_verbose(f"{__file__}({__line__}): module '{file}' already loaded")
            return mod
        else:
            output_verbose(f"{__file__}({__line__}): module '{file}' not yet loaded")

        buffer.value = file.encode('utf-8')
        fmod = strtok(buffer.value, b"::")
        if fmod is not None and fmod != file.encode('utf-8'):
            modname = strtok(None, b"::")
            parent_mod = self.module_find(fmod)
            if parent_mod is None:
                parent_mod = self.module_load(fmod, 0, None)
            previous = Class.class_get_last_class()
            if parent_mod is not None and parent_mod.subload is not None:
                if self.module_find(fmod) is None:
                    self.module_load(fmod, 0, None)
                child_mod = parent_mod.subload(modname, mod, ctypes.byref(previous) if previous else None, argc, argv)
                if child_mod is None:
                    output_error(f"module_load(file='{fmod}::{modname}'): subload failed")
                    return None
                if mod is not None:
                    self.last_module.next = mod
                    self.last_module = mod
                    mod.oclass = previous.next if previous else Class.class_get_first_class()
                return self.last_module
            else:
                fmap = [
                    {"name": b"matlab", "loader": None},
                    {"name": b"java", "loader": load_java_module},
                    {"name": b"python", "loader": load_python_module},
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
                        file = buffer.value
                        break
                if p is None:
                    output_error(
                        f"module_load(file='{file}',...): foreign module type {fmod.decode('utf-8')} not recognized or supported")
                    return None

        mod = Module()
        if mod is None:
            output_verbose(f"{__file__}({__line__}): module '{file}' memory allocation failed")
            self.errno = ENOMEM
            return None
        else:
            output_verbose(f"{__file__}({__line__}): module '{file}' memory allocated")

        pathname.value = f"{file.decode('utf-8')}{DLEXT}".encode('utf-8')

        if self.find_file(pathname.value, None, X_OK | R_OK, tpath, sizeof(tpath)) is None:
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

        hLib = DLLOAD(tpath.value)
        if hLib is None:
            output_error(f"{__file__}({__line__}): module '{file}' load failed - {dlerror().decode('utf-8')}")
            output_debug(f"{__file__}({__line__}): path to module is '{tpath.value.decode('utf-8')}'")
            dlload_error(pathname.value)
            errno = ENOENT
            free(mod)
            mod = None
            return None
        else:
            output_verbose(f"{__file__}({__line__}): module '{file}' loaded ok")

        init = LIBINIT(DLSYM(hLib, b"init"))
        if init is None:
            output_error(f"{__file__}({__line__}): module '{file}' does not export init()")
            dlload_error(pathname.value)
            errno = ENOEXEC
            free(mod)
            mod = None
            return None
        else:
            output_verbose(f"{__file__}({__line__}): module '{file}' exports init()")

        mod.hLib = hLib
        pMajor = ctypes.cast(DLSYM(hLib, b"gld_major"), ctypes.POINTER(ctypes.c_int))
        pMinor = ctypes.cast(DLSYM(hLib, b"gld_minor"), ctypes.POINTER(ctypes.c_int))
        mod.major = pMajor.contents.value if pMajor is not None else 0
        mod.minor = pMinor.contents.value if pMinor is not None else 0
        mod.import_file = ctypes.cast(DLSYM(hLib, b"import_file"), ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p))
        mod.export_file = ctypes.cast(DLSYM(hLib, b"export_file"), ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p))
        mod.setvar = ctypes.cast(DLSYM(hLib, b"setvar"),
                                 ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p))
        mod.getvar = ctypes.cast(DLSYM(hLib, b"getvar"),
                                 ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint))
        mod.check = ctypes.cast(DLSYM(hLib, b"check"), ctypes.CFUNCTYPE(ctypes.c_int))
        mod.deltadesired = ctypes.cast(DLSYM(hLib, b"deltamode_desired"),
                                       ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.POINTER(DELTAMODEFLAGS)))
        mod.preupdate = ctypes.cast(DLSYM(hLib, b"preupdate"),
                                    ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_int64, ctypes.c_uint64))
        mod.interupdate = ctypes.cast(DLSYM(hLib, b"interupdate"),
                                      ctypes.CFUNCTYPE(SIMULATIONMODE, ctypes.c_void_p, ctypes.c_int64, ctypes.c_uint64,
                                                       ctypes.c_ulong, ctypes.c_uint))
        mod.deltaClockUpdate = ctypes.cast(DLSYM(hLib, b"deltaClockUpdate"),
                                           ctypes.CFUNCTYPE(SIMULATIONMODE, ctypes.c_void_p, ctypes.c_double,
                                                            ctypes.c_ulong, SIMULATIONMODE))
        mod.postupdate = ctypes.cast(DLSYM(hLib, b"postupdate"),
                                     ctypes.CFUNCTYPE(STATUS, ctypes.c_void_p, ctypes.c_int64, ctypes.c_uint64))
        mod.clockupdate = ctypes.cast(DLSYM(hLib, b"clock_update"),
                                      ctypes.CFUNCTYPE(TIMESTAMP, ctypes.POINTER(TIMESTAMP)))
        mod.cmdargs = ctypes.cast(DLSYM(hLib, b"cmdargs"),
                                  ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)))
        mod.kmldump = ctypes.cast(DLSYM(hLib, b"kmldump"),
                                  ctypes.CFUNCTYPE(ctypes.c_int, ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p),
                                                   ctypes.POINTER(OBJECT)))
        mod.subload = ctypes.cast(DLSYM(hLib, b"subload"), ctypes.CFUNCTYPE(ctypes.POINTER(MODULE), ctypes.c_char_p,
                                                                            ctypes.POINTER(ctypes.POINTER(MODULE)),
                                                                            ctypes.POINTER(ctypes.POINTER(CLASS)),
                                                                            ctypes.c_int, ctypes.POINTER(
                ctypes.POINTER(ctypes.c_char_p))))
        mod.test = ctypes.cast(DLSYM(hLib, b"test"),
                               ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)))
        mod.stream = ctypes.cast(DLSYM(hLib, b"stream"), STREAMCALL)
        mod.globals = None
        mod.term = ctypes.cast(DLSYM(hLib, b"term"), ctypes.CFUNCTYPE(None))

        mod.name = file.encode('utf-8')
        mod.next = None

        if mod.major != REV_MAJOR or mod.minor != REV_MINOR:
            output_error(f"Module version {mod.major}.{mod.minor} mismatch from core version {REV_MAJOR}.{REV_MINOR}")
            return None

        errno = 0
        mod.oclass = init(self.callbacks, ctypes.byref(mod), argc, argv)
        if mod.oclass is None and errno != 0:
            return None

        for c in mod.oclass:
            fname = ctypes.create_string_buffer(1024)
            map = [
                (ctypes.byref(c.create), b"create", False),
                (ctypes.byref(c.init), b"init", True),
                (ctypes.byref(c.precommit), b"precommit", True),
                (ctypes.byref(c.sync), b"sync", True),
                (ctypes.byref(c.commit), b"commit", True),
                (ctypes.byref(c.finalize), b"finalize", True),
                (ctypes.byref(c.notify), b"notify", True),
                (ctypes.byref(c.isa), b"isa", True),
                (ctypes.byref(c.plc), b"plc", True),
                (ctypes.byref(c.recalc), b"recalc", True),
                (ctypes.byref(c.update), b"update", True),
                (ctypes.byref(c.heartbeat), b"heartbeat", True),
            ]
            for m in map:
                fname.value = f"{m[1]}_{fmod.decode('utf-8') if isforeign else c.name.decode('utf-8')}".encode('utf-8')
                m[0] = ctypes.cast(DLSYM(hLib, fname.value), ctypes.CFUNCTYPE(None))
                if m[0] is None and not m[2]:
                    output_fatal(
                        f"intrinsic {fname.value.decode('utf-8')} is not defined in class {file.decode('utf-8')}")
                    errno = EINVAL
                    return None
                elif not m[2]:
                    output_verbose(
                        f"{__file__}({__line__}): module '{file}' intrinsic {fname.value.decode('utf-8')} found")

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

    def _module_list(self):
        pass

    def module_list(self):
        pass


    def module_setvar(self, mod, var_name, value):
        mod_var_name = "{}::{}".format(mod.name, var_name)
        return global_setvar(mod_var_name, value) == SUCCESS


    def module_get_first(self, ):
        return self.first_module


    def module_find(self, modname):
        mod = None
        mod = self.first_module
        while mod is not None:
            if mod.name == modname:
                break
            mod = mod.next
        return mod


    def module_import(self, mod, filename):
        if mod.import_file is None:
            errno = ENOENT
            return 0
        return mod.import_file(filename)


    def module_export(self, mod, filename):
        if mod.export_file is None:
            self.errno = ENOENT
            return 0
        return mod.export_file(filename)

    def module_save(self, mod, filename):
        if mod.export_file is None:
            self.errno = ENOENT
            return 0
        return mod.export_file(filename)

    def module_dumpall(self, ):
        mod = self.first_module
        count = 0
        while mod is not None:
            if mod.export_file is not None:
                count += self.module_save(mod, None)
            mod = mod.next
        return count

    def module_check_all(self, ):
        mod = self.first_module
        count = 0
        while mod is not None:
            count += self.module_check(mod)
            mod = mod.next
        return count

    def module_check(self, mod):
        if mod.check is None:
            return 0
        return mod.check() if callable(mod.check) else 0

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

    def module_get_next(self, module):
        return module.next

    def module_term_all(self, ):
        mod = self.first_module
        while mod is not None:
            if mod.term:
                mod.term()
            mod = mod.next

    def module_find_transform_function(self, transform_function):
        item = external_function_list
        while item is not None:
            if item.call == self.function:
                return item.fname
            item = item.next
        errno = ENOENT
        return None


class SCallbacks(ctypes.Structure):
    def __init__(self):
        self.global_clock = ctypes.POINTER(ctypes.c_int64)
        self.global_delta_curr_clock = ctypes.POINTER(ctypes.c_int64)
        self.global_exit_code = ctypes.POINTER(ctypes.c_int)
        self.global_stoptime = ctypes.POINTER(TIMESTAMP)
        self.output_verbose = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.output_message = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.output_warning = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.output_error = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.output_fatal = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.output_debug = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.output_test = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.register_class = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(CLASS))
        self.create_single = ctypes.CFUNCTYPE(ctypes.POINTER(OBJECT), ctypes.POINTER(CLASS), ctypes.POINTER(ctypes.c_char_p))
        self.create_array = ctypes.CFUNCTYPE(ctypes.POINTER(OBJECT), ctypes.POINTER(CLASS), ctypes.c_uint)
        self.create_foreign = ctypes.CFUNCTYPE(ctypes.POINTER(OBJECT), ctypes.POINTER(CLASS), ctypes.POINTER(ctypes.c_char_p))
        self.define_map = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(CLASS), ctypes.c_char_p)
        self.loadmethod = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(CLASS), ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(OBJECT)))
        self.class_getfirst = ctypes.CFUNCTYPE(ctypes.POINTER(CLASS))
        self.class_getname = ctypes.CFUNCTYPE(ctypes.POINTER(CLASS), ctypes.c_char_p)
        self.class_add_extended_property = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(CLASS), ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
        self.function_define = ctypes.CFUNCTYPE(ctypes.POINTER(FUNCTION), ctypes.POINTER(CLASS), ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p))
        self.function_get = ctypes.CFUNCTYPE(ctypes.POINTER(FUNCTION), ctypes.POINTER(CLASS), ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)))
        self.define_enumeration_member = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(CLASS), ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
        self.define_set_member = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(CLASS), ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int)
        self.object_get_first = ctypes.CFUNCTYPE(ctypes.POINTER(OBJECT))
        self.object_set_dependent = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(OBJECT), ctypes.POINTER(OBJECT))
        self.object_set_parent = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(OBJECT), ctypes.POINTER(OBJECT))
        self.object_set_rank = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(OBJECT), ctypes.c_int)
        self.object_get_property = ctypes.CFUNCTYPE(ctypes.POINTER(PROPERTY), ctypes.POINTER(OBJECT), ctypes.c_char_p)
        self.object_set_value_by_addr = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(OBJECT), ctypes.POINTER(PROPERTY), ctypes.c_void_p, ctypes.c_int)
        self.object_get_value_by_addr = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(OBJECT), ctypes.POINTER(PROPERTY), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        self.object_set_value_by_name = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(OBJECT), ctypes.POINTER(PROPERTY), ctypes.c_char_p, ctypes.c_int)
        self.object_get_value_by_name = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(OBJECT), ctypes.POINTER(PROPERTY), ctypes.c_char_p, ctypes.POINTER(ctypes.c_int))
        self.object_get_reference = ctypes.CFUNCTYPE(ctypes.POINTER(OBJECT), ctypes.POINTER(OBJECT), ctypes.POINTER(OBJECT), ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(OBJECT)))
        self.object_get_unit = ctypes.CFUNCTYPE(ctypes.POINTER(UNIT), ctypes.POINTER(OBJECT), ctypes.c_char_p)
        self.object_get_addr = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(OBJECT), ctypes.POINTER(ctypes.c_void_p



class Sched:
    def __init__(self):
        pass

    def sched_get_cpuid(self, n):
        if my_proc is None or my_proc.list is None or n >= my_proc.n_procs:
            return PROCERR
        return my_proc.list[n]

    def sched_get_procid(self, ):
        cpuid = sched_get_cpuid(0)
        if PROCERR == cpuid:
            output_warning("proc_map %x, myproc not assigned", process_map, sched_get_cpuid(0))
            return 0
        output_debug("proc_map %x, myproc %ui", process_map, sched_get_cpuid(0))
        return process_map[cpuid].pid

    def sched_lock(self, proc: int) -> None:
        if process_map:
            wlock(process_map[proc].lock)

    def sched_unlock(self, proc):
        if process_map:
            wunlock(process_map[proc].lock)

    def sched_update(self, clock, status):
        if my_proc is None or my_proc.list is None:
            return
        for t in range(my_proc.n_procs):
            n = my_proc.list[t]
            sched_lock(n)
            process_map[n].status = status
            process_map[n].progress = clock
            process_map[n].starttime = global_starttime
            process_map[n].stoptime = global_stoptime
            sched_unlock(n)

    def sched_finish(self, ):
        if my_proc is None or my_proc.list is None:
            return
        for t in range(my_proc.n_procs):
            n = my_proc.list[t]
            sched_lock(n)
            process_map[n].status = MLS_DONE
            sched_unlock(n)

    def sched_pkill(self, pid):
        if process_map is not None and process_map[pid].pid != 0:
            os.kill(process_map[pid].pid, signal.SIGINT)

    def sched_signal(self, sig):
        print("\n*** SIGINT ***\n")
        sched_stop = 1