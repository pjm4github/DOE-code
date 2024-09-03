import subprocess

class MatlabEnvironment:
    def __init__(self, argc, argv):
        self.argc = argc
        self.argv = argv

    def startup(self):
        pass

    def load_java_module(self, file, argc, argv):
        print("support for Java modules is implemented somewhere else ~ please review the documentation")
        return None

    def load_python_module(self, file, argc, argv):
        print("support for Python modules is not implemented yet")
        return None


def matlab_startup(argc, argv):
    result = subprocess.call(["matlab", "-r", "gl"])
    if result == 0:
        return "success"
    else:
        return "failed"
