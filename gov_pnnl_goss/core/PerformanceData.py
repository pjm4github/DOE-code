
class PerformanceData:
    serial_version_UID = 9030062346549383871

    def __init__(self):
        self.ds1 = 0
        self.ds2 = 0

    def get_ds1(self):
        return self.ds1

    def set_ds1(self, ds1):
        self.ds1 = ds1

    def get_ds2(self):
        return self.ds2

    def set_ds2(self, ds2):
        self.ds2 = ds2
    # Note: In Python, we do not need to explicitly implement `Serializable` interface as in Java.