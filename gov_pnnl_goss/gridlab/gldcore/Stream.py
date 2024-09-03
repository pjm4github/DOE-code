# stream.py
from gov_pnnl_goss.gridlab.gldcore.Class import DynamicClass
from gov_pnnl_goss.gridlab.gldcore.Globals import global_get_count, global_get_var, global_set_var, global_get_next
from gov_pnnl_goss.gridlab.gldcore.Output import output_debug, output_error
from gridlab.gldcore.Module import Module
from gridlab.gldcore.Object import Object
import struct


SF_IN = 0x0001
SF_OUT = 0x0002
SF_STR = 0x0004

STREAM_NAME = "GRIDLABD"
STREAM_VERSION = 2

fp = None
count = 0

# Global variables

stream_name = STREAM_NAME
stream_version = STREAM_VERSION
stream_wordsize = None
stream_pos = 0
flags = 0x00


#stream_wordsize = struct.calcsize("P")
_DEBUG = True


class TOKEN(str):
    pass


class PROPERTY:
    pass


class Streamer:
    stream_list = None
    SF_OUT = 0x01  # Flag for output (writing to stream)
    SF_IN = 0x02   # Flag for input (reading from stream)

    def __init__(self, file_ptr=None, flags=0x00):
        self.stream_pos = 0
        self.file_ptr = file_ptr
        self.flags = flags
        self.stream_list = None
        self.stream_callback = None
        self.stream_name = "STREAM_NAME"
        self.stream_version = "STREAM_VERSION"
        self.stream_wordsize = 8  # Assuming 64-bit system
        self.stream_pos = 0
        self.flags = 0x00
        self.file_ptr = None


    def register_stream_callback(self, callback):
        """
        Register a callback function for the stream.
        The callback function should take four arguments:
        buffer, size, is_write, user_data
        """
        self.stream_callback = callback

    def stream_register(self, call):
        pass

    def stream_callback(self, ptr, len, is_str, match):
        try:
            if is_str:
                return self.stream(ptr, len, True, match)
            else:
                return self.stream(ptr, len, False, match)
        except:
            return -1


    def stream_string(self, s, max_length=0):
        # Handle string streaming
        pass

    def stream_module(self, mod):
        self.stream("MOD")

        count = Module().module_get_count()
        self.stream(count)
        for n in range(count):
            name = [0] * 1024
            if mod:
                name = mod.name
            self.stream(name)

            if flags & SF_OUT:
                mod = mod.next
            if flags & SF_IN:
                Module().module_load(name, 0, None)

        self.stream("/MOD")

    def stream_property(self, owner_class, prop):
        # Handle property streaming
        pass

    def stream_class(self, oclass):
        global stream_pos
        self.stream("RTC")

        # Simulate getting the runtime count for the class
        count = DynamicClass.class_get_runtimecount(oclass)
        self.stream(count)
        for n in range(count):
            # Assuming oclass has attributes like 'name', 'size', 'passconfig'
            # and methods like 'register', 'get_next_runtime', etc.
            name = oclass.name if oclass else ""
            self.stream(name, len(name))

            size = oclass.size if oclass else 0
            self.stream(size)

            passconfig = oclass.passconfig if oclass else 0
            self.stream(passconfig)

            if flags & SF_IN:
                # Register or load class as needed
                oclass = DynamicClass.class_register(None, name, size, passconfig) if oclass else None

            # Stream properties or other related data
            self.stream_properties(oclass)

            if flags & SF_OUT:
                oclass = DynamicClass.class_get_next_runtime(oclass) if oclass else None

            if flags & SF_IN:
                # Load module or perform additional actions required for input streaming
                Module.module_load(oclass.name, 0, None) if oclass else None

        self.stream("/RTC")

    def stream_object(self, obj):
        # Handle object streaming
        pass

    def stream_global(self, var):
        # Handle global variable streaming
        pass



    def stream_type(self, T):
        def stream_type_impl(data, size, property):
            # Your implementation of the stream global_property_types function for a specific global_property_types T here
            pass
        return stream_type_impl
    
    # Define stream functions for various types
    @stream_type(int)
    def stream_int(self, data, size, property):
        # Your implementation for int global_property_types
        pass
    
    @stream_type(float)
    def stream_float(self, data, size, property):
        # Your implementation for float global_property_types
        pass
    
    @stream_type(str)
    def stream_str(self, data, size, property):
        # Your implementation for str global_property_types
        pass

    def stream_context(self, ):
        buffer = bytearray(64)

        return buffer

    def stream_error(self, format, *args):
        buffer = bytearray(1024)
        result = format % args
        buffer[:len(result)] = result.encode()
        return -1

    def stream_warning(self, format, *args):
        b = [f"{arg}" for arg in args]
        buffer = " ".join(b)
        print(buffer)
        return -1

    def stream_compress(self, buf, fp):
        """

        # Example usage:
        if __name__ == "__main__":
            buf = []  # Your input buffer here
            with open("output_file.bin", "wb") as fp:
                stream_compress(buf, fp)
        :param buf:
        :param fp:
        :return:
        """
        count = 0
        original = len(buf)
        raw = buf
        rawlen = 0
        run = buf
        runlen = 0
        diff = 0
        state = "RAW"

        for p in buf:
            dp = p[1] - p[0]

            if state == "RAW":
                if dp == diff:  # pattern repeats
                    runlen += 1
                else:
                    runlen = 0

                if runlen == 8:  # raw buffer in progress and run is long enough to use
                    if rawlen > runlen:
                        rawlen -= runlen  # don't include new run data
                        fp.write(rawlen.to_bytes(2, byteorder='big'))
                        fp.write(raw[:rawlen])
                        count += rawlen + 2

                    state = "RUNLEN"
                    rawlen = 0
                    run = p - runlen

                elif rawlen == 32767:  # long raw buffer
                    fp.write(rawlen.to_bytes(2, byteorder='big'))
                    fp.write(raw[:rawlen])
                    count += rawlen + 2
                    rawlen = 0
                    raw = p
                else:
                    rawlen += 1

            elif state == "RUNLEN":
                if dp == diff:  # run continues
                    runlen += 1

                    if runlen == 32767:  # run buffer is too long
                        runlen |= 0x8000
                        fp.write(runlen.to_bytes(2, byteorder='big'))
                        fp.write(diff.to_bytes(1, byteorder='big'))
                        fp.write(run[0].to_bytes(1, byteorder='big'))
                        count += 4
                        runlen = 0
                        run = p

                else:  # run ends
                    runlen |= 0x8000
                    fp.write(runlen.to_bytes(2, byteorder='big'))
                    fp.write(diff.to_bytes(1, byteorder='big'))
                    fp.write(run[0].to_bytes(1, byteorder='big'))
                    count += 4
                    state = "RAW"
                    raw = p
                    rawlen = 0
                    runlen = 0

            diff = dp

        rawlen = 0
        fp.write(rawlen.to_bytes(2, byteorder='big'))
        count += 2

        fp.write(count.to_bytes(2, byteorder='big'))
        count += 2

        print(f"stream_compress(): {original // 1000 + 1} kB -> {count // 1000 + 1} kB ({count * 100 / original:.1f}%)")
        return count

    def stream_decompress(self, fp, buf):
        count = 0
        ptr = buf
        buflen = 0
        confirm = 0

        class RunState:
            def __init__(self):
                self.runlen = 0
                self.is_compressed = 0

        runstate = RunState()

        while buflen < len(buf):
            runstate_bytes = fp.read(2)
            if len(runstate_bytes) != 2:
                return self.stream_error("stream_decompress(): failed to read runlen")
            runstate.runlen, runstate.is_compressed = int.from_bytes(runstate_bytes, byteorder='big')

            count += 2

            # Check for the end of the compressed stream
            if runstate.runlen == 0:
                break

            # Handle run data
            if runstate.is_compressed:  # Compression flag set
                delta_byte = fp.read(1)
                value_byte = fp.read(1)
                if len(delta_byte) != 1 or len(value_byte) != 1:
                    return self.stream_error("stream_decompress(): failed to read delta/value")
                count += 2
                delta = int.from_bytes(delta_byte, byteorder='big', signed=True)
                value = int.from_bytes(value_byte, byteorder='big', signed=False)

                if delta == 0:
                    ptr += (runstate.runlen + 1)
                    ptr[0:runstate.runlen + 1] = bytes([value] * (runstate.runlen + 1))
                else:
                    run = runstate.runlen + 1
                    while run > 0:
                        ptr[0] = value
                        ptr += 1
                        value += delta
                        run -= 1

            else:  # No compression
                raw_data = fp.read(runstate.runlen)
                if len(raw_data) != runstate.runlen:
                    return self.stream_error("stream_decompress(): failed to read raw data")
                ptr[0:runstate.runlen] = raw_data
                ptr += runstate.runlen
                count += runstate.runlen

        # Check for overrun
        if buflen > len(buf):
            return self.stream_error("stream_decompress(): stream overrun--possible invalid stream")

        # Read confirmation code
        confirm_bytes = fp.read(2)
        if len(confirm_bytes) == 2:
            confirm = int.from_bytes(confirm_bytes, byteorder='big')
            if confirm == count:
                return count
            else:
                return self.stream_error("stream_decompress(): stream confirmation code mismatched--probable invalid stream")
        else:
            return self.stream_error("stream_decompress(): failed to read confirmation code")

    # Register stream functions
    def register_stream_functions(self):
        self.stream_register(self.stream_int)
        self.stream_register(self.stream_float)
        self.stream_register(self.stream_str)


    def stream(ptr, len, is_str, match=None):
        global stream_pos
        if flags & SF_OUT:
            if _DEBUG:
                if is_str:
                    len = len(ptr)
                a = print(f"{len} ", end="")
                if a < 0:
                    raise Exception("Error writing to stream")
                for i in range(len):
                    c = ptr[i]
                    b = 1
                    if not is_str or c < 32 or c > 126 or c == '\\':
                        b = print(f"\\{c:02x}", end="")
                    else:
                        try:
                            print(chr(c), end="")
                        except EOFError:
                            b = -1
                    if b == -1:
                        raise Exception("Error writing to stream")
                    a += b
                print()
                stream_pos += a
                return a
            else:
                # Simplified write operation
                if is_str:
                    len = len(ptr)
                with open("stream_file", "wb") as f:
                    a = f.write(struct.pack("I", len))
                    b = f.write(ptr.encode('utf-8') if isinstance(ptr, str) else ptr)
                    stream_pos += a + b
                    return a + b
        elif flags & SF_IN:
            # Reading from stream
            raise NotImplementedError("Stream reading functionality is not implemented yet.")

    def stream_overload(self, s, max=0):
        t = s[:1024]
        self.stream(t, max if max else len(s), True, s)

    def stream_module(self, mod):
        self.stream("MOD")
        count = Module.module_getcount()
        self.stream(count)
        for n in range(count):
            name = mod.name if mod else ""
            self.stream(name, 1024)
            if flags & SF_OUT:
                mod = mod.next
            if flags & SF_IN:
                Module.module_load(name, 0, None)
        self.stream("/MOD")

    # Additional functions for CLASS, PROPERTY, OBJECT, GLOBALVAR streaming need to be defined here
    # ...

    def stream_file(self, fileptr, opts):
        global stream_pos, flags
        stream_pos = 0
        flags = opts
        # Assuming file operations and additional streaming functionalities are implemented
        # This function will orchestrate the overall streaming process similar to the C++ version

    # def stream_v(self, v):
    #     pass
    #
    # def stream_oc(self, oclass, prop):
    #     pass
    #
    # def stream_o(self, oclass):
    #     pass
    #
    # def stream_obj(self, obj):
    #     self.stream("OBJ")
    #     count = Object.object_get_count()
    #     self.stream(count)
    #     for n in range(count):
    #         pass
    #     self.stream("/OBJ")
    #
    # def stream_gvar(self, var):
    #     pass
    #
    # def stream_file(self, file_ptr, opts):
    #     self.file_ptr = file_ptr
    #     self.flags = opts
    #     stream_pos = 0
    #     fp = self.file_ptr
    #     flags = opts
    #     output_debug("starting stream on file %d with options %x", fp, flags)
    #     try:
    #         self.stream("GLD30")
    #         try:
    #             self.stream(DynamicClass.class_get_first_runtime())
    #         except:
    #             pass
    #         try:
    #             self.stream(Module.module_get_first())
    #         except:
    #             pass
    #         try:
    #             self.stream(Object.object_get_first(None))
    #         except:
    #             pass
    #         try:
    #             self.stream(global_get_next(None))
    #         except:
    #             pass
    #         s = self.stream_list
    #         while s != None:
    #             pass
    #         output_debug("done processing stream on file %d with options %x", fp, flags)
    #         return stream_pos
    #     except Exception as e:
    #         if isinstance(e, str):
    #             pass
    #         else:
    #             output_error("stream() failed as offset %lld", int(stream_pos))
    #             return -1
    #
    #
    #
    # def stream_values(self, oclass, prop):
    #     self.stream("RTC")
    #
    #     count = DynamicClass.class_get_extended_count(oclass)
    #     self.stream(count)
    #     for n in range(count):
    #         name = "" if prop is None else prop.name
    #         self.stream(name, len(name))
    #
    #         global_property_types = None if prop is None else prop.global_property_types
    #         self.stream(global_property_types)
    #
    #         unit = "" if prop is None else prop.unit.name if prop.unit else ""
    #         self.stream(unit, 64)
    #
    #         width = 0 if prop is None else prop.width
    #         self.stream(width)
    #
    #         if flags & SF_OUT:
    #             prop = prop.next
    #         if flags & SF_IN:
    #             DynamicClass.class_add_extended_property(oclass, name, global_property_types, unit)
    #
    #     self.stream("/RTC")
    #
    # def stream_var(self, var):
    #     self.stream("VAR")
    #
    #     count = global_get_count()
    #     self.stream(count)
    #     for n in range(count):
    #         name = ""
    #         if var:
    #             name = var.prop.name
    #         self.stream(name, len(name))
    #
    #         value = ""
    #         if var:
    #             value = global_get_var(name, 1024)
    #         self.stream(value, 1024)
    #
    #         if flags & SF_OUT:
    #             var = var.next
    #         if flags & SF_IN:
    #             global_set_var(name, value)
    #
    #     self.stream("/VAR")
    #
    # # def stream(self, ptr, length, is_str, match=None):
    # #     # This method needs to be implemented based on the specific requirements of streaming
    # #     pass
    #
    # def stream_runtime_count(self, data, is_str=False, match=None):
    #     oclass: DynamicClass = data
    #     self.stream("RTC")
    #
    #     count = DynamicClass.class_get_runtime_count()
    #     self.stream(count)
    #     for n in range(count):
    #         name = oclass.name if oclass else ""
    #         self.stream(name, len(name))
    #
    #         size = oclass.size if oclass else 0
    #         self.stream(size)
    #
    #         passconfig = oclass.passconfig if oclass else None
    #         self.stream(passconfig)
    #
    #         if flags & SF_IN:
    #             oclass = DynamicClass.register(None, name, size, passconfig)
    #
    #         self.stream(oclass, oclass.pmap)
    #
    #         if flags & SF_OUT:
    #             oclass = DynamicClass.get_next_runtime(oclass)
    #         if flags & SF_IN:
    #             Module.module_load(oclass.name, 0, None)
    #     self.stream("/RTC")
    #
    # def stream(self, data, is_str=False, match=None):
    #     """
    #     Stream data to/from a file.
    #     - data: Data to be written or buffer for data to be read.
    #     - is_str: Flag indicating if the data is a string.
    #     - match: Optional match when reading (mismatch causes an exception).
    #     """
    #     if self.flags & self.SF_OUT:
    #         return self._write_to_stream(data, is_str)
    #     elif self.flags & self.SF_IN:
    #         return self._read_from_stream(data, is_str, match)
    #     else:
    #         raise ValueError("Invalid stream flag.")

    # Additional methods to support streaming of various types (MODULE, CLASS, OBJECT, GLOBALVAR)
    # ...

    # Implement other specific methods as needed based on the C++ code

    # def stream(self, s, max=0):
    #     t = s[:1024]
    #     self.stream(t, max if max else len(s), True, s)
    #
    #
    # def stream(self, v):
    #     self.stream(v, len(v))
    #
    # def stream(self, ptr, len_, is_str, match):
    #     if flags & SF_OUT:
    #         if is_str:
    #             len_ = len(ptr)
    #         fp =f"{len_:d}"
    #         a = len(fp)
    #         if a < 0:
    #             pass
    #         for i in range(len_):
    #             b = 0
    #             c = ptr[i]
    #             if not is_str or c < 32 or c > 126 or c == '\\':
    #                 fp = f"{c:02x}"
    #                 b = len(fp)
    #             a += b
    #         fp += "\n"
    #         b = len(fp)
    #         if b < 0:
    #             pass
    #         a += b
    #         self.stream_pos += a
    #         return a
    #     if flags & SF_IN:
    #         a = 0
    #         a = fscanf(fp, "%d", a)
    #         if a < 1:
    #             raise
    #         if a > len:
    #             raise
    #         if fgetc(fp) != ' ':
    #             raise "FMT"
    #         (c_char * len).from_buffer(ptr).value = 0
    #         for i in range(a):
    #             b = fgetc(fp)
    #             if b == '\\' and fscanf(fp, "%02x", b) < 1:
    #                 raise
    #             cast(ptr, POINTER(c_char))[i] = c_char(b)
    #         while fgetc(fp) != '\n':
    #             pass
    #         if match is not None and memcmp(ptr, match, a):
    #             raise 0
    #         b = (log(float(a)) + 2) + a * 3
    #         stream_pos += b
    #         return b
    #     raise
    #
    #
    # def stream(self, owner_class):
    #     self.stream("RTC")
    #
    #     count = DynamicClass.class_get_runtime_count()
    #     self.stream(count)
    #     for n in range(count):
    #         name = owner_class.name if owner_class else ""
    #         self.stream(name, len(name))
    #
    #         size = owner_class.size if owner_class else 0
    #         self.stream(size)
    #
    #         passconfig = owner_class.passconfig if owner_class else None
    #         self.stream(passconfig)
    #
    #         if flags & SF_IN:
    #             owner_class = DynamicClass.register(None, name, size, passconfig)
    #
    #         self.stream(owner_class, owner_class.pmap)
    #
    #         if flags & SF_OUT:
    #             owner_class = DynamicClass.get_next_runtime(owner_class)
    #         if flags & SF_IN:
    #             Module.module_load(owner_class.name, 0, None)
    #     self.stream("/RTC")

    # def stream_type(self, T):
    #     def stream_T(ptr, len, prop):
    #         return self.stream(cast(ptr, POINTER(T)), len)


    # Other forms of the stream method
    # def stream(s, max=0):
    #     t = ctypes.create_string_buffer(s, 1024)
    #     if max:
    #         stream(t, max, True, s)
    #     else:
    #         stream(t, len(s), True, s)

    # def stream(s, max=0):
    #     if max == 0:
    #         max = len(s)
    #     stream(s, max, True)

    # def stream(v):
    #     stream(v, sizeof(v))

    # def stream(mod):
    #     stream("MOD")
    #
    #     count = module_getcount()
    #     stream(str(count))
    #
    #     for n in range(count):
    #         name = ""
    #         if mod:
    #             name = mod.name
    #         stream(name)
    #
    #         if flags & SF_OUT:
    #             mod = mod.next
    #         if flags & SF_IN:
    #             module_load(name, 0, None)
    #
    #     stream("/MOD")

    # def stream(oclass, prop):
    #     stream("RTC")
    #
    #     count = class_get_extendedcount(oclass)
    #     stream(count)
    #     for n in range(count):
    #         name = prop.name if prop else ""
    #         stream(name, len(name))
    #
    #         global_property_types = prop.global_property_types if prop else ""
    #         stream(global_property_types)
    #
    #         unit = prop.unit.name if prop and prop.unit else ""
    #         stream(unit, 64)
    #
    #         width = prop.width if prop else 0
    #         stream(width)
    #
    #         if (flags & SF_OUT):
    #             prop = prop.next
    #         if (flags & SF_IN):
    #             class_add_extended_property(oclass, name, global_property_types, unit)
    #
    #     stream("/RTC")

    # def stream(oclass):
    #     stream("RTC")
    #
    #     count = class_get_runtimecount()
    #     stream(count)
    #     for n in range(count):
    #         name = oclass.name if oclass else ""
    #         stream(name, len(name))
    #
    #         size = oclass.size if oclass else 0
    #         stream(size)
    #
    #         passconfig = oclass.passconfig if oclass else None
    #         stream(passconfig)
    #
    #         if flags & SF_IN:
    #             oclass = ClassRegistry.register_class(None, name, None)
    #
    #         stream(oclass, oclass.pmap)
    #
    #         if flags & SF_OUT:
    #             oclass = class_get_next_runtime(oclass)
    #         if flags & SF_IN:
    #             module_load(oclass.name, 0, None)
    #
    #     stream("/RTC")

    # def stream(var):
    #     print("VAR")
    #
    #     count = global_getcount()
    #     print(count)
    #
    #     for n in range(count):
    #         name = ""
    #         if var:
    #             name = var.prop.name
    #         print(name)
    #
    #         value = ""
    #         if var:
    #             value = global_getvar(name, 1024)
    #         print(value)
    #
    #         if flags & SF_OUT:
    #             var = var.next
    #         if flags & SF_IN:
    #             global_setvar(name, value)
    #
    #     print("/VAR")



    def _write_to_stream(self, data, is_str):
        if is_str:
            if not isinstance(data, str):
                raise ValueError("Data must be a string.")
            data = data.encode()  # Convert string to bytes
        self.file_ptr.write(data)
        self.stream_pos += len(data)
        return len(data)

    def _read_from_stream(self, buffer, is_str, match):
        if is_str and not isinstance(buffer, bytes):
            raise ValueError("Buffer must be a byte array for string data.")
        length = len(buffer)
        read_data = self.file_ptr.read(length)
        if match and read_data != match:
            raise ValueError("Data does not match.")
        if is_str:
            read_data = read_data.decode()  # Convert bytes to string
        self.stream_pos += len(read_data)
        return read_data

    
