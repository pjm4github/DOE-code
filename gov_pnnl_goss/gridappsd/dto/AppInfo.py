
import json
from enum import Enum


class AppType(Enum):
    REMOTE = "REMOTE"
    PYTHON = "PYTHON"
    JAVA = "JAVA"
    WEB = "WEB"


class AppInfo:


    def __init__(self,
                 id: str = None,
                 app_name: str = None,
                 creator: str = None,
                 description: str = None,
                 execution_path: str = None,
                 inputs: list = None,
                 outputs: list = None,
                 launch_on_startup: bool = False,
                 multiple_instances: bool = True,
                 options: list = None,
                 prereqs: list = None,
                 type: AppType = None
                 ):
        self.app_name = app_name
        self.id = id
        self.description = description
        self.creator = creator
        self.inputs = inputs if inputs else []
        self.outputs = outputs if outputs else []
        self.options = options if options else []
        self.execution_path = execution_path
        self.type = type
        self.launch_on_startup = launch_on_startup
        self.prereqs = prereqs if prereqs else []
        self.multiple_instances = multiple_instances

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_creator(self):
        return self.creator

    def set_creator(self, creator):
        self.creator = creator

    def get_inputs(self):
        return self.inputs

    def set_inputs(self, inputs):
        self.inputs = inputs

    def get_outputs(self):
        return self.outputs

    def set_outputs(self, outputs):
        self.outputs = outputs

    def get_options(self):
        return self.options

    def set_options(self, options):
        self.options = options

    def get_execution_path(self):
        return self.execution_path

    def set_execution_path(self, execution_path):
        self.execution_path = execution_path

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def is_launch_on_startup(self):
        return self.launch_on_startup

    def set_launch_on_startup(self, launch_on_startup):
        self.launch_on_startup = launch_on_startup

    def get_prereqs(self):
        return self.prereqs

    def set_prereqs(self, prereqs):
        self.prereqs = prereqs

    def is_multiple_instances(self):
        return self.multiple_instances

    def set_multiple_instances(self, multiple_instances):
        self.instances = multiple_instances

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj.get("id") is None:
            raise ValueError("Expected attribute id not found")
        app_info = AppInfo()
        app_info.__dict__ = obj
        return app_info
