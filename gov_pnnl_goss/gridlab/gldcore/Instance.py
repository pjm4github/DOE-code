import time
import os
from typing import List
import threading

from gridlab.connection.Connection import MESSAGEFLAG
from gridlab.gldcore.Exec import Exec
from gridlab.gldcore.GldRandom import random_id
from gridlab.gldcore.Globals import SUCCESS, FAILED, MULTIRUNMODE, TIMESTAMP
from gridlab.gldcore.Output import output_error, output_debug, output_verbose
from enum import Enum, auto
from socket import socket, AF_INET, SOCK_STREAM

# Assuming TIMESTAMP and STATUS are defined elsewhere, we'll use placeholders
STATUS = bool

# Lock and condition for signaling
mls_inst_lock = threading.Lock()
mls_inst_signal = threading.Condition(mls_inst_lock)

class LinkageType:
    LT_MASTERTOSLAVE = 1
    LT_SLAVETOMASTER = 2


class InstanceState(Enum):
    IST_DEFAULT = auto()
    IST_MASTER_INIT = auto()
    IST_MASTER_RUN = auto()
    IST_MASTER_WAIT = auto()
    IST_MASTER_DONE = auto()
    IST_SLAVE_INIT = auto()
    IST_SLAVE_RUN = auto()
    IST_SLAVE_WAIT = auto()
    IST_SLAVE_DONE = auto()

class CnxType(Enum):
    CI_MMAP = auto()  # memory map (windows localhost)
    CI_SHMEM = auto()  # shared memory (linux localhost)
    CI_SOCKET = auto()  # socket (remote host)

class INSTANCE_MSG:
    MSG_GLM	= "GLDGLM".encode('utf-8')
    MSG_LINK = "GLDLNKS".encode('utf-8')
    MSG_INST = "GLDINST".encode('utf-8')
    MSG_DATA = "GLDDATA".encode('utf-8')
    MSG_OK = "GLDOKAY".encode('utf-8')
    MSG_START = "GLDSTART".encode('utf-8')
    MSG_ERR = "GLDERROR".encode('utf-8')
    MSG_DONE = "GLDDONE".encode('utf-8')

class Message:
    def __init__(self, usize, asize, id, hard_event, ts, name_size, data_size, data):
        self.usize = usize
        self.asize = asize
        self.id = id
        self.hard_event = hard_event
        self.ts = ts
        self.name_size = name_size
        self.data_size = data_size
        self.data = data

    def message_init(self, asize, name_size, data_size):
        global global_clock
        self.usize = 0
        self.asize = asize
        self.ts = global_clock
        self.hard_event = 0
        self.name_size = name_size
        self.data_size = data_size

class MessageWrapper:
    """
    # Example usage:
        # Assuming `msg` is an instance of `Message` already created
        wrapper, status = messagewrapper_init(msg)
        if status == SUCCESS:
            print("MessageWrapper initialized successfully")
        else:
            print("MessageWrapper initialization failed")
    """
    def __init__(self, msg: Message):
        if msg is None:
            raise ValueError("MessageWrapper initialization failed: msg is None")

        self.msg = msg
        self.name_size = msg.name_size
        self.data_size = msg.data_size
        # Assuming `name_buffer` and `data_buffer` are intended to reference portions of `msg.data`
        # In Python, we don't manipulate memory directly but can slice or directly assign data.
        self.name_buffer = msg.data[:msg.name_size]  # Slice the `data` attribute of msg for `name_buffer`
        self.data_buffer = msg.data[msg.name_size:msg.name_size + msg.data_size]  # Adjust for `data_buffer`

    @staticmethod
    def message_wrapper_init(message):
        if message is None:
            output_error("messagewrapper_init(): msg is None")
            return FAILED
        try:
            wrapper = MessageWrapper(message)
            return wrapper, SUCCESS
        except ValueError as e:
            output_error(str(e))
            return None, FAILED