# Example usage:
if __name__ == "__main__":
    # # Example usage
    # def example_stream_callback(buffer, size, is_write, user_data):
    #     # Implement the callback functionality here
    #     print(f"Buffer: {buffer}, Size: {size}, Is Write: {is_write}, User Data: {user_data}")
    #     return size
    #
    #
    # # Create a Streamer object and use it
    # stream_module = Streamer()
    # stream_module.register_stream_callback(example_stream_callback)
    #
    # # Example file stream operation
    # with open('example.txt', 'r') as file:
    #     stream_size = stream_module.stream(file, flags=0)
    #     print(f"Streamed {stream_size} bytes")
    #
    # Streamer.register_stream_functions()
    # # Call the stream function with appropriate parameters
    # # self.stream(SF_IN | SF_OUT, stream_callback)

    # Example usage
    # streamer = Streamer()
    # with open('example.txt', 'wb') as file_ptr:
    #     streamer.stream_file(file_ptr, opts=0x00)


    # Example usage
    streamer = Streamer()
    with open('example.txt', 'wb') as file_ptr:
        streamer = Streamer(file_ptr, Streamer.SF_OUT)
        streamer.stream(b"Example binary data")

    with open('example.txt', 'rb') as file_ptr:
        streamer = Streamer(file_ptr, Streamer.SF_IN)
        buffer = bytearray(20)  # Buffer size of 20 bytes
        data_read = streamer.stream(buffer)
        print(data_read)

