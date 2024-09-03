import copy

from gridlab.gldcore.GridLabD import GldProperty


class CacheItem:
    def __init__(self, var):
        self.var = var
        self.value = ""
        # obj = var.obj.get_object()
        # prop = var.obj.get_property()
        # self.remote_name = var.remote_name
        # self.id = self.get_id(var)
        # if self.index is None:
        #     gl_verbose("cacheitem::init(): initial cache index size is %d" % self.index_size)
        #     self.index = [None] * self.index_size
        #
        # if self.index[self.id] is not None:
        #     item = self.get_item(self.id)
        #     if item.get_object() == obj and item.get_property() == prop and item.get_remote() == self.remote_name:
        #         raise "attempt to create a duplication cache item"
        #     else:
        #         gl_debug("cache collison, growing cache size")
        #         self.grow()
        #         self.__init__(var_map)
        # else:
        #     self.marked = False
        #     self.index[self.id] = self
        #     self.var = var_map
        #     self.value = [0] * 1025
        #     self.xltr = None
        #     self.next = None
        #     if self.first is not None:
        #         self.first.next = self
        #     self.first = self

    def get_remote(self):
        return "test"

    @staticmethod
    def get_id(var):
        # # Simplified ID generation based on 'var'. Adjust as necessary.
        # obj = var.obj.get_object()
        # prop = var.obj.get_property()
        # remote_name = var.remote_name
        # a = obj.id
        # b = int(prop.addr)
        # nb = int(prop.owner_class.size)
        # c = 0
        # nc = len(remote_name) * 128
        # for char in remote_name:
        #     c += ord(char)
        # return ((a * nb + b) * nc + c) % size

        return hash(var)

    def read(self):
        # Simulate reading cache item value
        #     def read(self, buffer, length):
        #         if length > len(self.value) + 1:
        #             if self.xltr is None:
        #                 buffer = self.value
        #             else:
        #                 self.xltr(buffer, length, self.value, 1025, TF_DATA, self.var)
        #             self.unmark()
        #             self.value = ""
        #             return True
        #         else:
        #             return False

        return copy.deepcopy(self.value)

    def write(self, buffer):
        # len_value = len(self.value)
        # if len_value < 1025:  # TODO look into using prop_width instead to save memory
        #     # check cache
        #     if self.value != '' and buffer != self.value:
        #         gl_warning("cache_item.write(): cache already contains different data for local '{}'/remote '{}'".format(self.var_local_name, self.var_remote_name))
        #
        #     # copy/xlate buffer to cache
        #     if self.xltr is None:
        #         self.value = buffer
        #     else:
        #         self.xltr(self.value, 1025, buffer, len(buffer) + 1, TF_DATA, self.var)
        #     self.mark()
        #     return True
        # else:
        #     return False

        # Simulate writing to cache item
        self.value = copy.deepcopy(buffer)

    def copy_from_object(self):
        # Placeholder for copying from associated object
        # prop = GldProperty(self.get_object(), self.get_property())
        # return prop.to_string(value, 1024) < 0 ? False : True

        prop = GldProperty(self.get_object(), self.get_property())
        return False if prop.to_string(self.value, 1024) < 0 else True

    def copy_to_object(self):
        # prop = gld_property(self.get_object(), self.get_property())
        # return False if prop.from_string(value) < 0 else True

        # Placeholder for copying to associated object
        pass

    # def grow_cache_item(self):
    #
    #     new_size = self.index_size * 0x100  # 16 times bigger
    #     gl_verbose("cache_item::grow(): double cache index size to %d entries", new_size)
    #     new_index = [None] * new_size
    #
    #     # TODO this takes a while--put a mechanism in place to keep/use a list of non-null entries
    #     # copy old ids to new ids
    #     n = self.first
    #     while n is not None:
    #         new_id = self.get_id(n.get_var())
    #         new_index[new_id] = n
    #         n = n.next
    #
    #     del self.index
    #     self.index = new_index

