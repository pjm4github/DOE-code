# stream.py
from gov_pnnl_goss.gridlab.gldcore.Class import Class, PROPERTYNAME
from gov_pnnl_goss.gridlab.gldcore.Globals import global_getnext, global_get_count, global_get_var, global_set_var
from gov_pnnl_goss.gridlab.gldcore.Output import output_debug, output_error
from gridlab.gldcore.Module import Module
from gridlab.gldcore.Object import Object

SF_IN = 0x0001
SF_OUT = 0x0002
SF_STR = 0x0004

STREAM_NAME = "GRIDLABD"
STREAM_VERSION = 2

fp = None
count = 0

stream_name = STREAM_NAME
stream_version = STREAM_VERSION
stream_wordsize = None
stream_pos = 0
flags = 0x00


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

    def stream_property(self, oclass, prop):
        # Handle property streaming
        pass

    def stream_class(self, oclass):
        # Handle class streaming
        pass

    def stream_object(self, obj):
        # Handle object streaming
        pass

    def stream_global(self, var):
        # Handle global variable streaming
        pass

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
    # def stream(self, oclass):
    #     self.stream("RTC")
    #
    #     count = Class.class_get_runtime_count()
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
    #             oclass = Class.register(None, name, size, passconfig)
    #
    #         self.stream(oclass, oclass.pmap)
    #
    #         if flags & SF_OUT:
    #             oclass = Class.get_next_runtime(oclass)
    #         if flags & SF_IN:
    #             Module.module_load(oclass.name, 0, None)
    #     self.stream("/RTC")

    # def stream_type(self, T):
    #     def stream_T(ptr, len, prop):
    #         return self.stream(cast(ptr, POINTER(T)), len)

    def stream_type(self, T):
        def stream_type_impl(data, size, property):
            # Your implementation of the stream type function for a specific type T here
            pass
        return stream_type_impl
    
    # Define stream functions for various types
    @stream_type(int)
    def stream_int(self, data, size, property):
        # Your implementation for int type
        pass
    
    @stream_type(float)
    def stream_float(self, data, size, property):
        # Your implementation for float type
        pass
    
    @stream_type(str)
    def stream_str(self, data, size, property):
        # Your implementation for str type
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

    def stream_v(self, v):
        pass
    
    def stream_oc(self, oclass, prop):
        pass

    def stream_o(self, oclass):
        pass
        
    def stream_obj(self, obj):
        self.stream("OBJ")
        count = Object.object_get_count()
        self.stream(count)
        for n in range(count):
            pass
        self.stream("/OBJ")

    def stream_gvar(self, var):
        pass

    def stream_file(self, file_ptr, opts):
        self.file_ptr = file_ptr
        self.flags = opts
        stream_pos = 0
        fp = self.file_ptr
        flags = opts
        output_debug("starting stream on file %d with options %x", fp, flags)
        try:
            self.stream("GLD30")
            try:
                self.stream(Class.class_get_first_runtime())
            except:
                pass
            try:
                self.stream(Module.module_get_first())
            except:
                pass
            try:
                self.stream(Object.object_get_first(None))
            except:
                pass
            try:
                self.stream(global_getnext(None))
            except:
                pass
            s = self.stream_list
            while s != None:
                pass
            output_debug("done processing stream on file %d with options %x", fp, flags)
            return stream_pos
        except Exception as e:
            if isinstance(e, str):
                pass
            else:
                output_error("stream() failed as offset %lld", int(stream_pos))
                return -1
    


    def stream_values(self, oclass, prop):
        self.stream("RTC")
    
        count = Class.class_get_extended_count(oclass)
        self.stream(count)
        for n in range(count):
            name = "" if prop is None else prop.name
            self.stream(name, len(name))
    
            ptype = None if prop is None else prop.ptype
            self.stream(ptype)
    
            unit = "" if prop is None else prop.unit.name if prop.unit else ""
            self.stream(unit, 64)
    
            width = 0 if prop is None else prop.width
            self.stream(width)
    
            if flags & SF_OUT:
                prop = prop.next
            if flags & SF_IN:
                Class.class_add_extended_property(oclass, name, ptype, unit)
    
        self.stream("/RTC")
    
    def stream_var(self, var):
        self.stream("VAR")
    
        count = global_get_count()
        self.stream(count)
        for n in range(count):
            name = PROPERTYNAME()
            if var:
                name = var.prop.name
            self.stream(name, len(name))
    
            value = ""
            if var:
                value = global_get_var(name, 1024)
            self.stream(value, 1024)
    
            if flags & SF_OUT:
                var = var.next
            if flags & SF_IN:
                global_set_var(name, value)
    
        self.stream("/VAR")

    # def stream(self, ptr, length, is_str, match=None):
    #     # This method needs to be implemented based on the specific requirements of streaming
    #     pass

    def stream_runtime_count(self, data, is_str=False, match=None):
        oclass: OClass = data
        self.stream("RTC")

        count = Class.class_get_runtime_count()
        self.stream(count)
        for n in range(count):
            name = oclass.name if oclass else ""
            self.stream(name, len(name))

            size = oclass.size if oclass else 0
            self.stream(size)

            passconfig = oclass.passconfig if oclass else None
            self.stream(passconfig)

            if flags & SF_IN:
                oclass = Class.register(None, name, size, passconfig)

            self.stream(oclass, oclass.pmap)

            if flags & SF_OUT:
                oclass = Class.get_next_runtime(oclass)
            if flags & SF_IN:
                Module.module_load(oclass.name, 0, None)
        self.stream("/RTC")

    def stream(self, data, is_str=False, match=None):
        """
        Stream data to/from a file.
        - data: Data to be written or buffer for data to be read.
        - is_str: Flag indicating if the data is a string.
        - match: Optional match when reading (mismatch causes an exception).
        """
        if self.flags & self.SF_OUT:
            return self._write_to_stream(data, is_str)
        elif self.flags & self.SF_IN:
            return self._read_from_stream(data, is_str, match)
        else:
            raise ValueError("Invalid stream flag.")

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

