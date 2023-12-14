import pickle


class PlatformStatus:
    serial_version_UID = 285312877963778626
    # # Example usage
    # apps = [AppInfo(), AppInfo()]
    # services = [ServiceInfo(), ServiceInfo()]
    # app_instances = [AppInstance(), AppInstance()]
    # service_instances = [ServiceInstance(), ServiceInstance()]
    # platform_status = PlatformStatus(apps, services, app_instances, service_instances)

    def __init__(self, applications=None, services=None, app_instances=None, service_instances=None):
        self.applications = applications if applications else []
        self.services = services if services else []
        self.app_instances = app_instances if app_instances else []
        self.service_instances = service_instances if service_instances else []
        self.field_model_mrid = ''

    def get_applications(self):
        return self.applications

    def set_applications(self, applications):
        self.applications = applications

    def get_services(self):
        return self.services

    def set_services(self, services):
        self.services = services

    def get_app_instances(self):
        return self.app_instances

    def set_app_instances(self, app_instances):
        self.app_instances = app_instances

    def get_service_instances(self):
        return self.service_instances

    def set_service_instances(self, service_instances):
        self.service_instances = service_instances

    def set_field(self, field_model_mrid):
        self.field_model_mrid = field_model_mrid
