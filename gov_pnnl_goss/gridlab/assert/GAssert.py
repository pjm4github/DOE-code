class GAssert:
    AS_INIT = 0
    AS_TRUE = 1
    AS_FALSE = 2
    AS_NONE = 3

    TCOP_EQ = 0
    TCOP_LT = 1
    TCOP_LE = 2
    TCOP_GT = 3
    TCOP_GE = 4
    TCOP_NE = 5
    TCOP_IN = 6
    TCOP_NI = 7

    def __init__(self, module):
        self.status = self.AS_INIT
        self.target = ""
        self.part = ""
        self.relation = self.TCOP_EQ
        self.value = ""
        self.value2 = ""
        self.lower = ""
        self.upper = ""
        self.module = module

    def create(self):
        default_values = GAssert(self.module)
        self.status = default_values.status
        self.target = default_values.target
        self.part = default_values.part
        self.relation = default_values.relation
        self.value = default_values.value
        self.value2 = default_values.value2
        self.lower = default_values.lower
        self.upper = default_values.upper
        return 1

    def init(self, parent):
        target_obj = self.module.get_object(self.target)
        if not target_obj:
            raise Exception(f"Target '{self.target}' property does not exist")

        self.set_status(self.AS_TRUE)
        return 1

    def commit(self, t1, t2):
        target_obj = self.module.get_object(self.target)
        if not target_obj:
            print(f"{self.target}: target {self.target} is not valid")
            return None

        if self.status == self.AS_NONE:
            print(f"{self.get_name()}: test is not being run on {target_obj.get_name()}")
            return None
        else:
            if self.evaluate_status() != self.get_status():
                relation_str = self.get_relation_str()
                relation_name = self.get_relation_name()
                part = self.part if self.part else "(void)"
                print(
                    f"{self.get_name()}: assert failed on {'NOT ' if self.status != self.AS_TRUE else ''}"
                    f"{target_obj.get_name()} {self.target}.{part} {relation_str} {relation_name} {self.value} {self.value2}"
                )
                return None
            else:
                print(f"{self.get_name()}: assert passed on {target_obj.get_name()}")
                return None

    def evaluate_status(self):
        target_obj = self.module.get_object(self.target)
        if not self.part:
            return target_obj.compare(self.relation, self.value, self.value2) == 1
        else:
            return target_obj.compare(self.relation, self.value, self.value2, self.part) == 1

    def postnotify(self, prop, value):
        # TODO: Implement notify handler for changed value
        return 1

    def get_relation_str(self):
        relations = ["==", "<", "<=", ">", ">=", "!=", "inside", "outside"]
        return relations[self.relation]

    def get_relation_name(self):
        relations = ["TCOP_EQ", "TCOP_LT", "TCOP_LE", "TCOP_GT", "TCOP_GE", "TCOP_NE", "TCOP_IN", "TCOP_NI"]
        return relations[self.relation]


# Example usage:
# module = YourModule()  # Replace with your module implementation
# g_assert = GAssert(module)
# g_assert.status = GAssert.AS_TRUE
# g_assert.target = "my_property"
# g_assert.part = "part_name"
# g_assert.relation = GAssert.TCOP_EQ
# g_assert.value = "42"
# g_assert.value2 = "50"
# g_assert.init(None)
# g_assert.commit(None, None)
