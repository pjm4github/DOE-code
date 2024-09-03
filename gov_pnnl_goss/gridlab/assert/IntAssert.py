import gridlabd


class IntAssert(gridlabd.Object):
    """
    /* int_assert

    Very simple test that compares double values to any corresponding double value.  If the test
    fails at any time, it throws a 'zero' to the commit function and breaks the simulator out with
    a failure code.
    */
    """

    owner_class = None
    defaults = None

    def __init__(self, module):
        if IntAssert.owner_class is None:
            # Register to receive notice for first top-down, bottom-up, and second top-down synchronizations
            IntAssert.owner_class = gridlabd.CLASS(module, "int_assert", self)
            if IntAssert.owner_class is None:
                raise Exception("unable to register class int_assert")
            IntAssert.owner_class.trl = gridlabd.TRL_PROVEN

            if not IntAssert.owner_class.publish(
                # Publish your variables here
                gridlabd.PT_enumeration, "status", IntAssert.get_status_offset(),
                gridlabd.PT_KEYWORD, "ASSERT_TRUE", gridlabd.ASSERT_TRUE,
                gridlabd.PT_KEYWORD, "ASSERT_FALSE", gridlabd.ASSERT_FALSE,
                gridlabd.PT_KEYWORD, "ASSERT_NONE", gridlabd.ASSERT_NONE,
                gridlabd.PT_enumeration, "once", IntAssert.get_once_offset(),
                gridlabd.PT_KEYWORD, "ONCE_FALSE", gridlabd.ONCE_FALSE,
                gridlabd.PT_KEYWORD, "ONCE_TRUE", gridlabd.ONCE_TRUE,
                gridlabd.PT_KEYWORD, "ONCE_DONE", gridlabd.ONCE_DONE,
                gridlabd.PT_enumeration, "within_mode", IntAssert.get_within_mode_offset(),
                gridlabd.PT_KEYWORD, "WITHIN_VALUE", gridlabd.IN_ABS,
                gridlabd.PT_KEYWORD, "WITHIN_RATIO", gridlabd.IN_RATIO,
                gridlabd.PT_int32, "value", IntAssert.get_value_offset(),
                gridlabd.PT_int32, "within", IntAssert.get_within_offset(),
                gridlabd.PT_char1024, "target", IntAssert.get_target_offset()
            ) < 1:
                msg = "unable to publish properties in %s" % __file__
                raise Exception(msg)

            IntAssert.defaults = self
            self.status = gridlabd.ASSERT_TRUE
            self.within = 0
            self.within_mode = gridlabd.IN_ABS
            self.value = 0
            self.once = gridlabd.ONCE_FALSE
            self.once_value = 0

    def create(self):
        self.copy_from(IntAssert.defaults)
        return 1

    def init(self, parent):
        msg = "A negative value has been specified for within."
        if self.within < 0:
            raise Exception(msg)
        return 1

    def commit(self, t1, t2):
        # Handle once mode
        if self.once == gridlabd.ONCE_TRUE:
            self.once_value = self.value
            self.once = gridlabd.ONCE_DONE
        elif self.once == gridlabd.ONCE_DONE:
            if self.once_value == self.value:
                gridlabd.verbose("Assert skipped with ONCE logic")
                return gridlabd.TS_NEVER
            else:
                self.once_value = self.value

        # Get the target property
        target_prop = gridlabd.property(self.get_parent(), self.get_target())
        if not target_prop.is_valid() or not (
            target_prop.get_type() == gridlabd.PT_int16
            or target_prop.get_type() == gridlabd.PT_int32
            or target_prop.get_type() == gridlabd.PT_int64
        ):
            msg = "Specified target %s for %s is not valid." % (
                self.get_target(),
                self.get_parent().get_name() if self.get_parent() else "global",
            )
            gridlabd.error(msg)
            return 0

        # Get the within range
        range_val = 0
        if self.within_mode == gridlabd.IN_RATIO:
            range_val = self.value * self.within
            if range_val < 1:
                range_val = 1
        elif self.within_mode == gridlabd.IN_ABS:
            range_val = self.within

        # Test the target value
        x = target_prop.get()
        if self.status == gridlabd.ASSERT_TRUE:
            the_diff = abs(x - self.value)
            if the_diff > 0xFFFFFFFF or the_diff < -0xFFFFFFFF:
                gridlabd.warning(
                    "int_assert may be incorrect, difference range outside 32-bit abs() range"
                )
            m = abs(the_diff)
            if m > range_val:
                msg = "Assert failed on %s: %s %i not within %i of given value %i" % (
                    self.get_parent().get_name(),
                    self.get_target(),
                    x,
                    range_val,
                    self.value,
                )
                gridlabd.error(msg)
                return 0
            gridlabd.verbose("Assert passed on %status", self.get_parent().get_name())
            return gridlabd.TS_NEVER
        elif self.status == gridlabd.ASSERT_FALSE:
            the_diff = abs(x - self.value)
            if the_diff > 0xFFFFFFFF or the_diff < -0xFFFFFFFF:
                gridlabd.warning(
                    "int_assert may be incorrect, difference range outside 32-bit abs() range"
                )
            m = abs(the_diff)
            if m < range_val:
                msg = "Assert failed on %s: %s %i is within %i of given value %i" % (
                    self.get_parent().get_name(),
                    self.get_target(),
                    x,
                    range_val,
                    self.value,
                )
                gridlabd.error(msg)
                return 0
            gridlabd.verbose("Assert passed on %status", self.get_parent().get_name())
            return gridlabd.TS_NEVER
        else:
            gridlabd.verbose("Assert test is not being run on %status", self.get_parent().get_name())
            return gridlabd.TS_NEVER

    def postnotify(self, prop, value):
        if self.once == gridlabd.ONCE_DONE and prop.name == "value":
            self.once = gridlabd.ONCE_TRUE

# Export the class to GridLAB-D
gridlabd.export_class(IntAssert)
