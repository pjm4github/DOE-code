import json

from gov_pnnl_goss.gridlab.gldcore.Class import DynamicClass
from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyFlags, PropertyType, PropertyAccess
#
from gridlab.gldcore.Property import PropertyValue

CMDOK = -1
CMDERR = -2



# def output_fatal(message):
#     print(f"FATAL: {message}")
#
# def output_redirect(stream, destination):
#     if destination is None:
#         try:
#             sys.stdout = open(os.devnull, "w")
#             sys.stderr = open(os.devnull, "w")
#         except Exception as e:
#             return None
#     else:
#         try:
#             if stream == "output":
#                 sys.stdout = open(destination, "w")
#             elif stream == "error":
#                 sys.stderr = open(destination, "w")
#             elif stream == "warning":
#                 # Redirect warnings to a file (you can customize this)
#                 pass
#             elif stream == "debug":
#                 # Redirect debug messages to a file (you can customize this)
#                 pass
#             elif stream == "verbose":
#                 # Redirect verbose messages to a file (you can customize this)
#                 pass
#             elif stream == "profile":
#                 # Redirect profile messages to a file (you can customize this)
#                 pass
#             elif stream == "progress":
#                 # Redirect progress messages to a file (you can customize this)
#                 pass
#             else:
#                 return None
#         except Exception as e:
#             return None
#
#     return True


loader_time = 0



# def output_error(message):
#     print(f"ERROR: {message}")
#
# def output_warning(message):
#     print(f"WARNING: {message}")
#
# def output_raw(message):
#     print(message)
# #
# # def output_redirect(stream, destination):
# #     # Replace this with actual redirection logic
# #     pass
#
#
# def object_init(object):
#     # Replace this with actual object initialization logic
#     pass
#
#
# def object_save(buffer, object):
#     # Replace this with actual object saving logic
#     pass
#
# def generate_classdef(modname, classname, owner_class, obj):
#     buffer = f"struct('module','{modname}','class','{classname}'"
#     temp = ""
#     for prop in owner_class.pmap:
#         if prop.owner_class != owner_class or '.' in prop.name:
#             continue  # Skip properties that are not part of the class or are structures
#         from gridlab.gldcore.Object import Object
#         value = Object.object_property_to_string(obj, prop.name)
#         if value is not None:
#             buffer += f",...\n\t'{prop.name}','{value}'"
#     buffer += ");\n"
#     return buffer
#
#
# def load_module_list(fd, test_mod_num):
#     mod_test = "mod_test{}={}"
#     line = fd.readline().strip()
#
#     while line:
#         print(f"Line: {line}")
#         mod_test_formatted = mod_test.format(test_mod_num[0], line)
#
#         if not global_setvar(mod_test_formatted):
#             print("Unable to store module name")
#             """
#             TROUBLESHOOT
#             This error is caused by a failure to set up a module test, which
#             requires that the name module being tested be stored in a global
#             variable called mod_test<num>.  The root cause will be identified
#             by determining what error in the global_setvar call occurred.
#             """
#             return "FAILED"
#
#         test_mod_num[0] += 1
#         line = fd.readline().strip()
#
#     return "SUCCESS"
#
class Pntree:
    def __init__(self, name, owner_class):
        self.name = name
        self.owner_class = owner_class
        self.left = None
        self.right = None
#
#
# def modhelp_alpha(ctree, owner_class):
#     targ = ctree
#
#     cmpval = owner_class.name.find(targ.name)
#
#     if cmpval == 0:
#         # print("ERROR", owner_class.name)  # exception?
#         return
#     if cmpval < 0:  # class < root ~ go left
#         if targ.left is None:
#             targ.left = Pntree(owner_class.name, owner_class)
#         else:  # non-null, follow upwards
#             modhelp_alpha(targ.left, owner_class)
#     else:
#         if targ.right is None:
#             targ.right = Pntree(owner_class.name, owner_class)
#         else:
#             modhelp_alpha(targ.right, owner_class)
#
#
# # Example usage:
# # ctree = Pntree("root", some_class)
# # modhelp_alpha(ctree, another_class)
#
#
#

#
#

