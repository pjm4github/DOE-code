
from gov_pnnl_goss.core.Request import Request


class ExecuteRequest(Request):

    serial_version_UID = 3599179114722683296

    def __init__(self, job_id, machine_name):
        super().__init__()
        self.job_id = job_id
        self.machine_name = machine_name
        self.remote_password = ""  # Utilities.get_property(machine_name)

    def get_job_id(self):
        return self.job_id

    def set_job_id(self, job_id):
        self.job_id = job_id

    def get_machine_name(self):
        return self.machine_name

    def set_machine_name(self, machine_name):
        self.machine_name = machine_name

    def get_remote_password(self):
        return self.remote_password
