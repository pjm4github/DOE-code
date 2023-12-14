class SyncMachine:
    def __init__(self, name=None, p=0.0, q=0.0):
        self.name = self.safe_name(name) if name is not None else None
        self.p = p
        self.q = q
        self.id = ""

    @staticmethod
    def safe_name(arg):
        """
        convert a CIM name to simulator name, replacing non-allowed characters
        :param arg: the root bus or component name, aka CIM name
        :return: the compatible name for GridLAB-D or OpenDSS
        """
        if arg is None:
            return None
        s = arg.replace(' ', '_')
        s = s.replace('.', '_')
        s = s.replace('=', '_')
        s = s.replace('+', '_')
        s = s.replace('^', '_')
        s = s.replace('$', '_')
        s = s.replace('*', '_')
        s = s.replace('|', '_')
        s = s.replace('[', '_')
        s = s.replace(']', '_')
        s = s.replace('{', '_')
        s = s.replace('}', '_')
        s = s.replace('(', '_')
        s = s.replace(')', '_')
        return s
