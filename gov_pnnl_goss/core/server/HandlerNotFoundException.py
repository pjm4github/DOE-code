
class HandlerNotFoundException(Exception):
    serial_version_UID = 5582363974612539305

    def __init__(self, request=None):
        if not request:
            super().__init__()
        elif isinstance(request, str):
            super().__init__(request)
        else:
            super().__init__(f"Handler for {request.__class__.getName()} request was not found!")
    
