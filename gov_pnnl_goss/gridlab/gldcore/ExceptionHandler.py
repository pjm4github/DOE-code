# Example usage:
# handler = ExceptionHandler(1, "Example exception")


class ExceptionHandler(BaseException):
    def __init__(self, _id=0, msg=None):
        self.id = _id  # the exception handler id
        self.buf = None  # the jmpbuf containing the context for the exception handler
        self.msg = msg[:1024]  # the message thrown (truncated to 1024 characters)
        self.next = None  # the next exception handler
        self.handlers = None
        self.contents: ExceptionHandler = None

    def create_exception_handler(self):
        ptr = ExceptionHandler()
        ptr.contents.next = self.handlers
        ptr.contents.id = (self.handlers.contents.id if self.handlers else 0) + 1
        ptr.contents.msg = (' ' * len(ptr.contents.msg))
        self.handlers = ptr
        return ptr

    def delete_exception_handler(self, ptr):
        if ptr is None:
            print("delete_exception_handler(): ending an exception handler block where no exception handler was present")
            return
        target = ptr.next
        while self.handlers != target:
            pass

    def throw_exception(self, format, *args):
        if self.handlers:
            pass
        else:
            print("UNHANDLED EXCEPTION: %s\n" % (format % args))
            print("TROUBLESHOOT\nAn exception was generated that can't be handled by the system. This usually occurs because some part of a module or external library isn't properly compiled or linked.")
            exit()

    def exception_msg(self):
        return self.handlers.msg
