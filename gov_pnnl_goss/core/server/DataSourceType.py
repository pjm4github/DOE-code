
class DataSourceType:
    DS_TYPE_JDBC = 10
    DS_TYPE_REST = 20
    DS_TYPE_OTHER = 1000

    def __init__(self, number):
        self.number = number
