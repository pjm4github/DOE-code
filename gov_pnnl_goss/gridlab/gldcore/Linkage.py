

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
class Linkage:
    def create_writer(self, inst, from_obj, from_var, to_obj, to_var):
        pass

    def create_reader(self, inst, from_obj, from_var, to_obj, to_var):
        pass

    def master_to_slave(self, buffer, lnk):
        pass

    def slave_to_master(self, buffer, lnk):
        pass

    def init(self, inst, lnk):
        pass


def linkage_create_writer(inst, fromobj, fromvar, toobj, tovar):
    # allocate linkage
    lnk = linkage()
    if not lnk:
        output_error("unable to allocate memory for linkage %s:%s -> %s:%s", fromobj, fromvar, toobj, tovar)
        return 0
    memset(lnk, 0, sizeof(linkage))
    lnk.global_property_types = LT_MASTERTOSLAVE

    # copy local info
    lnk.local.obj = fromobj
    lnk.local.prop = fromvar

    # copy remote info
    lnk.remote.obj = toobj
    lnk.remote.prop = tovar

    # attach to instance cache
    if not instance_add_linkage(inst, lnk):
        output_error("unable to attach linkage %s:%s -> %s:%s to instance %s", lnk.local.obj, lnk.local.prop, lnk.remote.obj, lnk.remote.prop, inst.model)
        return 0
    else:
        output_verbose("created write linkage from local %s:%s to remote %s:%s", fromobj, fromvar, toobj, tovar)
        return 1

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def linkage_create_reader(inst, from_obj, from_var, to_obj, to_var):
    # allocate linkage
    lnk = Linkage()
    if not lnk:
        output_error("unable to allocate memory for linkage %s:%s <- %s:%s" % (from_obj, from_var, to_obj, to_var))
        return 0
    lnk.type = LT_SLAVETOMASTER

    # copy local info
    lnk.local.obj = to_obj
    lnk.local.prop = to_var

    # copy remote info
    lnk.remote.obj = from_obj
    lnk.remote.prop = from_var

    # attach to instance cache
    if not instance_add_linkage(inst, lnk):
        output_error("unable to attach linkage %s:%s <- %s:%s to instance %s" % (lnk.local.obj, lnk.local.prop, lnk.remote.obj, lnk.remote.prop, inst.model))
        return 0
    else:
        output_verbose("created read linkage from local %s:%s to remote %s:%s" % (from_obj, from_var, to_obj, to_var))
        return 1


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def status_linkage_master_to_slave(buffer, lnk):
    rv = 0
    size = 0

    # output_debug("linkage_master_to_slave")

    # null checks
    if lnk == 0:
        output_error("linkage_master_to_slave has null lnk pointer")
        return "FAILED"
    if lnk.target.obj == 0:
        output_error("linkage_master_to_slave has null lnk->target.self pointer")
        return "FAILED"
    size = int(property_minimum_buffersize(lnk.target.prop))
    if global_multirun_mode == "MRM_MASTER":
        # rv = class_property_to_string(lnk.target.prop,GETADDR(lnk.target.self,lnk.target.prop),(char *)((int64)lnk.addr),size)
        rv = object_get_value_by_addr(lnk.target.obj, GETADDR(lnk.target.obj, lnk.target.prop), 
                                      (int64(lnk.addr)), size, lnk.target.prop)
        output_debug("prop %s, addr %x, addr2 %x, val %s", lnk.target.prop.name, 
                     GETADDR(lnk.target.obj, lnk.target.prop), (int64(lnk.addr)), lnk.addr)
    elif global_multirun_mode == "MRM_SLAVE":
        # rv = class_string_to_property(lnk.target.prop,GETADDR(lnk.target.self,lnk.target.prop),(char *)((int64)lnk.addr))
        rv = object_set_value_by_addr(lnk.target.obj, GETADDR(lnk.target.obj, lnk.target.prop), 
                                      (int64(lnk.addr)), lnk.target.prop)
        output_debug("prop %s, addr %x, addr2 %x, val %s", lnk.target.prop.name, 
                     GETADDR(lnk.target.obj, lnk.target.prop), (int64(lnk.addr)), lnk.addr)
    else:
        pass
    if rv == 0:
        output_error("linkage_master_to_slave failed for link %s.%s", lnk.target.obj.name, lnk.target.prop.name)
        output_debug("str=%8s", (int64(lnk.addr)))
        return "FAILED"
    return "SUCCESS"


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def status_linkage_slave_to_master(buffer, lnk):
    rv = 0
    size = property_minimum_buffersize(lnk.target.prop)

    # null checks
    if lnk is None:
        output_error("linkage_master_to_slave has null lnk pointer")
        return "FAILED"
    if lnk.target.obj is None:
        output_error("linkage_master_to_slave has null lnk->target.self pointer")
        return "FAILED"
    
    if global_multirun_mode == "MRM_MASTER":
        rv = object_set_value_by_addr(lnk.target.obj, GETADDR(lnk.target.obj, lnk.target.prop), str(int64(lnk.addr)), lnk.target.prop)
        output_debug("prop %s, addr %x, addr2 %x, val %s", lnk.target.prop.name, GETADDR(lnk.target.obj, lnk.target.prop), str(int64(lnk.addr)), lnk.addr)
    elif global_multirun_mode == "MRM_SLAVE":
        rv = object_get_value_by_addr(lnk.target.obj, GETADDR(lnk.target.obj, lnk.target.prop), str(int64(lnk.addr)), size, lnk.target.prop)
        output_debug("prop %s, addr %x, addr2 %x, val %s", lnk.target.prop.name, GETADDR(lnk.target.obj, lnk.target.prop), str(int64(lnk.addr)), lnk.addr)
    
    if rv == 0:
        output_error("linkage_slave_to_master failed for link %s.%s", lnk.target.obj.name, lnk.target.prop.name)
        output_debug("str=%8s", str(int64(lnk.addr)))
        return "FAILED"
    return "SUCCESS"


def linkage_init(instance, lnk):
    # find local object
    lnk.target.obj = object_find_name(lnk.local.obj)
    if not lnk.target.obj:
        output_error("unable to find linkage source object '%s'" % lnk.local.obj)
        return "FAILED"

    # find local property
    lnk.target.prop = object_get_property(lnk.target.obj, lnk.local.prop, None)
    if not lnk.target.prop:
        output_error("unable to find linkage source property '%s' in object '%s'" % (lnk.local.prop, lnk.local.obj))
        return "FAILED"

    # calculate buffer size
    lnk.prop_size = property_minimum_buffersize(lnk.target.prop)
    lnk.name_size = len(lnk.remote.obj) + len(lnk.remote.prop) + 2
    lnk.size = lnk.name_size + lnk.prop_size

    output_verbose("initialized linkage between local %s:%s and remote %s:%s" % (lnk.local.obj, lnk.local.prop, lnk.remote.obj, lnk.remote.prop))
    return "SUCCESS"