#
# def jprint_class(owner_class, module):
#     jprint_class_d(owner_class, 0, module)
#
#
# def jprint_modhelp_tree(ctree, module):
#     if ctree.left:
#         jprint_modhelp_tree(ctree.left, module)
#         ctree.left = None  # Set left child to None to free memory
#
#     jprint_class(ctree.owner_class, module)
#
#     if ctree.right:
#         jprint_modhelp_tree(ctree.right, module)
#         ctree.right = None  # Set right child to None to free memory
#
#
# # Example usage:
# # owner_class = ...  # Replace with your DynamicClass instance
# # module = {}  # Initialize an empty dictionary
# # jprint_class(owner_class, module)
# # print(json.dumps(module, indent=4))  # Pretty print the JSON data
#
#
# def print_class_d(owner_class, tabdepth):
#     tabs = '\t' * tabdepth
#
#     print(f"{tabs}class {owner_class.name} {{")
#
#     if owner_class.parent:
#         print(f"{tabs}\tparent {owner_class.parent.name};")
#         print_class_d(owner_class.parent, tabdepth + 1)
#
#     for func in owner_class.fmap:
#         if func.owner_class != owner_class:
#             break
#         print(f"{tabs}\tfunction {func.name}();")
#
#     for prop in owner_class.pmap:
#         if prop.owner_class != owner_class:
#             break
#         propname = DynamicClass.class_get_property_typename(prop.global_property_types)
#         if propname:
#             if prop.access & PropertyAccess.PA_HIDDEN == PropertyAccess.PA_HIDDEN:
#                 continue
#             if prop.unit:
#                 print(f"{tabs}\t{propname} {prop.name}[{prop.unit.name}];")
#             elif prop.global_property_types in [PropertyType.PT_set, PropertyType.PT_enumeration]:
#                 keyword_list = ", ".join([f"{key.name}={key.value}" for key in prop.keywords])
#                 print(f"{tabs}\t{propname} {{{keyword_list}}} {prop.name};")
#             else:
#                 print(f"{tabs}\t{propname} {prop.name};", end="")
#
#             if prop.description:
#                 deprecated_flag = "(DEPRECATED) " if prop.flags & PropertyFlags.PF_DEPRECATED else ""
#                 print(f" // {deprecated_flag}{prop.description}")
#             else:
#                 print()
#
#     print(f"{tabs}}}\n")
#
#
# # Example usage:
# # owner_class = ...  # Replace with your DynamicClass instance
# # print_class_d(owner_class, 0)
#
#
# def print_class(owner_class):
#     print_class_d(owner_class, 0)
#
#
# def print_modhelp_tree(ctree):
#     if ctree.left is not None:
#         print_modhelp_tree(ctree.left)
#         ctree.left = 0
#
#     print_class(ctree.owner_class)
#     if ctree.right is not None:
#         print_modhelp_tree(ctree.right)
#         ctree.right = 0
#
#
# def compare(a, b):
#     return 0 if a.casefold() == b.casefold() else (1 if a.casefold() > b.casefold() else -1)
#
#
# # Example usage:
# # result = compare("abc", "ABC")
# # print(result)
#
#
# class CMDARG:
#     def __init__(self, lopt, sopt, call, args, desc):
#         self.lopt = lopt
#         self.sopt = sopt
#         self.call = call
#         self.args = args
#         self.desc = desc
#
#
# # Example usage:
# # cmdarg = CmdArg("--help", "-h", help_function, "arg1 arg2", "Display help message")
#
#
# # **********************************************************************
# # COMMAND LINE PARSING ROUTINES
# #
# # All cmdline parsing routines must use the prototype int (*)(int,char *[])
# #
# # The return value must be the number of args processed (excluding primary
# # one). A return value of CMDOK indicates that processing must stop immediately
# # and the return status is the current status.  A return value of CMDERR indicates
# # that processing must stop immediately and FAILED status is returned.
# #
#
#
# def no_cmdargs():
#     global global_environment
#     global global_mainloopstate
#     global global_autostartgui
#     global global_browser
#     htmlfile = "gridlabd.htm"
#
#     if global_autostartgui and os.access(htmlfile, os.R_OK):
#         cmd = ""
#
#         # Determine the platform and open the HTML file in a browser
#         if platform.system() == "Windows":
#             if not os.path.isabs(htmlfile):
#                 htmlfile = os.path.join(global_workdir, "gridlabd.htm")
#             output_message("Opening html page:", htmlfile)
#             cmd = f'start {global_browser} file:///{htmlfile}'
#         elif platform.system() == "Darwin":
#             cmd = f'open -a {global_browser} {htmlfile}'
#         else:
#             cmd = f'{global_browser} "{htmlfile}" & ps -p $! >/dev/null'
#
#         output_verbose("Starting browser using command:", cmd)
#
#         if os.system(cmd) != 0:
#             output_error("Unable to start the browser")
#             return CMDERR
#         else:
#             output_verbose("Starting interface")
#             global_environment = "server"
#             global_mainloopstate = MAINLOOPSTATE.MLS_PAUSED
#             return CMDOK
#     else:
#         output_error("Default HTML file 'gridlabd.htm' not found (workdir='{}')".format(global_workdir))
#         return CMDOK
#
#
# # # Example usage:
# # result = no_cmdargs()
# # if result == CMDOK:
# #     print("Success")
# # elif result == CMDERR:
# #     print("Error")
#
#
# def copyright(argc, argv):
#     legal_notice()
#     return 0
#
#
# def warn(argc, argv):
#     global global_warn_mode
#     global_warn_mode = not global_warn_mode
#     return 0
#
#
# def both_stdout(argc, argv):
#     output_both_stdout()
#     return 0
#
#
# def check(argc, argv):
#     global global_runchecks
#     from gridlab.gldcore.Property import property_check
#     if property_check() == FAILED:
#         output_fatal("main_core_property_implementation_failed_size_checks")
#         exit(XC_INIERR)
#     global_runchecks = not global_runchecks
#     return 0
#
#
# def debug(argc, argv):
#     global global_debug_output
#     global_debug_output = not global_debug_output
#     return 0
#
#
# def debugger(argc, argv):
#     global global_debug_mode, global_debug_output
#     global_debug_mode = 1
#     global_debug_output = 1
#     return 0
#
#
# def dump_all(argc, argv):
#     global global_dumpall
#     global_dumpall = not global_dumpall
#     return 0
#
#
# def quiet(argc, argv):
#     global global_quiet_mode
#     global_quiet_mode = not global_quiet_mode
#     return 0
#
#
# def verbose(argc, argv):
#     global global_verbose_mode
#     global_verbose_mode = not global_verbose_mode
#     return 0
#
#
# def _check_version(argc, argv):
#     check_version(0)
#     return 0
#
#
# def profile(argc, argv):
#     global global_profiler
#     global_profiler = not global_profiler
#     return 0
#
#
# def mt_profile(argc, argv):
#     global global_threadcount
#     if argc > 1:
#         global_profiler = 1
#         global_mt_analysis = int(argv[1])
#         argc -= 1
#         argv.pop(0)
#
#         if global_threadcount > 1:
#             print("--mt_profile forces threadcount=1")
#
#         if global_mt_analysis < 2:
#             print("--mt_profile <n-threads> value must be 2 or greater")
#             return CMDERR
#         else:
#             global_threadcount = 1
#             return 1
#     else:
#         print("Missing mt_profile thread count")
#         return CMDERR
#
#
#
# # # Example usage:
# # argc = len(sys.argv)
# # argv = sys.argv
# #
# # if argc < 2:
# #     print("Usage: python script.py --mt_profile <n-threads>")
# #     sys.exit(1)
# #
# # result = mt_profile(argc, argv)
# # if result == CMDOK:
# #     print("Success")
# # elif result == CMDERR:
# #     print("Error")
#
#
#
# def pause_at_exit(argc, argv):
#     global global_pause_at_exit
#     global_pause_at_exit = not global_pause_at_exit
#     return 0
#
#
#
# def compile(argc, argv):
#     global global_compileonly
#     global_compileonly = not global_compileonly
#     return 0
#
#
#
# def license(argc, argv):
#     legal_license()
#     return 0
#
#
#
# def server_portnum(argc, argv):
#     if argc > 1:
#         global_server_portnum = int(argv.pop(0))
#         return 1
#     else:
#         output_fatal("missing server port number")
#         return CMDERR
#
#
#
# def server_inaddr(argc, argv):
#     global global_server_inaddr
#
#     if argc > 1:
#         global_server_inaddr = argv[1][:len(global_server_inaddr)-1]
#         return 1
#     else:
#         output_fatal("missing server ip address")
#         #   TROUBLESHOOT
#         #   The <b>--server_inaddr</b> command line directive
#         #   was not followed by a valid IP address.  The correct syntax is
#         #   <b>--server_inaddr <i>interface address</i></b>.
#         #
#         return CMDERR
#
#
# def version(argc, argv):
#     global global_version_major, global_version_minor, global_version_patch
#     global global_version_build, global_version_branch, global_platform
#     output_message("GridLAB-D %d.%d.%d-%d (%.48s) %d-bit %s %s" %
#         (global_version_major, global_version_minor, global_version_patch,
#         global_version_build, global_version_branch, 0, global_platform,
#         "DEBUG" if DEBUG else "RELEASE"))
#
#     return 0
#
#
# def dsttest(argc, argv):
#     timestamp_test()
#     return 0
#
#
# def randtest(argc, argv):
#     random_test()
#     return 0
#
#
# unit_test = Unit()
#
#
# def unitstest(argc, argv):
#     unit_test.unit_test()
#     return 0
#
#
# def schedule_test(argc, argv):
#     schedule_test()
#     return 0
#
#
# def load_shape_test(argc, argv):
#     loadshape_test()
#     return 0
#
#
# end_use = Enduse()
#
#
# def endusetest(argc, argv):
#     end_use.enduse_test()
#     return 0
#
#
# def xml_strict(argc, argv):
#     global global_xmlstrict
#     global_xmlstrict = not global_xmlstrict
#     output_verbose("xmlstrict is %s", "enabled" if global_xmlstrict else "disabled")
#     return 0
#
#
# def globaldump(argc, argv):
#     global_dump()
#     return CMDOK
#
#
# def relax(argc, argv):
#     global global_strictnames
#     global_strictnames = False
#     return 0
#
#
# def pidfile(argc, argv):
#     global global_pidfile
#     filename = argv[0].split('=')[1] if '=' in argv[0] else None
#     if filename is None:
#         global_pidfile = "gridlabd.pid"
#     else:
#         global_pidfile = filename
#     return 0
#
#
# def kml(argc, argv):
#     global global_kmlfile
#     filename = argv[0].split('=')[1] if '=' in argv[0] else None
#     global_kmlfile = filename if filename else "gridlabd.kml"
#     return 0
#
#
# def avlbalance(argc, argv):
#     global global_no_balance
#     global_no_balance = not global_no_balance
#     return 0
#
#
# def testall(argc, argv):
#     global global_test_mode
#     test_mod_num = 1
#     fd = None
#     if argv[1] is not None:
#         fd = open(argv[1], "r")
#     else:
#         output_fatal("no filename for testall")
#         return CMDERR
#     argc -= 1
#     global_test_mode = True
#
#     if fd is None:
#         output_fatal("incorrect module list file name")
#         return CMDERR
#
#     if load_module_list(fd, test_mod_num) == FAILED:
#         return CMDERR
#
#     return 1
#
#
# def modattr(argc, argv):
#     if argc > 1:
#         mod = None
#         owner_class = None
#         argv = argv[1:]
#         argc -= 1
#
#         if ':' not in argv[0]:  # no class
#             mod = Module.load(argv[0], 0, None)
#         else:
#             mod = Module.load(argv[0].split(':')[0], 0, None)
#
#         j_module = {}
#         _global = {}
#         var = None
#
#         # Dump module globals
#         while True:
#             var = global_get_next(var)
#             if var is None:
#                 break
#
#             prop = var.prop
#             proptype = DynamicClass.class_get_property_typename(prop.global_property_types)
#
#             if not var.prop.name.startswith(mod.name):
#                 continue
#
#             if prop.access & PropertyAccess.PA_HIDDEN == PropertyAccess.PA_HIDDEN:
#                 continue
#
#             if proptype is not None:
#                 _property = {}
#
#                 if prop.unit is not None:
#                     _property["global_property_types"] = proptype
#                     _property["unit"] = prop.unit.name
#                 elif prop.global_property_types == PropertyType.PT_set or prop.global_property_types == PropertyType.PT_enumeration:
#                     _property["global_property_types"] = proptype
#                     for key in prop.keywords:
#                         _property["keywords"][key.name] = key.value
#                 else:
#                     _property["global_property_types"] = proptype
#
#                 if prop.description is not None:
#                     _property["description"] = prop.description
#
#                 if prop.flags & PropertyFlags.PF_DEPRECATED:
#                     _property["deprecated"] = True
#
#                 _global[prop.name] = _property
#
#         j_module["global_attributes"] = _global
#
#         if mod is None:
#             output_fatal(f"module {argv[0]} is not found")
#             # 			/*	TROUBLESHOOT
#             # 				The <b>--modhelp</b> parameter was found on the command line, but
#             # 				if was followed by a module specification that isn't valid.
#             # 				Verify that the module exists in GridLAB-D's <b>lib</b> folder.
#             # 			*/
#             return FAILED
#
#         ctree = None
#         owner_class = DynamicClass.class_get_first_class
#         ctree = Pntree()
#         ctree.name = owner_class.name
#         ctree.owner_class = owner_class
#         ctree.left = ctree.right = None
#
#         for owner_class in DynamicClass.class_get_next_classes():
#             modhelp_alpha(ctree, owner_class)
#
#         # Flatten tree
#         jprint_modhelp_tree(ctree, j_module)
#
#         json_data = json.dumps(j_module, indent=2)
#         print(json_data)
#
#     return 1
#
# def modhelp(argc, argv):
#     if argc > 1:
#         mod = None
#         owner_class = None
#         argv = argv[1:]
#         argc -= 1
#         from gridlab.gldcore.Cmex import module_load
#         if ':' not in argv[0]:  # no class
#
#             mod = module_load(argv[0], 0, None)
#         else:
#             var = None
#             cname = argv[0].split(':')[1]
#             mod = module_load(argv[0].split(':')[0], 0, None)
#             owner_class = DynamicClass(cname)
#             if owner_class is None:
#                 output_fatal(f"Unable to find class '{cname}' in module '{argv[0].split(':')[0]}'")
#                 return FAILED
#
#             # Dump module globals
#             print(f"module {mod.name} {{")
#             while True:
#                 var = global_get_next(var)
#                 if var is None:
#                     break
#
#                 prop = var.prop
#                 proptype = DynamicClass.class_get_property_typename(prop.global_property_types)
#
#                 if not var.prop.name.startswith(mod.name):
#                     continue
#
#                 if prop.access & PropertyAccess.PA_HIDDEN == PropertyAccess.PA_HIDDEN:
#                     continue
#
#                 if proptype is not None:
#                     if prop.unit is not None:
#                         print(f"\t{proptype} {prop.name.split(':')[-1]}[{prop.unit.name}];")
#                     elif prop.global_property_types == PropertyType.PT_set or prop.global_property_types == PropertyType.PT_enumeration:
#                         print(f"\t{proptype} {{")
#                         for key in prop.keywords:
#                             print(f"\t\t{key.name}={key.value},")
#                         print(f"\t}} {prop.name.split(':')[-1]};")
#                     else:
#                         print(f"\t{proptype} {prop.name.split(':')[-1]};")
#
#                     if prop.description is not None:
#                         print(f" // {'' if not prop.flags & PropertyFlags.PF_DEPRECATED else '(DEPRECATED) '}{prop.description}")
#
#             print("}")
#
#         if mod is None:
#             output_fatal(f"module {argv[0]} is not found")
#             return FAILED
#
#         if owner_class is not None:
#             print_class(owner_class)
#         else:
#             owner_class = DynamicClass.class_get_first_class
#             ctree = Pntree(owner_class.name, owner_class)
#             if ctree is None:
#                 raise Exception("--modhelp: malloc failure")
#             ctree.name = owner_class.name
#             ctree.owner_class = owner_class
#             ctree.left = 0
#             ctree.right = 0
#             for owner_class in owner_class.next:
#                 modhelp_alpha(ctree, owner_class)
#
#             # Flatten tree
#             print_modhelp_tree(ctree)
#
#     return 1
#
#
# module = Module()
#
#
# def modlist(arvc, argv):
#     module.module_list()
#     return 1
#
#
# def modtest(argc, argv):
#     if argc > 1:
#         from gridlab.gldcore.Cmex import module_load
#         mod = module_load(argv[1], 0, None)
#         if mod is None:
#             output_fatal(f"module {argv[1]} is not found")
#             # 			/*	TROUBLESHOOT
#             # 				The <b>--modtest</b> parameter was found on the command line, but
#             # 				if was followed by a module specification that isn't valid.
#             # 				Verify that the module exists in GridLAB-D's <b>lib</b> folder.
#             # 			*/
#         else:
#             argv.pop(0)
#             argc -= 1
#             if mod.exec_test is None:
#                 output_fatal(f"module {argv[0]} does not implement a test routine")
#                 # 				/*	TROUBLESHOOT
#                 # 					The <b>--modtest</b> parameter was found on the command line, but
#                 # 					if was followed by a specification for a module that doesn't
#                 # 					implement any test procedures.  See the <b>--libinfo</b> command
#                 # 					line parameter for information on which procedures the
#                 # 					module supports.
#                 # 				*/
#             else:
#                 output_test(f"*** modtest of {argv[0]} beginning ***")
#                 mod.exec_test(0, None)
#                 output_test(f"*** modtest of {argv[0]} ended ***")
#     else:
#         output_fatal("definition is missing")
#         # 		/*	TROUBLESHOOT
#         # 			The <b>--modtest</b> parameter was found on the command line, but
#         # 			if was not followed by a module specification.  The correct
#         # 			syntax is <b>gridlabd --modtest <i>module_name</i></b>.
#         # 		*/
#         return FAILED
#
#
# def test(argc, argv):
#     global global_test_mode
#     n = 0
#     global_test_mode = True
#     while argc > 1:
#         test_request(argv.pop(0))
#         argc -= 1
#         n += 1
#     return n
#
#
#
# def define(argc, argv):
#     global global_strictnames
#     if argc > 1:
#         namestate = global_strictnames
#         global_strictnames = False
#         argv.pop(0)
#         argc -= 1
#
#         if global_setvar(argv[0], None) == SUCCESS:
#             argc -= 1
#
#         global_strictnames = namestate
#         return 1
#     else:
#         output_fatal("definition is missing")
#         return CMDERR
#
#
# def globals(argc, argv):
#     list_ = []
#     n = 0
#     var = None
#
#     # Load the list into the array
#     while True:
#         var = global_get_next(var)
#         if var is None:
#             break
#         if n < 65536:
#             list_.append(var.prop.name)
#             n += 1
#         else:
#             output_fatal("--globals has insufficient buffer space to sort globals list")
#             return 1
#
#     # Sort the array
#     list_.sort(key=lambda x: x.lower())
#
#     # Output the sorted array
#     for name in list_:
#         buffer = [""] * 1024
#         var = global_find(name)
#         if (var.prop.access & PropertyAccess.PA_HIDDEN) == PropertyAccess.PA_HIDDEN:
#             continue
#         global_get_var(var.prop.name, buffer, 1024)
#         value = "".join(buffer)
#         print(f"{var.prop.name}={value};", end="")
#         if var.prop.description or var.prop.flags & PropertyFlags.PF_DEPRECATED:
#             print(f" // {'DEPRECATED ' if var.prop.flags & PropertyFlags.PF_DEPRECATED else ''}"
#                   f"{var.prop.description if var.prop.description else ''}")
#         else:
#             print()
#
#     return 0
#
#
# def redirect(argc, argv):
#     if argc > 1:
#         buffer = argv[1]
#         argv.pop(1)
#         argc -= 1
#
#         if buffer == "none":
#             # Used by validate to block default --redirect all behavior
#             pass
#         elif buffer == "all":
#             streams = ["output", "error", "warning", "debug", "verbose", "profile", "progress"]
#             success = True
#             for stream in streams:
#                 if not output_redirect(stream, None):
#                     output_fatal(f"redirection of {stream} failed")
#                     success = False
#             if not success:
#                 return 1
#         elif ":" in buffer:
#             parts = buffer.split(":")
#             if len(parts) == 2:
#                 stream, destination = parts
#                 if not output_redirect(stream, destination):
#                     output_fatal(f"redirection of {stream} to '{destination}' failed")
#                     return 1
#             else:
#                 output_fatal("invalid redirection format")
#                 return 1
#         else:
#             if not output_redirect(buffer, None):
#                 output_fatal(f"default redirection of {buffer} failed")
#                 return 1
#     else:
#         output_fatal("redirection is missing")
#         return 1
#
# module_instance = Module()
# def libinfo(argc, argv):
#     if argc - 1 > 0:
#         argc -= 1
#         module_instance.module_libinfo(argv[0])
#         return CMDOK
#     else:
#         output_fatal("missing library name")
#     return CMDERR
#
#
# def threadcount(argc, argv):
#     global global_thread_count
#     if argc > 1:
#         global_thread_count = int(argv.pop(0))
#         argc -= 1
#     else:
#         output_fatal("missing thread count")
#         return CMDERR
#     return 1
#
#
# def output(argc, argv):
#     global global_savefile
#     if argc > 1:
#         global_savefile = argv.pop(0)
#         return 1
#     else:
#         output_fatal("missing output file")
#         return CMDERR
#
#
# def environment(argc, argv):
#     global global_environment
#     if argc > 1:
#         global_environment = argv[1]
#     else:
#         output_fatal("environment not specified")
#         # 	TROUBLESHOOT
#         # 	The <b>-e</b> or <b>--environment</b> command line directive
#         # 	was not followed by a valid environment specification.  The
#         # 	correct syntax is <b>-e <i>keyword</i></b> or <b>--environment <i>keyword</i></b>.
#         #
#         return CMDERR
#     return 1
#
#
# def xmlencoding(argc, argv):
#     global global_xml_encoding
#     if argc > 1:
#         global_xml_encoding = int(argv[1])
#         argc -= 1
#     else:
#         output_fatal("xml encoding not specified")
#         #  /*	TROUBLESHOOT
#         #  	The <b>--xmlencoding</b> command line directive
#         #  	was not followed by a encoding specification.  The
#         #  	correct syntax is <b>--xmlencoding <i>keyword</i></b>.
#         #   */
#         return FAILED
#     return 1
#
#
# def xsd(argc, argv):
#     if argc > 0:
#         argc -= 1
#         output_xsd(argv[0])
#         return CMDOK
#     else:
#         mod = Module.get_first()
#         while mod is not None:
#             output_xsd(mod.name)
#             mod = mod.next
#         return 0
#
#
# def xsl(argc, argv):
#     if argc - 1 > 0:
#         fname = f"gridlabd-{global_version_major}_{global_version_minor}.xsl"
#         p_arg = argv[1]
#         n_args = 1
#         p_args = []
#         argc -= 1
#
#         for char in p_arg:
#             if char == ',':
#                 n_args += 1
#
#         p_arg = argv[1].split(',')
#
#         for arg in p_arg:
#             p_args.append(arg)
#
#         output_xsl(fname, n_args, p_args)
#         return CMDOK
#     else:
#         output_fatal("module list not specified")
#         return CMDERR
#
#
# def stream(argc, argv):
#     global global_streaming_io_enabled
#     global_streaming_io_enabled = not global_streaming_io_enabled
#     return 0
#
#
# def server(argc, argv):
#     global global_environment
#     ctypes.CDLL('msvcrt').strcpy(ctypes.c_char_p(global_environment), b"server")
#     return 0
#
#
# schedule = Schedule()
# def clearmap(argc, argv):
#     schedule.sched_clear()
#     return 0
#
#
# def pstatus(argc, argv):
#     schedule.sched_init(1)
#     schedule.sched_print(0)
#     return 0
#
#
# def pkill(argc, argv):
#     if argc > 0:
#         argc -= 1
#         schedule.sched_pkill(int(argv[0]))
#         return 1
#     else:
#         output_fatal("processor number not specified")
#         #   TROUBLESHOOT
#         #   The <b>--pkill</b> command line directive
#         #   was not followed by a valid processor number.
#         #   The correct syntax is <b>--pkill <i>processor_number</i></b>.
#         #
#         return CMDERR  # assuming CMDERR is defined elsewhere in the code
#
#
# def plist(argc, argv):
#     schedule.sched_init(1)
#     schedule.sched_print(0)
#     return 0
#
#
# def pcontrol(argc, argv):
#     schedule.sched_init(1)
#     schedule.sched_controller()
#     return 0
#
#
# def info(argc, argv):
#     if argc > 1:
#         global_browser = "your_browser_command_here"  # Replace with your browser command
#         global_infourl = "http://your_infourl_here.com"  # Replace with your info URL
#         cmd = ""
#
#         if sys.platform.startswith("win"):
#             cmd = f'start {global_browser} "{global_infourl}{argv[1]}"'
#         elif sys.platform == "darwin":
#             cmd = f'open -a {global_browser} "{global_infourl}{argv[1]}"'
#         else:
#             cmd = f'{global_browser} "{global_infourl}{argv[1]}" & ps -p $! >/dev/null'
#
#         output_verbose(f"Starting browser using command [{cmd}]")
#         return_code = os.system(cmd)
#
#         if return_code != 0:
#             output_error("unable to start browser")
#             return CMDERR
#         else:
#             output_verbose("starting interface")
#             return SUCCESS
#     else:
#         output_fatal("info subject not specified")
#         return CMDERR
#
#
# def slave(argc, argv):
#     global global_master, global_master_port, global_multirun_connection
#
#     if argc < 2:
#         output_error("ERROR: slave connection parameters are missing")
#         return CMDERR
#
#     connection_param = argv[1]
#     parts = connection_param.split(':')
#
#     if len(parts) != 2:
#         output_error("ERROR: unable to parse slave parameters")
#         return CMDERR
#
#     host, port = parts
#
#     global_master = host[:255]
#
#     if global_master == "localhost":
#         try:
#             global_master_port = int(port, 16)  # Assuming the port is in hexadecimal
#             global_multirun_connection = MULTIRUNCONNECTION.MRC_MEM
#         except ValueError:
#             output_error("ERROR: Invalid hexadecimal port value")
#             return CMDERR
#     else:
#         try:
#             global_master_port = int(port)
#             global_multirun_connection = MULTIRUNCONNECTION.MRC_SOCKET
#         except ValueError:
#             output_error("ERROR: Invalid port value")
#             return CMDERR
#
#     if instance_slave_init() == "FAILED":
#         output_error(f"ERROR: slave instance init failed for master '{global_master}' connection '{global_master_port}'")
#         return CMDERR
#
#     output_verbose(f"VERBOSE: slave instance for master '{global_master}' using connection '{global_master_port}' started ok")
#     return SUCCESS
#
#
# def instance_slave_init():
#     # Implement your initialization logic here
#     return "SUCCESS"  # Return "SUCCESS" or "FAILED" accordingly
#
# e = Exec()
#
# def slavenode(argc, argv):
#     e.exec_slave_node()
#     return CMDOK
#
#
# def slave_id(argc, argv):
#     if argc < 2:
#         output_error("--id requires an ID number argument")
#         return CMDERR
#
#     try:
#         global_slave_id = int(argv[1])
#     except ValueError:
#         output_error("slave_id(): unable to read ID number")
#         return CMDERR
#
#     output_debug(f"DEBUG: slave using ID {global_slave_id}")
#     return SUCCESS
#
#
# def example(argv):
#     global global_clock
#     if len(argv) < 2:
#         output_error("--example requires a module:class argument")
#         return 1  # CMDERR
#
#     modname, classname = argv[1].split(':')
#
#     module = Module.load(modname)
#     if module is None:
#         output_error(f"--example: module {modname} is not found")
#         return 1  # CMDERR
#
#     owner_class = DynamicClass.get_class_from_classname(classname)
#     if owner_class is None:
#         output_error(f"--example: class {classname} is not found")
#         return 1  # CMDERR
#
#     from gridlab.gldcore.Object import Object
#     object = Object.object_create_single(owner_class)
#     if object is None:
#         output_error(f"--example: unable to create example object from class {classname}")
#         return 1  # CMDERR
#
#     global_clock = time.time_ns()
#     output_redirect("error", None)
#     output_redirect("warning", None)
#
#     if not object_init(object):
#         output_warning(f"--example: unable to initialize example object from class {classname}")
#
#     buffer = ""
#     if object_save(buffer, object) > 0:
#         output_raw(buffer)
#     else:
#         output_warning("no output generated for object")
#
#     return 0  # CMDOK
#
#
# def mclassdef(argv):
#     if len(argv) < 2:
#         output_error("--mclassdef requires a module:class argument")
#         return 1  # CMDERR
#
#     modname, classname = argv[1].split(':')
#
#     module = Module.load(modname)
#     if module is None:
#         output_error(f"--mclassdef: module {modname} is not found")
#         return 1  # CMDERR
#
#     owner_class = DynamicClass.get_class_from_classname(classname)
#     if owner_class is None:
#         output_error(f"--mclassdef: class {classname} is not found")
#         return 1  # CMDERR
#
#     from gridlab.gldcore.Object import Object
#     obj = Object.object_create_single(owner_class)
#     if obj is None:
#         output_error(f"--mclassdef: unable to create mclassdef object from class {classname}")
#         return CMDERR
#
#     global_clock = time.time()
#     output_redirect("error", None)
#     output_redirect("warning", None)
#
#     if not object_init(obj):
#         output_warning(f"--mclassdef: unable to initialize mclassdef object from class {classname}")
#
#     buffer = generate_classdef(modname, classname, owner_class, obj)
#     output_raw(buffer)
#
#     return CMDOK
#
#
# def locktest(argc, argv):
#     test_lock()
#     return CMDOK
#
#
# def lock(argc, argv):
#     global global_lock_enabled
#     global_lock_enabled = not global_lock_enabled
#     return 0
#
#
# def workdir(argc, argv):
#     global global_workdir
#     if argc < 2:
#         output_error("--workdir requires a directory argument")
#         return CMDERR
#     global_workdir = argv[1]
#     try:
#         os.chdir(global_workdir)
#     except OSError:
#         output_error("%s is not a valid workdir" % global_workdir)
#         return CMDERR
#     output_verbose("working directory is '%s'" % os.getcwd(global_workdir))
#     return 1
#
# sanitize = Sanitize()
#
# main_cmd = [
#     # Section heading
#     {
#         'long_str': None,
#         'short_str': None,
#         'processor_call': None,
#         'arglist_desc': None,
#         'help_desc': "Command-line options"
#     },
#
#     # Command-line options
#     {
#         'long_str': "check",
#         'short_str': "c",
#         'processor_call': check,
#         'arglist_desc': None,
#         'help_desc': "Performs module checks before starting simulation"
#     },
#     {
#         'long_str': "debug",
#         'short_str': None,
#         'processor_call': debug,
#         'arglist_desc': None,
#         'help_desc': "Toggles display of debug messages"
#     },
#     {
#         'long_str': "debugger",
#         'short_str': None,
#         'processor_call': debugger,
#         'arglist_desc': None,
#         'help_desc': "Enables the debugger"
#     },
#     {
#         'long_str': "dumpall",
#         'short_str': None,
#         'processor_call': dump_all,
#         'arglist_desc': None,
#         'help_desc': "Dumps the global variable list"
#     },
#     {
#         'long_str': "mt_profile",
#         'short_str': None,
#         'processor_call': mt_profile,
#         'arglist_desc': "<n-threads>",
#         'help_desc': "Analyses multithreaded performance profile"
#     },
#     {
#         'long_str': "profile",
#         'short_str': None,
#         'processor_call': profile,
#         'arglist_desc': None,
#         'help_desc': "Toggles performance profiling of core and modules while simulation runs"
#     },
#     {
#         'long_str': "quiet",
#         'short_str': "q",
#         'processor_call': quiet,
#         'arglist_desc': None,
#         'help_desc': "Toggles suppression of all but error and fatal messages"
#     },
#     {
#         'long_str': "verbose",
#         'short_str': "v",
#         'processor_call': verbose,
#         'arglist_desc': None,
#         'help_desc': "Toggles output of verbose messages"
#     },
#     {
#         'long_str': "warn",
#         'short_str': "w",
#         'processor_call': warn,
#         'arglist_desc': None,
#         'help_desc': "Toggles display of warning messages"
#     },
#     {
#         'long_str': "workdir",
#         'short_str': "W",
#         'processor_call': workdir,
#         'arglist_desc': None,
#         'help_desc': "Sets the working directory"
#     },
#     {
#         'long_str': "lock",
#         'short_str': "l",
#         'processor_call': lock,
#         'arglist_desc': None,
#         'help_desc': "Toggles read and write locks"
#     },
#
#     # Global and module control
#     {
#         'long_str': "define",
#         'short_str': "D",
#         'processor_call': define,
#         'arglist_desc': "<name>=[<module>:]<value>",
#         'help_desc': "Defines or sets a global (or module) variable"
#     },
#     {
#         'long_str': "globals",
#         'short_str': None,
#         'processor_call': globals,
#         'arglist_desc': None,
#         'help_desc': "Displays a sorted list of all global variables"
#     },
#     {
#         'long_str': "libinfo",
#         'short_str': "L",
#         'processor_call': libinfo,
#         'arglist_desc': "<module>",
#         'help_desc': "Displays information about a module"
#     },
#
#     # Information
#     {
#         'long_str': None,
#         'short_str': None,
#         'processor_call': None,
#         'arglist_desc': None,
#         'help_desc': "Information"
#     },
#     {
#         'long_str': "copyright",
#         'short_str': None,
#         'processor_call': copyright,
#         'arglist_desc': None,
#         'help_desc': "Displays copyright"
#     },
#     {
#         'long_str': "license",
#         'short_str': None,
#         'processor_call': license,
#         'arglist_desc': None,
#         'help_desc': "Displays the license agreement"
#     },
#     {
#         'long_str': "version",
#         'short_str': "V",
#         'processor_call': version,
#         'arglist_desc': None,
#         'help_desc': "Displays the version information"
#     },
#     {
#         'long_str': None,
#         'short_str': None,
#         'processor_call': None,
#         'arglist_desc': None,
#         'help_desc': "Test processes"
#     },
#     {
#         'long_str': "dsttest",
#         'short_str': None,
#         'processor_call': dsttest,
#         'arglist_desc': None,
#         'help_desc': "Perform daylight savings rule test"
#     },
#     {
#         'long_str': "endusetest",
#         'short_str': None,
#         'processor_call': endusetest,
#         'arglist_desc': None,
#         'help_desc': "Perform enduse pseudo-object test"
#     },
#     {
#         'long_str': "globaldump",
#         'short_str': None,
#         'processor_call': globaldump,
#         'arglist_desc': None,
#         'help_desc': "Perform a dump of the global variables"
#     },
#     {
#         'long_str': "loadshapetest",
#         'short_str': None,
#         'processor_call': load_shape_test,
#         'arglist_desc': None,
#         'help_desc': "Perform loadshape pseudo-object test"
#     },
#     {
#         'long_str': "locktest",
#         'short_str': None,
#         'processor_call': locktest,
#         'arglist_desc': None,
#         'help_desc': "Perform memory locking test"
#     },
#     {
#         'long_str': "modtest",
#         'short_str': None,
#         'processor_call': modtest,
#         'arglist_desc': "<module>",
#         'help_desc': "Perform test function provided by module"
#     },
#     {
#         'long_str': "randtest",
#         'short_str': None,
#         'processor_call': randtest,
#         'arglist_desc': None,
#         'help_desc': "Perform random number generator test"
#     },
#     {
#         'long_str': "scheduletest",
#         'short_str': None,
#         'processor_call': schedule_test,
#         'arglist_desc': None,
#         'help_desc': "Perform schedule pseudo-object test"
#     },
#     {
#         'long_str': "test",
#         'short_str': None,
#         'processor_call': test,
#         'arglist_desc': "<module>",
#         'help_desc': "Perform unit test of module (deprecated)"
#     },
#     {
#         'long_str': "testall",
#         'short_str': None,
#         'processor_call': testall,
#         'arglist_desc': "=<filename>",
#         'help_desc': "Perform tests of modules listed in file"
#     },
#     {
#         'long_str': "unitstest",
#         'short_str': None,
#         'processor_call': unitstest,
#         'arglist_desc': None,
#         'help_desc': "Perform unit conversion system test"
#     },
#     {
#         'long_str': "validate",
#         'short_str': None,
#         'processor_call': validate,
#         'arglist_desc': "...",
#         'help_desc': "Perform model validation check"
#     },
#
#     # File and I/O Formatting
#     {
#         'long_str': None,
#         'short_str': None,
#         'processor_call': None,
#         'arglist_desc': None,
#         'help_desc': "File and I/O Formatting"
#     },
#     {
#         'long_str': "kml",
#         'short_str': None,
#         'processor_call': kml,
#         'arglist_desc': "[=<filename>]",
#         'help_desc': "Output to KML (Google Earth) file of model (only supported by some modules)"
#     },
#     {
#         'long_str': "stream",
#         'short_str': None,
#         'processor_call': stream,
#         'arglist_desc': None,
#         'help_desc': "Toggles streaming I/O"
#     },
#     {
#         'long_str': "sanitize",
#         'short_str': None,
#         'processor_call': sanitize,
#         'arglist_desc': "<options> <indexfile> <outputfile>",
#         'help_desc': "Output a sanitized version of the GLM model"
#     },
#     {
#         'long_str': "xmlencoding",
#         'short_str': None,
#         'processor_call': xmlencoding,
#         'arglist_desc': "8|16|32",
#         'help_desc': "Set the XML encoding system"
#     },
#     {
#         'long_str': "xmlstrict",
#         'short_str': None,
#         'processor_call': xml_strict,
#         'arglist_desc': None,
#         'help_desc': "Toggle strict XML formatting (default is enabled)"
#     },
#     {
#         'long_str': "xsd",
#         'short_str': None,
#         'processor_call': xsd,
#         'arglist_desc': "[module[:class]]",
#         'help_desc': "Prints the XSD of a module or class"
#     },
#     {
#         'long_str': "xsl",
#         'short_str': None,
#         'processor_call': xsl,
#         'arglist_desc': "module[,module[,...]]]",
#         'help_desc': "Create the XSL file for the module(s) listed"
#     },
#
#     # Help
#     {
#         'long_str': None,
#         'short_str': None,
#         'processor_call': None,
#         'arglist_desc': None,
#         'help_desc': "Help"
#     },
#     {
#         'long_str': "help",
#         'short_str': "h",
#         'processor_call': help,
#         'arglist_desc': None,
#         'help_desc': "Displays command line help"
#     },
#     {
#         'long_str': "info",
#         'short_str': None,
#         'processor_call': info,
#         'arglist_desc': "<subject>",
#         'help_desc': "Obtain online help regarding <subject>"
#     },
#     {
#         'long_str': "modattr",
#         'short_str': None,
#         'processor_call': modattr,
#         'arglist_desc': "module",
#         'help_desc': "Display structure of all classes in a module and its attributes in json format"
#     },
#     {
#         'long_str': "modhelp",
#         'short_str': None,
#         'processor_call': modhelp,
#         'arglist_desc': "module[:class]",
#         'help_desc': "Display structure of a class or all classes in a module"
#     },
#     {
#         'long_str': "modlist",
#         'short_str': None,
#         'processor_call': modlist,
#         'arglist_desc': None,
#         'help_desc': "Display list of available modules"
#     },
#     {
#         'long_str': "example",
#         'short_str': None,
#         'processor_call': example,
#         'arglist_desc': "module:class",
#         'help_desc': "Display an example of an instance of the class after init"
#     },
#     {
#         'long_str': "mclassdef",
#         'short_str': None,
#         'processor_call': mclassdef,
#         'arglist_desc': "module:class",
#         'help_desc': "Generate Matlab classdef of an instance of the class after init"
#     },
#
#     # Process control
#     {
#         'long_str': None,
#         'short_str': None,
#         'processor_call': None,
#         'arglist_desc': None,
#         'help_desc': "Process control"
#     },
#     {
#         'long_str': "pidfile",
#         'short_str': None,
#         'processor_call': pidfile,
#         'arglist_desc': "[=<filename>]",
#         'help_desc': "Set the process ID file (default is gridlabd.pid)"
#     },
#     {
#         'long_str': "threadcount",
#         'short_str': "T",
#         'processor_call': threadcount,
#         'arglist_desc': "<n>",
#         'help_desc': "Set the maximum number of threads allowed"
#     },
#     {
#         'long_str': "job",
#         'short_str': None,
#         'processor_call': job,
#         'arglist_desc': "...",
#         'help_desc': "Start a job"
#     },
#
#     # System options
#     {
#         'long_str': None,
#         'short_str': None,
#         'processor_call': None,
#         'arglist_desc': None,
#         'help_desc': "System options"
#     },
#     {
#         'long_str': "avlbalance",
#         'short_str': None,
#         'processor_call': avlbalance,
#         'arglist_desc': None,
#         'help_desc': "Toggles automatic balancing of object index"
#     },
#     {
#         'long_str': "bothstdout",
#         'short_str': None,
#         'processor_call': both_stdout,
#         'arglist_desc': None,
#         'help_desc': "Merges all output on stdout"
#     },
#     {
#         'long_str': "check_version",
#         'short_str': None,
#         'processor_call': _check_version,
#         'arglist_desc': None,
#         'help_desc': "Perform online version check to see if any updates are available"
#     },
#     {
#         'long_str': "compile",
#         'short_str': "C",
#         'processor_call': compile,
#         'arglist_desc': None,
#         'help_desc': "Toggles compile-only flags"
#     },
#     {
#         'long_str': "environment",
#         'short_str': "e",
#         'processor_call': environment,
#         'arglist_desc': "<appname>",
#         'help_desc': "Set the application to use for run environment"
#     },
#     {
#         'long_str': "output",
#         'short_str': "o",
#         'processor_call': output,
#         'arglist_desc': "<file>",
#         'help_desc': "Enables save of output to a file (default is gridlabd.glm)"
#     },
#     {
#         'long_str': "pause",
#         'short_str': None,
#         'processor_call': pause_at_exit,
#         'arglist_desc': None,
#         'help_desc': "Toggles pause-at-exit feature"
#     },
#     {
#         'long_str': "relax",
#         'short_str': None,
#         'processor_call': relax,
#         'arglist_desc': None,
#         'help_desc': "Allows implicit variable definition when assignments are made"
#     },
#
#     # Server mode
#     {
#         'long_str': None,
#         'short_str': None,
#         'processor_call': None,
#         'arglist_desc': None,
#         'help_desc': "Server mode"
#     },
#     {
#         'long_str': "server",
#         'short_str': None,
#         'processor_call': server,
#         'arglist_desc': None,
#         'help_desc': "Enables the server"
#     },
#     {
#         'long_str': "clearmap",
#         'short_str': None,
#         'processor_call': clearmap,
#         'arglist_desc': None,
#         'help_desc': "Clears the process global_map of defunct jobs (deprecated form)"
#     },
#     {
#         'long_str': "pclear",
#         'short_str': None,
#         'processor_call': clearmap,
#         'arglist_desc': None,
#         'help_desc': "Clears the process global_map of defunct jobs"
#     },
#     {
#         'long_str': "pcontrol",
#         'short_str': None,
#         'processor_call': pcontrol,
#         'arglist_desc': None,
#         'help_desc': "Enters process controller"
#     },
#     {
#         'long_str': "pkill",
#         'short_str': None,
#         'processor_call': pkill,
#         'arglist_desc': "<procnum>",
#         'help_desc': "Kills a run on a processor"
#     },
#     {
#         'long_str': "plist",
#         'short_str': None,
#         'processor_call': plist,
#         'arglist_desc': None,
#         'help_desc': "List runs on processes"
#     },
#     {
#         'long_str': "pstatus",
#         'short_str': None,
#         'processor_call': pstatus,
#         'arglist_desc': None,
#         'help_desc': "Prints the process list"
#     },
#     {
#         'long_str': "redirect",
#         'short_str': None,
#         'processor_call': redirect,
#         'arglist_desc': "<stream>[:<file>]",
#         'help_desc': "Redirects an output to stream to a file (or null)"
#     },
#     {
#         'long_str': "server_portnum",
#         'short_str': "P",
#         'processor_call': server_portnum,
#         'arglist_desc': None,
#         'help_desc': "Sets the server port number (default is 6267)"
#     },
#     {
#         'long_str': "server_inaddr",
#         'short_str': None,
#         'processor_call': server_inaddr,
#         'arglist_desc': None,
#         'help_desc': "Sets the server interface address (default is INADDR_ANY, any interface)"
#     },
#     {
#         'long_str': "slave",
#         'short_str': None,
#         'processor_call': slave,
#         'arglist_desc': "<master>",
#         'help_desc': "Enables slave mode under master"
#     },
#     {
#         'long_str': "slavenode",
#         'short_str': None,
#         'processor_call': slavenode,
#         'arglist_desc': None,
#         'help_desc': "Sets a listener for a remote GridLAB-D call to run in slave mode"
#     },
#     {
#         'long_str': "id",
#         'short_str': None,
#         'processor_call': slave_id,
#         'arglist_desc': "<idnum>",
#         'help_desc': "Sets the ID number for the slave to inform its using to the master"
#     }
# ]
#
#
# def cmdarg_runoption(value):
#     parts = value.split(' ', 1)
#     option = parts[0]
#     params = parts[1] if len(parts) > 1 else ""
#
#     for cmd in main_cmd:
#         if cmd['long_str'] is not None and cmd['long_str'] == option:
#             return cmd['processor_call'](len(parts), [params])
#
#     return 0
#
#
# def help(argc, argv):
#     global global_suppress_repeat_messages
#     old_suppress_repeat_messages = global_suppress_repeat_messages
#     global_suppress_repeat_messages = 0
#     indent = 0
#
#     output_message("Syntax: gridlabd [<options>] file1 [file2 [...]]")
#
#     for cmd in main_cmd:
#         len_cmd = 0
#         if cmd['short_str']:
#             len_cmd += len(cmd['short_str'])
#         if cmd['long_str']:
#             len_cmd += len(cmd['long_str'])
#         if cmd['arglist_desc']:
#             len_cmd += len(cmd['arglist_desc'])
#
#         if len_cmd > indent:
#             indent = len_cmd
#
#     for cmd in main_cmd:
#         if cmd['long_str'] is None and cmd['short_str'] is None and cmd['processor_call'] is None and cmd[
#             'arglist_desc'] is None:
#             desc_len = len(cmd['help_desc'])
#             buffer = "-" * desc_len
#             output_message("")
#             output_message(cmd['help_desc'])
#             output_message(buffer)
#         else:
#             buffer = "  "
#             if cmd['long_str']:
#                 buffer += "--" + cmd['long_str']
#             if cmd['short_str']:
#                 if cmd['long_str']:
#                     buffer += "|"
#                 buffer += "-" + cmd['short_str']
#             if cmd['arglist_desc'] is None or (cmd['arglist_desc'][0] != '=' and cmd['arglist_desc'][:2] != "[="):
#                 buffer += " "
#             if cmd['arglist_desc']:
#                 buffer += cmd['arglist_desc'] + " "
#
#             while len(buffer) < indent + 8:
#                 buffer += " "
#
#             buffer += cmd['help_desc']
#             output_message(buffer)
#
#     global_suppress_repeat_messages = old_suppress_repeat_messages
#     return 0
#
#
# def loadall(param):
#     pass
#
#
# def cmdarg_load(argc, argv):
#     global global_modelname
#     global loader_time
#     status = SUCCESS
#
#     # Special case for no args
#     if argc == 1:
#         return no_cmdargs()
#
#     # Process command arguments
#     while argc > 1:
#         argv_index = 1
#         found = False
#
#         for cmd in main_cmd:
#             arg_lopt = cmd["long_str"]
#             arg_sopt = cmd["short_str"]
#             arg_call = cmd["processor_call"]
#
#             if (arg_sopt and argv[argv_index].startswith("-") and argv[argv_index][1:] == arg_sopt) or \
#                (arg_lopt and argv[argv_index].startswith("--") and argv[argv_index][2:] == arg_lopt) or \
#                (arg_lopt and argv[argv_index].startswith("--") and argv[argv_index][2:].startswith(f"{arg_lopt}=")):
#
#                 n = arg_call(argc, argv[argv_index:])
#                 if n == "CMDOK":
#                     return status
#                 elif n == "CMDERR":
#                     return "FAILED"
#                 else:
#                     found = True
#                     argc -= n
#                     argv_index += n
#
#         # Cmdarg not processed
#         if not found:
#             # File name
#             if not argv[argv_index].startswith("-"):
#                 if global_test_mode:
#                     output_warning(f"file '{argv[argv_index]}' ignored in test mode")
#                 else:
#                     start = time.time()
#
#                     # Preserve name of first model only
#                     if global_modelname == "":
#                         global_modelname = argv[argv_index]
#
#                     if not loadall(argv[argv_index]):
#                         status = "FAILED"
#                     loader_time += time.time() - start
#
#             # Send cmdarg to modules
#             else:
#                 n = Module.cmdargs(argc, argv[argv_index:])
#                 if n == 0:
#                     output_error(f"command line option '{argv[argv_index]}' is not recognized")
#                     status = "FAILED"
#
#         argc -= 1
#
#     return status
#