class Instance:
    def __init__(self, hostname, id="", model=None, execdir="", threadid=0, cnxtypestr=None):
        self.buffer_size = 0
        self.cache = bytearray(self.buffer_size)  # Placeholder for the cache
        self.cacheid = self.random_id()
        self.cachesize = 0
        self.cnxtype = None
        self.cnxtypestr = cnxtypestr
        self.command = ""
        self.execdir = execdir
        self.hostname = hostname
        self.id = id
        self.message: [Message, None] = None
        self.model = model
        self.name_size = 0
        self.next = None
        self.pid = 0
        self.port = 0
        self.prop_size = 0
        self.read = []
        self.reader_count = 0
        self.return_port = 0
        self.sockfd = socket(AF_INET, socket)
        self.threadid = threadid
        self.write = []
        self.writer_count = 0

    def instance_init(self):
        if self is None:
            raise ValueError("instance_init(): null inst object")

        # Check for looping model
        global_modelname = "MasterModel"  # Assuming this is defined elsewhere
        if self.model == global_modelname:
            raise ValueError(
                f"instance_init(): slave instance model '{self.model}' is the same as the master model '{global_modelname}'")

        # Validate cnxtype
        cnxtypes = {
            "mmap": CnxType.CI_MMAP,
            "shmem": CnxType.CI_SHMEM,
            "socket": CnxType.CI_SOCKET,
        }

        if self.cnxtypestr:
            if self.cnxtypestr in cnxtypes:
                self.cnxtype = cnxtypes[self.cnxtypestr]
            else:
                raise ValueError(
                    f"instance_init(): unrecognized connection type '{self.cnxtypestr}' for instance '{self.model}'")
        else:
            # Default connection type
            # self.cnxtype = CnxType.CI_SHMEM if not _WIN32 else CnxType.CI_MMAP
            self.cnxtype = CnxType.CI_MMAP
        # Initialize linkages and calculate message buffer requirements
        for lnk in self.write + self.read:
            try:
                lnk.linkage_init()  # Assuming this function is defined elsewhere
            except Exception as e:
                raise ValueError(
                    f"instance_init(): linkage_init failed for inst '{self.hostname}.{self.model}' on link: {e}")

        # Allocate and initialize the message buffer
        self.buffer_size = self.cachesize = self.calculate_message_buffer_size(
            self)  # Assuming this function calculates buffer size
        self.cache = Message(self.cachesize)  # Assuming Message class exists and handles buffer initialization

        # Connect instance based on cnxtype
        if not self.instance_connect():  # Assuming this function is defined elsewhere
            raise ValueError("instance_init(): instance_connect() failed")

        # Start the slave instance process thread
        try:
            self.threadid =self.start_instance_thread(
                self)  # Assuming this function starts a thread and returns its identifier
        except Exception as e:
            raise ValueError(f"instance_init(): unable to start instance slave {self.id}: {e}")

        print(f"instance_init(): started instance for slave {self.id}")
        InstanceRegistry.instances_count += 1  # Assuming instances_count is a global variable tracking the number of instances

        return True  # Indicate success

    def random_id(self):
        # Placeholder for generating a random ID
        import random
        return random.randint(1, 10000)  # Example implementation

    # Placeholder methods for functionalities like instance creation, initialization, syncing, etc.
    @staticmethod
    def instance_create(name):
        """
        This function creates a new slave instance object in the current instance's list of slaves.
        @param name: Name for the new instance.
        @return: A new Instance object.

        Example usage
            new_instance = instance_create("localhost")
            if new_instance is not None:
                print(f"New instance created on {new_instance.hostname}")
        """
        try:
            inst = Instance(name)
        except ValueError as e:
            print(str(e))  # Assuming output_error prints to standard error or logs
            return None

        # Add to the start of the instance list (like pushing onto a stack)
        inst.next = InstanceRegistry.instance_list
        InstanceRegistry.instance_list = inst

        print(f"Defining new instance on {name}")  # Assuming output_verbose prints to standard output or logs
        return inst

    def instance_runproc_socket(self):
        if self is None:
            print("Error: null instance pointer")
            return
        running = 1
        rv = 0
        got_data = 0
        self.has_data = 0
        while running:
            buffer = self.sockfd.recv(self.buffer_size, 0)
            if rv == 0:
                output_error("instance_runproc_socket(): socket was closed before receiving data")
                running = 0
            elif rv < 0:
                output_error("instance_runproc_socket(): error receiving data")
                running = 0
            else:
                if buffer[:len(INSTANCE_MSG.MSG_DATA)] == INSTANCE_MSG.MSG_DATA:
                    got_data = 1
                    self.has_data += 1
                elif buffer[:len(INSTANCE_MSG.MSG_ERR)] == INSTANCE_MSG.MSG_ERR:
                    output_error("instance_runproc_socket(): slave indicated an error occurred")
                    running = 0
                elif buffer[:len(INSTANCE_MSG.MSG_DONE)] == INSTANCE_MSG.MSG_DONE:
                    output_verbose("instance_runproc_socket(): slave indicated run completion")
                    running = 0
                else:
                    pass
                self.cache = buffer[len(INSTANCE_MSG.MSG_DATA): len(INSTANCE_MSG.MSG_DATA)+len(INSTANCE_MSG.MESSAGE)]
                self.message.data_buffer = buffer[len(INSTANCE_MSG.MSG_DATA)+len(INSTANCE_MSG.MESSAGE): len(INSTANCE_MSG.MSG_DATA)+len(MESSAGEFLAG.MESSAGE)+self.prop_size]
                output_debug("inst %d sending signal 0x%x", self.id, self.sock_signal)
                Exec.pthread_cond_broadcast(self.sock_signal)
        Exec.pthread_cond_broadcast(self.sock_signal)
        Instance.sock_created = 0
        return 0

    def instance_runproc(self):
        if self is None:
            output_error("instance_runproc(): null instance pointer provided")
            return -1
        cmd = "char1024"
        rc = 0
        if self is None:
            output_error("instance_runproc(): null instance pointer provided")
            return -1
        output_error("Memory Map (mmap) instance mode only supported under Windows, please use Shared Memory (shmem) instead.")
        return -1

    def instance_add_linkage(self, linkage):
        if self is None:
            print("instance_add_linkage(): null inst object")  # Assuming output_error prints to stderr or a log
            return 0
        if linkage is None:
            print("instance_add_linkage(): null lnk object")
            return 0

        # Assuming LT_MASTERTOSLAVE and LT_SLAVETOMASTER are defined elsewhere
        if linkage.type == LinkageType.LT_MASTERTOSLAVE:
            linkage.next = self.write
            self.write = linkage
        elif linkage.type == LinkageType.LT_SLAVETOMASTER:
            linkage.next = self.read
            self.read = linkage
        else:
            return FAILED

        return SUCCESS

    def instance_initall(self):

        global global_multirun_mode
        if InstanceRegistry.instance_list:
            global_multirun_mode = MULTIRUNMODE.MRM_MASTER
            print("Entering multirun mode")  # output_verbose
            # output_prefix_enable()

            with mls_inst_signal:
                print("Waiting for slaves to signal initialization is complete...")  # output_verbose
                mls_inst_signal.wait()

        else:
            return SUCCESS

        for inst in InstanceRegistry.instance_list:
            if not inst.instance_init():  # Assuming instance_init function is defined elsewhere
                return FAILED

        # Wait for slaves to signal init done
        rv = self.instance_master_wait()  # Assuming this function is defined elsewhere
        if not rv:
            print("instance_initall(): final wait() failed")  # output_error
            return FAILED

        return SUCCESS

    # Example usage of instance_initall
    if instance_initall():
        print("All instances initialized successfully.")
    else:
        print("Initialization failed.")


    def instance_master_done(self, t1):
        for inst in InstanceRegistry.instance_list:
            # Assuming debug output is handled elsewhere
            # Update the timestamp in the instance's cache
            self.cache.ts = t1
            if inst.cnxtype == CnxType.CI_MMAP:
                print(f"Master signaling MMAP slave {self.id} with timestamp {self.cache.ts}")
                self.instance_master_done_mmap()
            elif inst.cnxtype == CnxType.CI_SHMEM:
                print(f"Master signaling SHMEM slave {self.id} with timestamp {self.cache.ts}")
                self.instance_master_done_shmem()
            elif inst.cnxtype == CnxType.CI_SOCKET:
                print(f"Master signaling SOCKET slave {self.id} with timestamp {self.cache.ts}")
            else:
                print(f"Unknown connection type for instance ID {self.id}")
                self.instance_master_done_socket()


    def instance_master_done_socket(self):
        if self is None:
            print("instance_master_done_socket(): null inst object")
            return

        try:
            # Assuming inst.buffer is a bytearray or similar that gets populated with data,
            # and self.sockfd is a socket object created elsewhere.
            msg = self.message.data.encode('utf-8') + self.cache + self.message.data_buffer
            sent_bytes = self.sockfd.send(msg)
            print("Sent {} bytes".format(sent_bytes))  # Placeholder for printcontent functionality

        except socket.error as e:
            print("instance_master_done_socket(): error sending data to inst ID {}: {}".format(self.id, e))
            self.sockfd.close()

    def instance_master_done_mmap(self):
        if self is None:
            print("instance_master_done_mmap(): null inst object")  # Assuming output_error logs or prints to stderr
            return

        # In Python, signaling across processes on Windows could be done using the multiprocessing library or
        # third-party libraries that wrap Windows API calls. This is a placeholder for such an operation.
        print("Master signaling slave with ID {} (placeholder for SetEvent)".format(self.id))

    def instance_master_done_shmem(self):
        # Placeholder function for shared memory signaling
        pass

    def instance_master_wait(self):
        status = FAILED

        for inst in InstanceRegistry.instance_list:
            print(f"master waiting on slave {inst.id}")
            if inst.cnxtype == CnxType.CI_SOCKET:
                status = self.instance_master_wait_socket()
            # Add other connection types as necessary

            if status == FAILED:
                break

        print("master resuming")
        return status

    def instance_master_wait_socket(self):
        if self is None:
            print("instance_master_wait_socket(): null inst object")
            return 0

        # Assuming `sock_created` checks if a socket is properly initialized
        if self.sock_created:
            with self.sock_lock:
                if self.has_data > 0:
                    print(f"instance_master_wait_socket(): already has data for {self.id}")
                else:
                    print(f"instance_master_wait_socket(): inst {self.id} waiting")
                    self.sock_signal.wait()  # Wait for the condition to be notified
                self.has_data -= 1

        else:
            print("instance_master_wait_socket(): no socket created")
            return 0

        return 1

    def instance_dispose(self):
        """
        # Example usage of instance_dispose
            if instance_dispose():
                print("All instances disposed successfully.")
            else:
                print("Failed to dispose instances.")
        :return:
        """
        if InstanceRegistry.instance_list:  # If there are instances in the master list
            self.instance_master_done(TIMESTAMP.TS_NEVER)  # Assuming this function signals all instances to terminate

            for inst in InstanceRegistry.instance_list:
                # Assuming each instance has a 'thread' attribute that is a Thread object
                if hasattr(inst, 'thread') and inst.thread.is_alive():
                    inst.thread.join()  # Wait for the thread to terminate

                # If there are other resources to release (e.g., network sockets), they should be closed here

            InstanceRegistry.instance_list.clear()  # Clear the list of instances
            return SUCCESS
        else:  # If there are no instances, or this is called in the context of a slave instance
            # Perform any necessary cleanup for slave instances here

            return SUCCESS

    def instance_presync(self, t1):
        pass

    def instance_sync(self, t1):
        pass

    def instance_postsync(self, t1):
        pass

    def instance_syncall(self, t1):

        if not InstanceRegistry.instance_list:  # If there are no instances, return TS_NEVER
            return TIMESTAMP.TS_NEVER

        t2 = TIMESTAMP.TS_NEVER
        ts = time.perf_counter()  # Using time.perf_counter() as a substitute for exec_clock()

        # Check if an instance was lost
        global instances_exited
        if instances_exited > 0:
            print(f"{instances_exited} instance exit detected, stopping main loop")
            return TIMESTAMP.TS_INVALID

        # Send linkage to slaves
        for inst in InstanceRegistry.instance_list:
            inst.cache.ts = t1
            self.instance_write_slave(inst)  # Assuming this function is defined elsewhere

        # Signal slaves to start
        self.instance_master_done(t1)  # Assuming this function is defined elsewhere

        # Wait for slaves to signal they're done
        wc = self.instance_master_wait()  # Assuming this function is defined elsewhere
        if wc != 0:
            pass  # Placeholder for any additional handling

        # Read linkages from slaves
        for inst in InstanceRegistry.instance_list:
            t3 = self.instance_read_slave(inst)  # Assuming this function is defined elsewhere
            if t3 < t2:
                t2 = t3

        print(f"instance sync time is {t2}")
        self.instance_synctime = time.perf_counter() - ts  # Update sync time; assuming instance_synctime is defined elsewhere

        return t2

    def instance_write_slave(self,  inst):
        if inst is None:
            print("instance_write_slave(): null inst object")  # Assuming output_error function logs errors
            return False  # FAILED

        # Mock-up: Assuming linkage_master_to_slave function is responsible for sending data to the slave
        for lnk in inst.write:
            res = Linkage.linkage_master_to_slave(
                lnk)  # Assuming this function is defined elsewhere and handles the actual data sending
            if not res:
                print(
                    "instance_write_slave(): linkage_master_to_slave failed")  # Assuming output_error function logs errors
                return False  # FAILED

        # Assuming inst.buffer and inst.cache are byte-like objects for simplicity
        # In Python, you'd directly assign the contents of cache to buffer instead of using memcpy
        inst.buffer = inst.cache[:inst.cachesize]  # Simulates memcpy from inst->cache to inst->buffer

        # Mock function to print content of the buffer
        print_content(inst.buffer)  # Assuming a function that prints or logs the buffer contents

        return True  # SUCCESS

    def instance_read_slave(self, inst):
        pass

        if inst is None:
            print("instance_read_slave(): null inst object")  # Assuming output_error logs errors
            return TIMESTAMP.TS_INVALID

        # Assuming inst.cache is an object with a timestamp attribute (ts)
        t2 = getattr(inst.cache, 'ts', TIMESTAMP.TS_INVALID)

        for lnk in inst.read:
            res = Linkage.linkage_slave_to_master(inst.cache, lnk)  # Assuming this function handles reading data from the slave
            if not res:
                print(
                    f"Failed to read data for linkage {lnk}")  # Handling failure, could be logging or other error handling

        return t2

