from gov_pnnl_goss.gridlab.gldcore.Exec import Exec
from gov_pnnl_goss.gridlab.gldcore.Output import output_fatal, output_verbose
from gov_pnnl_goss.gridlab.gldcore.Gui import GuiEntity
from gov_pnnl_goss.gridlab.gldcore.Globals import global_environment, global_dumpfile, FAILED, SUCCESS
from gov_pnnl_goss.gridlab.gldcore.Matlab import matlab_startup
from gov_pnnl_goss.gridlab.gldcore.Xcore import xstart


def server_startup(argc, argv):
    pass


def gui_html_output_all():
    pass


def server_join():
    pass


def gui_X11_start():
    pass


class Environment:

    def environment_start(self, argc, argv):
        global global_environment
        if global_environment == "batch":
            if GuiEntity.gui_get_root():
                global_environment = "gui"
                # go to UseGui
            # do the run
            if Exec.exec_start() == FAILED:
                output_fatal("shutdown after simulation stopped prematurely")
                # TROUBLESHOOT
                # The simulation stopped because an unexpected condition was encountered.
                # This can be caused by a wide variety of things, but most often it is
                # because one of the objects in the model could not be synchronized
                # propertly and its clock stopped.  This message usually follows a
                # more specific message that indicates what caused the simulation to
                # stop.
                if global_dumpfile[0] != '\0':
                    pass
                return FAILED
            return SUCCESS
        elif global_environment == "matlab":
            output_verbose("starting Matlab")
            return matlab_startup(argc, argv)
        elif global_environment == "server":
            # server only mode (no GUI)
            output_verbose("starting server")
            if server_startup(argc, argv):
                return Exec.exec_start()
            else:
                return FAILED
        elif global_environment == "html":
            # this mode simply dumps the html data to a file
            return gui_html_output_all()
        elif global_environment == "gui":
            # go to UseGui
            output_verbose("starting server")
            if server_startup(argc, argv) and GuiEntity.gui_startup(argc, argv):
                result = Exec.exec_start()
                gui = GuiEntity.gui_get_root()
                if result != SUCCESS:
                    return result
                if gui == None:
                    return FAILED
                if gui.hold:
                    return server_join()
                else:
                    return FAILED
            else:
                return FAILED
        elif global_environment == "X11":
            try:
                xstart()
                if GuiEntity.gui_get_root():
                    gui_X11_start()
                return Exec.exec_start()
            except Exception as e:
                output_fatal("X11 not supported")
                return FAILED
        else:
            output_fatal("%s environment not recognized or supported", global_environment)
            # TROUBLESHOOT
            # The environment specified isn't supported. Currently only
            # the <b>batch</b> environment is normally supported, although
            # some builds can support other environments, such as <b>matlab</b>.
            
            return FAILED
