

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
class TestList:
    def __init__(self, name, call, enabled, next_item):
        self.name = name
        self.call = call
        self.enabled = enabled
        self.next = next_item


class TestModule:
    test_list = [
        TestList("dst", timestamp_test, 0, None),
        TestList("rand", random_test, 0, None),
        TestList("units", unit_test, 0, None),
        TestList("schedule", schedule_test, 0, None),
        TestList("loadshape", loadshape_test, 0, None),
        TestList("enduse", enduse_test, 0, None),
        TestList("lock", test_lock, 0, None)
        # add new core test routines before this line
    ]
    last_test = test_list[len(test_list)-1]

    def test_register(self, name, call):
        pass

    def test_request(self, name):
        item = None
        mod = None
        output_verbose("running test '%s'...", name)
        for item in self.test_list:
            if item.name == name:
                item.enabled = 1
                return "SUCCESS"
        return "FAILED"

    def test_exec(self):
        for item in self.test_list:
            if item.enabled != 0:
                item.call()
        return "SUCCESS"


def test_register(name, call):
    pass


def test_request(name):
    item = None
    mod = None
    output_verbose("running test '%s'...", name)
    for item in TestModule.test_list:
        if item.name == name:
            item.enabled = 1
            return "SUCCESS"
    return "FAILED"


def test_exec():
    for item in TestModule.test_list:
        if item.enabled != 0:
            item.call()
    return "SUCCESS"


# Memory Lock Test
TESTCOUNT = "(10000000/global_thread_count)"
count = None
total = 0
key = 0
done = 0


def test_lock_proc(ptr):
    pass


def test_lock():
    if global_lock_enabled:
        n, sum = 0, 0
        count = [0]*global_threadcount
        if not count:
            pass
        output_test("*** Begin memory locking test for %d threads", global_threadcount)
        wlock(key)
        for n in range(global_threadcount):
            pt = None
            count[n] = 0
            if pthread_create(pt, None, test_lock_proc, n) != 0:
                output_test("thread creation failed")
                return "FAILED"
        wunlock(key)
        global_suppress_repeat_messages = 0
        for n in range(global_threadcount):
            output_raw("THREAD %2d  " % n)
        output_message("     TOTAL      ERRORS")
        for n in range(global_threadcount):
            output_raw("---------- %2d" % n)
        output_message("---------- --------")
        while done < global_threadcount:
            pass
        output_message("")
        for n in range(global_threadcount):
            output_test("thread %d count = %d" % (n, count[n]))
            sum += count[n]
        output_test("total count = %d" % total)
        if sum != total:
            output_test("TEST FAILED")
        else:
            output_test("Last key = %d" % key)
        output_test("*** End memory locking test", global_threadcount)
        return "SUCCESS"
    else:
        output_test("Locks disabled.")
        output_message("Locks disabled.")
        return "SUCCESS"


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def test_register(name, call):
    item = TESTLIST()
    if item == None:
        output_error("test_register(char *name='%s', TESTFUNCTION call=%p): memory allocation failed", name, call)
        return 'FAILED'
    last_test.next = item
    item.name = name[:len(item.name)]
    item.call = call
    item.enabled = 0
    item.next = None
    last_test = item
    return 'SUCCESS'


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def test_lock_proc(ptr):
    id = ptr[0]
    m = 0
    output_test("thread {} created ok".format(id))
    for m in range(TESTCOUNT):
        wlock(key)
        count[id] += 1
        total += 1
        wunlock(key)
    wlock(key)
    done += 1
    wunlock(key)
    output_test("thread {} done ok".format(id))
    return 0
