class Switch:
    def __init__(self, name=None, is_open=False):
        self.name = self.safe_name(name) if name is not None else None
        self.open = is_open

    @staticmethod
    def safe_name(arg):
        """
        convert a CIM name to simulator name, replacing unallowed characters
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