class Cache:
    def __init__(self):
        self.size = 0x100
        self.items = {}
        # self.cache_item = CacheItem(None)

        # self.size = 0x100
        # self.tail = 0
        # self.list = [None] * self.size
        # self.cache_item_init()

    def option(self, command):
        cmd, arg = command.split(maxsplit=1)
        if len(arg) > 0:
            if cmd == "size":
                self.set_size(int(arg))
                return True
        else:
            print(f"Cache.option(command={command}): invalid command")
            return False


        pass

    def set_size(self, n):
        # Adjust size if needed; Python list/dict automatically resize
        pass

    def write(self, var, translator=None):

        #         obj = var_map.obj.get_object()
        #         prop = var_map.obj.get_property()
        #         remote = var_map.remote_name
        #         id = cacheitem.get_id(var_map)
        #         item = cacheitem.get_item(id)
        #         if item is None:
        #             item = cacheitem(var_map)
        #         buffer = bytearray(1025)
        #         with var_map.obj.get_object().gld_rlock:
        #             var_map.obj.to_string(buffer, len(buffer))
        #         return True


        id = CacheItem.get_id(var)
        if id not in self.items:
            self.items[id] = CacheItem(var)
        # Assuming a buffer is a string representation of 'var' for simplicity
        buffer = str(var)
        self.items[id].write(buffer)
        return True

    def read(self, var, translator=None):
        #         obj = var_map.obj.get_object()
        #         prop = var_map.obj.get_property()
        #         remote = var_map.remote_name
        #         id = Cacheitem.get_id(var_map)
        #         item = Cacheitem.get_item(id)
        #         if item is None:
        #             item = Cacheitem(var_map)
        #         buffer = bytearray(1025)
        #         if item.read(buffer, len(buffer)):
        #             if len(buffer) > 0:
        #                 with gld_wlock(var_map.obj.get_object()):
        #                     return var_map.obj.from_string(buffer) > 0  # convert incoming data
        #             else:
        #                 return True  # no incoming data to process
        #         else:
        #             return False  # unable to read incoming data

        id = CacheItem.get_id(var)
        if id in self.items:
            return self.items[id].read()
        else:
            return False  # or appropriate error handling

    def add_item(self, var):
        # id_ = cacheitem.get_id(var)
        # item = cacheitem.get_item(id_)
        # if item is None:
        #     item = cacheitem(var)
        #
        # # assign it to the cache list
        # id_ = item.get_id()
        # if id_ > self.size:
        #     gl_error("cache id index overrun")
        #     del item
        #     return None
        # if self.list[id_] != 0:
        #     gl_error("cache id index collision")
        #     del item
        #     return None
        # self.list[self.tail] = id_
        # self.tail += 1
        #
        # # copy the initial value from the object
        # item.copy_from_object()
        #
        # return item


        id = CacheItem.get_id(var)
        if id not in self.items:
            self.items[id] = CacheItem(var)
        return self.items[id]

    def find_item(self, var):
        # n = 0
        # item = None
        # while n < self.tail:
        #     m = self.get_item(n)
        #     if (var_map.local_name == m.get_var().local_name and
        #             var_map.remote_name == m.get_var().remote_name):
        #         item = m
        #         break
        #     n += 1
        # return item
        id = CacheItem.get_id(var)
        return self.items.get(id, None)

    def dump(self):
        for id, item in self.items.items():
            print(f"{id}.{item.value}/{item.get_remote()}")
            # gl_debug("%6d %-16s %-32s", item->get_id(), name, item->get_buffer());

    def dump_cache(self):
        for n in self.items.keys():
            item = self.items[n]
            name = "{}.{}/{}".format(item.get_object().name, item.get_property().name, item.get_remote())
            print("{:6d} {:<16} {:<32}".format(item.get_id(), name, item.get_buffer()))


if __name__ == "__main__":
    # Example usage
    cache = Cache()
    var = "example_var"  # Simplified variable representation
    cache.write(var)
    print("Cache dump after writing:")
    cache.dump()
