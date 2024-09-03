from gridlab.gldcore.Globals import global_lock_enabled



import threading

MAXSPIN = 1000000000
WBIT = 0x80000000
RBITS = 0x7FFFFFFF


class LOCKLIST:
    def __init__(self):
        name = ""
        lock = 0
        last_value = 0
        next_ = None

class Lock:
    def __init__(self):
        pass

    def rlock(self, lock):
        pass

    def wlock(self, lock):
        pass

    def runlock(self, lock):
        pass

    def wunlock(self, lock):
        pass



class AtomicCounter:
    # # Example usage
    # atomic_counter = AtomicCounter()
    #
    # # Simulate atomic increment in a thread-safe manner
    # new_value = atomic_counter.atomic_increment()
    # print(f"New value after atomic increment: {new_value}")

    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def atomic_increment(self):
        with self.lock:
            self.value += 1
            return self.value

    def atomic_compare_and_swap(self, comp, xchg):
        with self.lock:
            if self.value == comp:
                self.value = xchg
                return True
            else:
                return False


def register_lock(name, lock):
    item = {"name": name, "lock": lock, "last_value": lock}
    if lock != 0:
        print(f"{name} lock initial value not zero ({lock})")
    item["next"] = register_lock.locklist if hasattr(register_lock, "locklist") else None
    register_lock.locklist = item


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def check_lock(lock, write, unlock):
    item = LOCKLIST()

    # lock locklist
    check_lock = 0
    timeout = MAXSPIN
    value = 0
    while(True):
        value = check_lock
        if timeout == 0:
            raise Exception("check lock timeout")
        timeout -= 1
        if ((value&1) or (not AtomicCounter().atomic_compare_and_swap(check_lock, value, value + 1))):
            break

    item = LOCKLIST()
    while(item):
        if item.lock == lock:
            break
        item = item.next
    if not item:
        if unlock and (lock&1) != 1:
            print("{} {}lock({}) = {} (unregistered)".format("write" if write else "read",
                  "un" if unlock else "  ", lock, lock))
        register_lock("unregistered", lock)
    else:
        no_lock = unlock and ((lock&1) != 1)
#       damage = abs(item.last_value - lock) > 1
#       if damage:  # found a registered lock that was damaged
#           print("{} {}lock({}) = {} ({}) - possible damage (last={})".format(
#               "write" if write else "read", "un" if unlock else "  ", lock, lock, item.name, item.last_value))
        if no_lock:  # found a registered lock that was not locked
            print("{} {}lock({}) = {} ({}) - no lock detected (last={})".format(
                "write" if write else "read", "un" if unlock else "  ", lock, lock, item.name, item.last_value))
        item.last_value = lock

    # unlock locklist
    AtomicCounter().atomic_increment(check_lock)


def runlock(lock):
    if global_lock_enabled:
        value = lock[0]
        check_lock(lock, False, True)
        AtomicCounter().atomic_increment(lock)

# def runlock(lock):
#     while True:
#         test = lock
#         if lock.compare_and_swap(test, test - 1):
#             break
# def runlock(lock):
#     while lock_tmp != lock or lock_tmp & 1:
#         pass



def unlock(lock):
    lock[0] = 0


def wunlock(lock):
    if global_lock_enabled:
        value = lock[0]
        check_lock(lock, True, True)
        AtomicCounter().atomic_increment(lock)

#
# def wunlock(lock):
#     test = 0
#     # Release write lock
#     while True:
#         test = lock.value
#         if AtomicCounter().atomic_compare_and_swap(lock, test, test & RBITS):
#             break
#

# def wunlock(lock):
#     # Release write lock
#     while True:
#         test = lock
#         if AtomicCounter().atomic_compare_and_swap(lock, test, test + 1):
#             break



def rlock(lock):
    value = 0
    while (value & 1) or not AtomicCounter().atomic_compare_and_swap(lock, value, value | 0x80000000):
        value = lock

#
# def rlock(lock):
#     while True:
#         test = lock.value
#         if not (test & WBIT) or AtomicCounter().atomic_compare_and_swap(lock, test, test + 1):
#             break
# def rlock(lock):
#     lock_tmp = 0
#     while True:
#         lock_tmp = lock
#         # End the loop, checking that no writes occurred or are in progress

def wlock(lock):
    while True:
        value = lock[0]
        if not (value & 0x80000001) or AtomicCounter().atomic_compare_and_swap(lock, value, value + 1):
            break

# def wlock(lock):
#     import sys
#     WBIT = 1 << (sys.getsizeof(lock)*8 - 1)
#     RBITS = ~WBIT
#
#     # 1. Wait for exclusive write lock to be released, if any
#     # 2. Take exclusive write lock
#     while True:
#         test = lock[0]
#         if test & WBIT == 0 and AtomicCounter().atomic_compare_and_swap(lock, test, test | WBIT):
#             break
#     # 3. Wait for readers to complete before proceeding
#     while lock[0] & RBITS:
#         pass

#
# def wlock(lock):
#     # 1. Wait for exclusive write lock to be released, if any
#     # 2. Take exclusive write lock
#     while True:
#         test = lock
#         if test & 1 or not threading._acquire_restore(lock, test, test + 1):
#             continue
#         break




