
import time
from threading import Timer
from collections import defaultdict

from gov_pnnl_goss.gridappsd.app.HeartbeatTimeout import HeartbeatTimeout
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class RemoteApplicationTimeoutTask:
    pass

class RemoteApplicationExecArgs:
    def __init__(self):
        self.command = ""


class HeartbeatEvent:
    def on_message(self, message):
        event = message
        app_id = event.data
        app_id = app_id.strip()
        resp = RemoteApplicationHeartbeatMonitor.remote_apps.get(app_id)
        if app_id in RemoteApplicationHeartbeatMonitor.remote_app_timers:
            task = RemoteApplicationHeartbeatMonitor.remote_app_timers[app_id]
            task.cancel()
            RemoteApplicationHeartbeatMonitor.remote_app_timers[app_id] = RemoteApplicationTimeoutTask(60, app_id, RemoteApplicationHeartbeatMonitor())
        else:
            print("Unknown appid: " + app_id)
        # log_manager.log(new LogMessage(this.getClass().getName(),
        #         null,
        #         new Date().getTime(),
        #         "Starting "+this.getClass().getName(),
        #         LogLevel.INFO,
        #         ProcessStatus.RUNNING,
        #         true),GridAppsDConstants.username,
        #         GridAppsDConstants.topic_platformLog);


class RemoteApplicationHeartbeatMonitor(HeartbeatTimeout):
    remote_apps = {}
    remote_app_timers = {}
    
    def __init__(self, log_manager, client):
        self.client = client
        self.logger_manager = log_manager
        self.client.subscribe(GridAppsDConstants.topic_remoteapp_heartbeat + ".*", HeartbeatEvent())

    def add_remote_application(self, app_id, response):
        self.remote_apps[app_id] = response
        task = self.application_timeout_task(60, app_id, self)
        self.remote_app_timers[app_id] = task

    def start_remote_application(self, app_id, args):
        if app_id in self.remote_apps:
            controller = self.remote_apps[app_id]
            exec_args = RemoteApplicationExecArgs()
            exec_args.command = args
            print("Attempting to start remote app on " + controller.start_control_topic[7:])
            self.client.publish(controller.start_control_topic[7:], str(exec_args))
        else:
            raise RuntimeError("No remote application registered for id: " + app_id)

    def stop_remote_application(self, app_id):
        if app_id in self.remote_apps:
            print("Stopping app: " + app_id)
            controller = self.remote_apps[app_id]
            self.client.publish(controller.stop_control_topic, "")
        else:
            raise RuntimeError("No remote application registered for id: " + app_id)

    def timeout(self, app_id):
        print("Unregistering " + app_id)
        if app_id in self.remote_app_timers:
            del self.remote_app_timers[app_id]
        if app_id in self.remote_apps:
            del self.remote_apps[app_id]

    def application_timeout_task(self, param, app_id, self1):
        pass