class CmdArg:
    def __init__(self):
        self.loader_time = 0
        # Initialize other necessary attributes here

    def load_module_list(self, fd, test_mod_num):
        """
        Processes a file descriptor to load module list.

        :param fd: File descriptor or path to the file containing the module list.
        :param test_mod_num: A mutable object like a list containing a single integer
                             to simulate pass-by-reference in Python.
        """
        with open(fd, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading and trailing whitespace
                if not line:
                    continue  # Skip empty lines

                print(f"Line: {line}")  # Simulating the printf call
                mod_test = f"mod_test{test_mod_num[0]}={line}"
                test_mod_num[0] += 1

                # Placeholder for global_setvar check
                if not self.global_setvar(mod_test):
                    print("Unable to store module name")
                    # Simulate returning FAILED enum
                    return "FAILED"

        # Simulate returning SUCCESS enum
        return "SUCCESS"

    def global_setvar(self, mod_test):
        """
        Placeholder for the global_setvar functionality.

        :param mod_test: The module test string.
        :return: A boolean indicating whether the operation was successful.
        """
        # Placeholder logic, always return True to simulate SUCCESS
        return True

    def create_pntree_node(self, oclass):
        """
        Creates and returns a new pntree node.
        """
        # Placeholder for actual node creation logic
        return Pntree(oclass.name, oclass)

    def modhelp_alpha(self, ctree, oclass):
        """
        Inserts a class into a binary tree based on its name.
        """
        cmpval = self.compare(oclass.name, ctree.name)
        if cmpval == 0:
            # Duplicate name, or some other logic as needed
            print(f"ERROR {oclass.name}") #  exception?
            pass
        elif cmpval < 0:
            if ctree.left is None:
                ctree.left = self.create_pntree_node(oclass)
            else:
                self.modhelp_alpha(ctree.left, oclass)
        else:
            if ctree.right is None:
                ctree.right = self.create_pntree_node(oclass)
            else:
                self.modhelp_alpha(ctree.right, oclass)

    def compare(self, a, b):
        """
        Compares two strings and returns -1, 0, or 1.
            Example usage:
            result = self.compare("abc", "ABC")
            print(result)
        """
        return 0 if a.casefold() == b.casefold() else (1 if a.casefold() > b.casefold() else -1)


    def set_tabs(self, tabs, tabdepth):
        """
        Example usage:
        tabs = [''] * 33  # Initialize tabs as a list of 33 empty strings
        set_tabs(tabs, 4)  # Set 4 tabs
        :param tabs:
        :param tabdepth:
        :return:
        """
        if tabdepth > 32:
            raise Exception("print_class_d: tabdepth > 32, which is mightily deep!")
            # TROUBLESHOOT: This means that there is very deep nesting and this is unexpected.
            # This suggests a problem with the internal model and should be reported.
        else:
            tabs[:tabdepth] = '\t' * tabdepth
        return tabs

    def jprint_class_d(self, owner_class=None, tab_depth=4):
        """
        Print details of a class in a structured (JSON) format.

        Example usage:
            jprint_class_d(owner_class, tabdepth, module)
            print(json.dumps(module, indent=4))  # Pretty print the JSON data
        :param owner_class:= ...  # Replace with your DynamicClass instance
        :param tab_depth: ...  # Replace with your tab depth
        :param j_module:  = {}  # Initialize an empty dictionary
        :return:
        """
        j_class = {}
        if owner_class.parent:
            j_class[owner_class.parent.name] = {"global_property_types": "parent"}


        for property_name in owner_class._properties.keys():
            #             self._properties[property_name] = {"global_property_types": self._convert_python_type_to_gradappsd_type(property_type),
            #                                                "default": default_value,
            #                                                "units": units,
            #                                                "flags": flags,
            #                                                "keywords": keywords,
            #                                                "description": description}

            j_property = {"type": str(owner_class._properties[property_name].get("global_property_types", None)),
                          "units": owner_class._properties[property_name].get('units', None),
                          "keywords": owner_class._properties[property_name].get('keywords', None),
                          "description": owner_class._properties[property_name].get('description', None),
                          "default": owner_class._properties[property_name].get('default', None),
                          "flags": owner_class._properties[property_name].get('flags', None),
                          "deprecated": True}

            j_class[property_name] = j_property

        # isinstance(pn, PropertyMap):
        # prop = owner_class.pmap
        # while prop and prop.owner_class == owner_class:
        #     # propname = DynamicClass.class_get_property_type_name(prop.global_property_types)
        #     propname = self.get_property_type_name(prop.global_property_types)
        #     if propname:
        #         if prop.access & PropertyAccess.PA_HIDDEN == PropertyAccess.PA_HIDDEN:
        #             prop = prop.next
        #             continue
        #
        #         j_property = {}
        #         if prop.unit:
        #             j_property["global_property_types"] = propname
        #             j_property["unit"] = prop.unit.name
        #         elif prop.global_property_types in {PropertyType.PT_set, PropertyType.PT_enumeration}:
        #             j_property["global_property_types"] = propname
        #             keywords = {}
        #             key = prop.keywords
        #             while key:
        #                 keywords[key.name] = key.value
        #                 key = key.next
        #             j_property["keywords"] = keywords
        #         else:
        #             j_property["global_property_types"] = propname
        #
        #         if prop.description:
        #             j_property["description"] = prop.description
        #         if prop.flags & PropertyFlags.PF_DEPRECATED:
        #             j_property["deprecated"] = True
        #
        #         j_class[prop.name] = j_property
        #     prop = prop.next

        j_module[owner_class.name] = j_class

        print(json.dumps(j_module, indent=tab_depth))
        return j_module

    def get_property_type_name(self, ptype):
        """
        Placeholder method to get property type name.
        """
        # This should return the name of the property type based on ptype
        # For demonstration, return a simple string
        proptype = ptype['global_property_types']

        return "ExampleType"

    def jprint_class(self, oclass, _module):
        # Stub for jprint_class
        print("Stub for jprint_class")
        pass

    def jprint_modhelp_tree(self, ctree, _module):
        # Stub for jprint_modhelp_tree
        print("Stub for jprint_modhelp_tree")
        pass

    def print_class_d(self, oclass, tabdepth):
        # Stub for print_class_d
        print("Stub for print_class_d")
        pass

    def print_class(self, oclass):
        # Stub for print_class
        print("Stub for print_class")
        pass

    def print_modhelp_tree(self, ctree):
        # Stub for print_modhelp_tree
        print("Stub for print_modhelp_tree")
        pass


    # Newly added stubs
    def help(self):
        print("Stub for help")

    def no_cmdargs(self):
        print("Stub for no_cmdargs")

    def cmdarg_runoption(self, value):
        print("Stub for cmdarg_runoption")

    def check_version(self):
        print("Stub for check_version")

    def test_lock(self):
        print("Stub for test_lock")

    # Include other necessary methods and utility functions here

    def run(self, args):
        # This method can simulate processing command line arguments
        # For now, it's just a placeholder
        print("Processing command line arguments...")


if __name__ == "__main__":  # Example usage
    cmd_arg = CmdArg()
    cmd_arg.run(['--example', 'input_file'])
    from gridlab.gldcore.Module import Module
    my_module = Module(name="my_module")
    # Example setup of classes and properties
    parent_class = DynamicClass(my_module, "ParentClass", None )
    child_class = DynamicClass(my_module,"ChildClass", base_class=parent_class)
    child_class.add_property(PropertyValue("prop1", 60.0, None, "PT_double", unit="Hz", description="An example property.", flags=None))
    j_module = cmd_arg.jprint_class_d(child_class, 4,)
