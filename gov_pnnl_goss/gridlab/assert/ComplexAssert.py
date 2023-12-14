import math


class ComplexAssert:
    """
    /* complex_assert

    Very simple test that compares complex values to any corresponding complex value.  It breaks the
    tests down into a test for the real value and a test for the imagniary portion.  If either test
    fails at any time, it throws a 'zero' to the commit function and breaks the simulator out with
    a failure code.
    */

    """
    def __init__(self):
        self.status = 'ASSERT_TRUE'
        self.within = 0.0
        self.value = 0.0
        self.once = 'ONCE_FALSE'
        self.once_value = 0
        self.operation = 'FULL'
        self.target = ''

    def init(self, parent):
        if self.within <= 0.0:
            raise ValueError("A non-positive value has been specified for within.")
        return 1

    def commit(self, t1, t2):
        if self.once == 'ONCE_TRUE':
            self.once_value = self.value
            self.once = 'ONCE_DONE'
        elif self.once == 'ONCE_DONE':
            if self.once_value.real == self.value.real and self.once_value.imag == self.value.imag:
                print("Assert skipped with ONCE logic")
                return None
            else:
                self.once_value = self.value

        # Simulate getting the target property
        x = self.get_target_value()

        if self.status == 'ASSERT_TRUE':
            if self.operation in ('FULL', 'REAL', 'IMAGINARY'):
                error = x - self.value
                real_error = error.real
                imag_error = error.imag
                if (math.isnan(real_error) or abs(real_error) > self.within) and (self.operation in ('FULL', 'REAL')):
                    print(f"Assert failed: Real part of {self.target} {x.real} not within {self.within} of given value {self.value.real}")
                    return None
                if (math.isnan(imag_error) or abs(imag_error) > self.within) and (self.operation in ('FULL', 'IMAGINARY')):
                    print(f"Assert failed: Imaginary part of {self.target} {x.imag} not within {self.within} of given value {self.value.imag}")
                    return None
            elif self.operation == 'MAGNITUDE':
                magnitude_error = abs(abs(x) - abs(self.value))
                if math.isnan(magnitude_error) or magnitude_error > self.within:
                    print(f"Assert failed: Magnitude of {self.target} ({abs(x)}) not within {self.within} of given value {abs(self.value)}")
                    return None
            elif self.operation == 'ANGLE':
                angle_error = abs(math.phase(x) - math.phase(self.value))
                if math.isnan(angle_error) or angle_error > self.within:
                    print(f"Assert failed: Angle of {self.target} ({math.degrees(math.phase(x))} degrees) not within {self.within} of given value {math.degrees(math.phase(self.value))} degrees")
                    return None
            print(f"Assert passed on {self.target}")
            return None
        elif self.status == 'ASSERT_FALSE':
            if self.operation in ('FULL', 'REAL', 'IMAGINARY'):
                error = x - self.value
                real_error = error.real
                imag_error = error.imag
                if (math.isnan(real_error) or abs(real_error) < self.within) and (self.operation in ('FULL', 'REAL')):
                    print(f"Assert failed: Real part of {self.target} {x.real} is within {self.within} of given value {self.value.real}")
                    return None
                if (math.isnan(imag_error) or abs(imag_error) < self.within) and (self.operation in ('FULL', 'IMAGINARY')):
                    print(f"Assert failed: Imaginary part of {self.target} {x.imag} is within {self.within} of given value {self.value.imag}")
                    return None
            elif self.operation == 'MAGNITUDE':
                magnitude_error = abs(abs(x) - abs(self.value))
                if math.isnan(magnitude_error) or magnitude_error < self.within:
                    print(f"Assert failed: Magnitude of {self.target} {abs(x)} is within {self.within} of given value {abs(self.value)}")
                    return None
            elif self.operation == 'ANGLE':
                angle_error = abs(math.phase(x) - math.phase(self.value))
                if math.isnan(angle_error) or angle_error < self.within:
                    print(f"Assert failed: Angle of {self.target} {math.degrees(math.phase(x))} degrees is within {self.within} of given value {math.degrees(math.phase(self.value))} degrees")
                    return None
            print(f"Assert passed on {self.target}")
            return None

    def postnotify(self, prop, value):
        if self.once == 'ONCE_DONE' and prop == 'value':
            self.once = 'ONCE_TRUE'
        return 1

    def get_target_value(self):
        # Simulate getting the target property value, replace with your implementation
        return 0.0  # Replace this with the actual value

# Example usage:
# complex_assert = ComplexAssert()
# complex_assert.status = 'ASSERT_TRUE'
# complex_assert.target = 'my_complex_number'
# complex_assert.value = 3 + 4j
# complex_assert.within = 0.1
# complex_assert.operation = 'FULL'
# complex_assert.init(None)
# complex_assert.commit(None, None)
