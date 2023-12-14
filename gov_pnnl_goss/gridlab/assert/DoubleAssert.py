import math


class DoubleAssert:
    """
    /* double_assert

    Very simple test that compares double values to any corresponding double value.  If the test
    fails at any time, it throws a 'zero' to the commit function and breaks the simulator out with
    a failure code.
    */
    """
    ASSERT_TRUE = 0
    ASSERT_FALSE = 1
    ASSERT_NONE = 2
    ONCE_FALSE = 0
    ONCE_TRUE = 1
    ONCE_DONE = 2
    IN_ABS = 0
    IN_RATIO = 1

    def __init__(self, module):
        self.status = self.ASSERT_TRUE
        self.within = 0.0
        self.within_mode = self.IN_ABS
        self.value = 0.0
        self.once = self.ONCE_FALSE
        self.once_value = 0.0
        self.target = ""
        self.module = module

    def create(self):
        default_values = DoubleAssert(self.module)
        self.status = default_values.status
        self.within = default_values.within
        self.within_mode = default_values.within_mode
        self.value = default_values.value
        self.once = default_values.once
        self.once_value = default_values.once_value
        return 1

    def init(self, parent):
        if self.within <= 0.0:
            raise ValueError("A non-positive value has been specified for within.")
        return 1

    def commit(self, t1, t2):
        if self.once == self.ONCE_TRUE:
            self.once_value = self.value
            self.once = self.ONCE_DONE
        elif self.once == self.ONCE_DONE:
            if self.once_value == self.value:
                print("Assert skipped with ONCE logic")
                return None
            else:
                self.once_value = self.value

        target_obj = self.module.get_object(self.target)
        if target_obj is None:
            print(f"Specified target {self.target} for {self.module.get_name()} is not valid.")
            return None

        x = target_obj.get_double(self.target)
        if self.status == self.ASSERT_TRUE:
            if self.within_mode == self.IN_RATIO:
                range_val = self.value * self.within
                if range_val < 0.001:
                    range_val = 0.001
            else:
                range_val = self.within

            error = abs(x - self.value)
            if math.isnan(error) or error > range_val:
                print(f"Assert failed on {target_obj.get_name()}: {self.target} {x} not within {range_val} of given value {self.value}")
                return None

            print(f"Assert passed on {target_obj.get_name()}")
            return None
        elif self.status == self.ASSERT_FALSE:
            if self.within_mode == self.IN_RATIO:
                range_val = self.value * self.within
                if range_val < 0.001:
                    range_val = 0.001
            else:
                range_val = self.within

            error = abs(x - self.value)
            if math.isnan(error) or error < range_val:
                print(f"Assert failed on {target_obj.get_name()}: {self.target} {x} is within {range_val} of given value {self.value}")
                return None

            print(f"Assert passed on {target_obj.get_name()}")
            return None
        else:
            print(f"Assert test is not being run on {target_obj.get_name()}")
            return None

    def postnotify(self, prop, value):
        if self.once == self.ONCE_DONE and prop == "value":
            self.once = self.ONCE_TRUE
        return 1

# Example usage:
# module = YourModule()  # Replace with your module implementation
# double_assert = DoubleAssert(module)
# double_assert.status = DoubleAssert.ASSERT_TRUE
# double_assert.target = "my_property"
# double_assert.value = 42.0
# double_assert.within = 0.1
# double_assert.within_mode = DoubleAssert.IN_ABS
# double_assert.init(None)
# double_assert.commit(None, None)
