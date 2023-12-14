import json

class RequestPlatformStatus:
    serial_version_UID = 8110107008939698575

    def __init__(self):
        self.applications = False
        self.services = False
        self.app_instances = False
        self.service_instances = False
        self.field = False
      
    def is_applications(self):
        return self.applications

    def set_applications(self, applications):
        self.applications = applications

    def is_services(self):
        return self.services

    def set_services(self, services):
        self.services = services

    def is_app_instances(self):
        return self.app_instances

    def set_app_instances(self, app_instances):
        self.app_instances = app_instances

    def is_service_instances(self):
        return self.service_instances

    def set_service_instances(self, service_instances):
        self.service_instances = service_instances

    def is_field(self):
        return self.field

    def set_field(self, field):
        self.field = field

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if not (obj.app_instances or obj.services or obj.applications or obj.service_instances or obj.field):
            obj.applications = True
            obj.services = True
            obj.app_instances = True
            obj.service_instances = True
            obj.field = True
        return obj