class InstanceRegistry:
    instance_list: List = []
    instance_synctime: int = 0
    instances_count: int = 0
    instances_exited: bool = True
    sock_created: bool = False

    HS_SYN = "GLDMTR"
    HS_ACK = "GLDSND"
    # note trailing space for CBK
    HS_CBK = "GLDSLV "
    HS_RSP = "GLDRDY"
    # note trailing space for CMD
    HS_CMD = "GLDCMD "
    HS_FAIL = "GLDFAIL"


    def __init__(self, host):
        if host is None:
            print("instance_create(): null host string provided")
        self.hostname = host
        self.cacheid = random_id()
        InstanceRegistry.instance_list.append(self)
        self.next = InstanceRegistry.instance_list[0]

class Linkage:
    """
    # Example usage:
        inst = Instance()
        lnk1 = Linkage(LinkageType.LT_MASTERTOSLAVE)
        lnk2 = Linkage(LinkageType.LT_SLAVETOMASTER)

        success1 = inst.add_linkage(lnk1)
        success2 = inst.add_linkage(lnk2)

        if success1 and success2:
            print("Both linkages added successfully.")
        else:
            print("Failed to add one or more linkages.")
    """
    def __init__(self, objname, propname, obj, prop, link_type):
        self.next = None  # Assuming linkage objects are linked
        self.remote_obj = objname
        self.remote_prop = propname
        self.target_obj = obj
        self.target_prop = prop
        self.type = link_type

    def add_linkage(self, lnk):
        """
        This method adds a linkage to an instance.
        @param lnk: The linkage to add.
        @return: True on success, False on failure.
        """
        if lnk is None:
            print("instance_add_linkage(): null lnk object")  # Assuming output_error logs or prints error
            return False

        if lnk.type == LinkageType.LT_MASTERTOSLAVE:
            lnk.next = self.write
            self.write = lnk
            return True
        elif lnk.type == LinkageType.LT_SLAVETOMASTER:
            lnk.next = self.read
            self.read = lnk
            return True
        else:
            return False

    def linkage_create_reader(inst, fromobj, fromvar, toobj, tovar):
        pass

    def linkage_create_writer(inst, fromobj, fromvar, toobj, tovar):
        pass

    def linkage_init(inst, lnk) -> int:
        pass

    # Mock-up of the linkage_master_to_slave function, assuming it sends data from master to slave
    @staticmethod
    def linkage_master_to_slave(lnk) -> int:
        # Simulate sending data to slave. In real application, this might involve sockets, files, etc.
        try:
            # Assuming lnk contains data to be sent and a way to send it (e.g., a socket or file descriptor)
            print(f"Sending data for linkage {lnk}")  # Placeholder action
            return True  # Simulate success
        except Exception as e:
            print(f"Failed to send data for linkage {lnk}: {str(e)}")
            return False

    @staticmethod
    def linkage_slave_to_master(lnk) -> int:
        pass



    #
    # def pthread_mutex_lock(lock):
    #     pass
    #
    # def pthread_cond_wait(cond, lock):
    #     pass
    #
    # def pthread_mutex_unlock(lock):
    #     pass
    #
    # def pthread_cond_broadcast(cond):
    #     pass
    #
    # def pthread_create(threadid, null, instance_runproc, void_ptr_inst):
    #     pass
    #
    # def recv(sockfd, buffer, A, B):
    #     pass

def global_modelname():
    pass

def print_content(data):
    the_str = [0] * 2*len(data)
    for i in range(data):
        the_str[2*i] = data[i] // 16 + 48
        the_str[2*i+1] = data[i] % 16 + 48
        if the_str[2*i] > 57:
            the_str[2*i] += 39
        if the_str[2*i+1] > 57:
            the_str[2*i+1] += 39

    s = "".join(chr(the_str))
    print(f"content = {s}")

