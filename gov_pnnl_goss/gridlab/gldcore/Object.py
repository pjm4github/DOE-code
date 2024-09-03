import math
import re
import threading
import time
from datetime import datetime
from enum import Enum
from typing import Any, List
import xml.etree.ElementTree as ET

import numpy as np


from gridlab.gldcore.Class import PASSCONFIG, DynamicClass, ClassRegistry
from gridlab.gldcore.Exec import Exec
from gridlab.gldcore.GridLabD import TS_ZERO
from gridlab.gldcore.Platform import QNAN
from gridlab.gldcore.PropertyHeader import Keyword, PropertyMap, PropertyStruct, PropertyType, PropertyAccess, PropertSpec, PropertyFlags
from gridlab.gldcore.TimeStamp import TS_NEVER, TimeStamp, TS_INVALID, TS_MAX, is_soft_timestamp, timestamp_get_part


class Profiler:
    def __init__(self):
        self.count = 0
        self.clocks = 0
        self.lock = threading.Lock()


# Object flags
class OBJECT_FLAG(Enum):
    OF_NONE = 0x0000  # Object flag; none set
    OF_HASPLC = 0x0001  # Object flag; external PLC is attached, disables local PLC
    OF_LOCKED = 0x0002  # Object flag; data write pending, reread recommended after lock clears
    OF_RECALC = 0x0008  # Object flag; recalculation of derived values is needed
    OF_FOREIGN = 0x0010  # Object flag; indicates that object was created in a DLL and memory cannot be freed by core
    OF_SKIPSAFE = 0x0020  # Object flag; indicates that skipping updates is safe
    OF_DELTAMODE = 0x0040  # Object flag; indicates that delta mode is enabled on this object
    OF_FORECAST = 0x0040  # Object flag; indicates that the object has a valid forecast available
    OF_DEFERRED = 0x0080  # Object flag; indicates that the object started to be initialized, but requested deferral
    OF_INIT = 0x0100  # Object flag; indicates that the object has been successfully initialized
    OF_RERANK = 0x4000  # Internal use only

SUCCESS = 1
FAILURE = 0
global_debug_output = True  # Assuming a global flag for debug output

class OPI_PROFILEITEM(Enum):
    OPI_PRESYNC = 1
    OPI_SYNC = 2
    OPI_POSTSYNC = 3
    OPI_INIT = 4
    OPI_HEARTBEAT = 5
    OPI_PRECOMMIT = 6
    OPI_COMMIT = 7
    OPI_FINALIZE = 8
    # add profile items here
    _OPI_NUMITEMS = 9


oflags= [ # "name", value, next */
    Keyword("NONE", OBJECT_FLAG.OF_NONE, 1),
    Keyword("HASPLC", OBJECT_FLAG.OF_HASPLC, 2),
    Keyword("LOCKED", OBJECT_FLAG.OF_LOCKED, 3),
    Keyword("RERANKED", OBJECT_FLAG.OF_RERANK, 4),
    Keyword("RECALC", OBJECT_FLAG.OF_RECALC, 5),
    Keyword("DELTAMODE", OBJECT_FLAG.OF_DELTAMODE, None),
]


oaccess= [
    Keyword("PUBLIC", PropertyAccess.PA_PUBLIC, 1),
    Keyword("REFERENCE", PropertyAccess.PA_REFERENCE, 2),
    Keyword("PROTECTED", PropertyAccess.PA_PROTECTED, 3),
    Keyword("PRIVATE", PropertyAccess.PA_PRIVATE, None)
]


next_object_id = 0
deleted_object_count = 0
object_array_size = 0

global_profiler = Profiler()
global_profiler_enabled = 1

# Placeholder for global variables
global_skipsafe = 0
global_maximum_synctime = 30  # Assuming a maximum sync time, adjust as needed

global_no_balance = False  # Assuming a global variable to control balancing

global_relax_naming_rules = False  # Global variable controlling naming rules

global_multirun_mode = 'MRM_STANDALONE'  # Simulating global mode indicator
global_threadcount = 1  # Simulating global thread count

class OBJECTTREE:
    def __init__(self, name, obj, before=None, after=None, balance=0):
        self.name = name
        self.obj = obj
        self.before = before
        self.after = after
        self.balance = balance  # Unused, but included for completenes

top: [OBJECTTREE, None] = None  # Global variable representing the top of the tree


def debug_traverse_tree(tree=None):
    """
    Example usage:
    Assuming you've built a binary tree structure by creating ObjectTree instances and linking them via the before and after attributes.
    top = ObjectTree("RootNode", obj)  # obj is an instance of another class you've defined
    Now you can call debug_traverse_tree() to print out the names of all nodes in the tree in a sorted order.
    :param tree:
    :return:
    """
    global top
    if tree is None:
        tree = top
        if top is None:
            return
    if tree.before is not None:
        debug_traverse_tree(tree.before)
    print(tree.name)  # Assuming output_test("%s", tree->name); is a placeholder for printing the name
    if tree.after is not None:
        debug_traverse_tree(tree.after)

def tree_get_height(tree):
    """
    If the current node (tree) is None, it returns 0, indicating that the height of an empty tree is 0.
    Otherwise, it recursively calculates the height of the left and right subtrees.
    It then returns the greater of the two heights plus 1 to account for the current node.

    Example usage:
    Assuming a tree structure has been created with instances of ObjectTree.
    root = ObjectTree("Root")
    root.before = ObjectTree("Left")
    root.after = ObjectTree("Right")
    root.before.before = ObjectTree("Left-Left")
    The tree looks like:
          Root
         /    \
      Left   Right
      /
    Left-Left
    :param tree:
    :return:
    """
    if tree is None:
        return 0
    else:
        left_height = tree_get_height(tree.before)
        right_height = tree_get_height(tree.after)
        return max(left_height, right_height) + 1

def rotate_tree_right(tree):
    """
    Checks if the tree or its left child is None. If so, it simply returns the original tree since a rotation cannot be performed.
    It then performs the right rotation by reassigning the appropriate child references.
    It returns the new root of the subtree after the rotation, which callers can use to update their references if necessary.

    Example usage
    Constructing a simple tree to demonstrate right rotation
        root = ObjectTree("Root")
        left_child = ObjectTree("LeftChild")
        root.before = left_child  # 'before' is used as the left child
        left_child.after = ObjectTree("LeftChildRight")  # 'after' is used as the right child

        # Rotate the tree right around the root
        new_root = rotate_tree_right(root)

        print(f"New root after right rotation: {new_root.name}")
    :param tree:
    :return:
    """
    if tree is None or tree.before is None:
        return tree

    root = tree
    pivot = root.before
    child = pivot.after

    # Perform the rotation
    pivot.after = root
    root.before = child

    # Adjust balance factors if needed
    root.balance += 2
    pivot.balance += 1

    return pivot  # New root after rotation

def rotate_tree_left(tree):
    """
    It checks if the tree or its right child is None. If so, it returns the original tree, as a rotation cannot be performed.
    It performs the left rotation by reassigning the appropriate child references.
    It returns the new root of the subtree after the rotation, which callers can use to update their references accordingly.

    Example usage
    Constructing a simple tree to demonstrate left rotation
        root = ObjectTree("Root")
        right_child = ObjectTree("RightChild")
        root.after = right_child  # 'after' is used as the right child
        right_child.before = ObjectTree("RightChildLeft")  # 'before' is used as the left child

    Rotate the tree left around the root
        new_root = rotate_tree_left(root)

        print(f"New root after left rotation: {new_root.name}")
    :param tree:
    :return:
    """
    if tree is None or tree.after is None:
        return tree

    root = tree
    pivot = root.after
    child = pivot.before

    # Perform the rotation
    pivot.before = root
    root.after = child

    # Adjust balance factors if needed
    root.balance -= 2
    pivot.balance -= 1

    return pivot  # New root after rotation


def object_tree_rebalance(tree):
    # Rebalance the tree to make searching more efficient
    # 	It's a good idea to this after the tree is built
    #       currently being done during insertions & deletions
    return 0


def addto_tree(tree, item):
    """
    Adds a new item to tree
    Recursively finds the correct location to insert the new item based on alphabetical order of the names.
    Directly returns the new item if the place where it should be inserted is None, effectively inserting the item.
    Adjusts the tree's balance after insertion and performs necessary rotations to maintain the binary search tree
    balanced if global_no_balance is not set.
    Assuming OBJECTTREE class, rotate_tree_left, rotate_tree_right,
    and tree_get_height functions are defined as before
    :param tree:
    :param item:
    :return: the "correct" root node for the subtree that an object was added to.
    """
    if tree is None:
        return item

    rel = (tree.name > item.name) - (tree.name < item.name)
    if rel > 0:
        if tree.before is None:
            tree.before = item
        else:
            addto_tree(tree.before, item)
    elif rel < 0:
        if tree.after is None:
            tree.after = item
        else:
            addto_tree(tree.after, item)
    else:
        return tree.obj == item.obj

    if global_no_balance:
        return

    # Check balance and perform rotations if necessary
    right_height = tree_get_height(tree.after)
    left_height = tree_get_height(tree.before)
    tree.balance = right_height - left_height

    # Rotations needed?
    if tree.balance > 1:
        if tree.after.balance < 0:  # Inner left is heavy
            tree.after = rotate_tree_right(tree.after)
        tree = rotate_tree_left(tree)
    elif tree.balance < -1:
        if tree.before.balance > 0:  # Inner right is heavy
            tree.before = rotate_tree_left(tree.before)
        tree = rotate_tree_right(tree)

    return tree


def object_tree_add(obj, name):
    """
    Add an object to the object tree.
	Returns the object tree item if successful, or fails because name already used

    :param obj:
    :param name:
    :return:
    """
    global top
    item = OBJECTTREE(obj, name)

    if top is None:
        top = item
        return top
    else:
        # Assume addto_tree modifies the tree in place and returns True on success, False otherwise
        if addto_tree(top, item):
            return item
        else:
            # In Python, it's more common to raise an exception than to return None for this kind of error
            raise ValueError(f"Object with name '{name}' already exists in the tree.")


def findin_tree(tree, name):
    """
    Recursively searches the binary tree for a node with the given name, traversing left or right as needed based on
    string comparison.
    Returns a direct reference to the ObjectTree instance with the matching name, or None if no match is found. This
    behavior mirrors the C++ version's goal of returning a pointer to the matching node or NULL if not found,
    adapted to Python's reference and object model.
    Eliminates the need for double pointers or manual memory management, leveraging Python's garbage collection and
    dynamic typing for simplicity and readability.

    Example usage:
    Assuming a binary search tree of ObjectTree instances has been created
        root = ObjectTree("RootNode")
    ... (add nodes to the tree)
    To find a node with a specific name:
        result = findin_tree(root, "TargetNodeName")
        if result:
            print(f"Found node: {result.name}")
        else:
            print("Node not found.")
    :param tree:
    :param name:
    :return:
    """
    if tree is None:
        return None
    else:
        rel = (tree.name > name) - (tree.name < name)
        if rel > 0:
            # Name should be in the left subtree
            return findin_tree(tree.before, name)
        elif rel < 0:
            # Name should be in the right subtree
            return findin_tree(tree.after, name)
        else:
            # Found the node with the matching name
            return tree


def object_tree_delete(tree: OBJECTTREE, name: str) -> OBJECTTREE:
    """
    This implements the delete operation using helper functions to find the parent of the node to delete
    and to carry out the deletion process. The find_parent function traverses the tree to find the parent of
    the node with the given name, and delete_node handles the deletion logic, including the cases where the
    node to delete has no children, one child, or two children.

    Example usage:
    Assuming 'top' is the root of your binary search tree
    and 'name' is the name of the node you wish to delete:
        object_tree_delete(top, 'name_to_delete')

    :param tree:
    :param name:
    :return: The tree after the named node is deleted
    """
    def find_parent(node, name):
        """Helper function to find the parent node of the node to delete."""
        if node is None:
            return None, None
        elif (node.before and node.before.name == name) or (node.after and node.after.name == name):
            return node, None
        elif node.name > name:
            return find_parent(node.before, name)
        else:
            return find_parent(node.after, name)

    def delete_node(parent, name):
        """Deletes the node from the tree."""
        direction = 'before' if parent.before and parent.before.name == name else 'after'
        node = getattr(parent, direction)

        # Node with no children
        if node.before is None and node.after is None:
            setattr(parent, direction, None)
        # Node with two children
        elif node.before and node.after:
            # Find the rightmost node in the left subtree
            replacement_parent = node
            replacement = node.before
            while replacement.after:
                replacement_parent = replacement
                replacement = replacement.after

            # Replace node with the rightmost node
            if replacement_parent != node:
                replacement_parent.after = replacement.before
                replacement.before = node.before
            replacement.after = node.after
            setattr(parent, direction, replacement)
        # Node with one child
        else:
            child = node.before if node.before else node.after
            setattr(parent, direction, child)

    parent, _ = find_parent(tree, name)
    if parent:
        delete_node(parent, name)
    else:
        # Handle the case where the tree itself is the node to delete
        if tree and tree.name == name:
            if tree.before and tree.after:
                # Complex case: node with two children
                # Similar logic to 'Node with two children' above
                pass  # Implement if needed
            else:
                # Simpler cases can be handled directly
                replacement = tree.before if tree.before else tree.after
                tree.name = replacement.name if replacement else None
                tree.obj = replacement.obj if replacement else None
                tree.before = replacement.before if replacement else None
                tree.after = replacement.after if replacement else None

    return tree

# class Namespace:
#     def __init__(self, name, next=None):
#         self.name = name
#         self.next = next


class Object:
    """
    Object functions support object operations.  Objects have two parts, an #OBJECTHDR
    block followed by an #OBJECTDATA block.  The #OBJECTHDR contains all the common
    object information, such as its id and clock.  The #OBJECTDATA contains all the
    data implemented by the module that created the object.

    OBJECTHDR		size						the size of the OBJECTDATA block
                    id							unique id of the object
                    owner_class						class the implements the OBJECTDATA
                    next						pointer to the next OBJECTHDR
                    parent						pointer to parent's OBJECTHDR
                    rank						object's rank (less than parent's rank)
                    clock						object's sync clock
                    latitude, longitude			object's geo-coordinates
                    in_svc, out_svc				object's activation/deactivation dates
                    flags						object flags (e.g., external PLC active)
    OBJECTDATA		(varies; defined by owner_class)
    """
    namespace = {'current': None, 'next': None}
    global_object_array: list = [] # an ordered list of object items
    _global_next_object_id: int = 0

    def __init__(self, id, owner_class, name, groupid=None, next_object=None, parent=None, child_count=0, rank=None,
                 clock=None, valid_to=None, schedule_skew=None, forecast=None, latitude=0.0, longitude=0.0,
                 in_svc=0, out_svc=0, in_svc_micro=0, out_svc_micro=0, in_svc_double=0.0,
                 out_svc_double=0.0, synctime=None, space=None, lock=None, rng_state=0, heartbeat=0, flags=None):
        self.child_count = child_count  # number of objects that have this object as a parent
        self.clock = datetime.now() if clock is None else clock  # object's private clock
        self.flags = set() if flags is None else flags  # object flags
        self.forecast = forecast  # forecast data block
        self.groupid = groupid  # char32
        self.heartbeat = heartbeat  # heartbeat interval
        # When the object is created we will get a global object id by default
        Object._global_next_object_id += 1
        self._id = Object._global_next_object_id  # OBJECTNUM id; globally unique
        self.in_svc = in_svc  # in service time (see the exec module)
        self.in_svc_double = in_svc_double  # double value of in service time
        self.in_svc_micro = in_svc_micro  # microsecond portion of in service time
        self.latitude = latitude  # object's latitude
        self.lock = lock if lock else threading.RLock  # object lock
        self.longitude = longitude  # object's longitude
        self.name = name  # OBJECTNAME
        self.next = next_object  # next object in list
        self.out_svc = out_svc  # out of service time
        self.out_svc_double = out_svc_double  # double value of out of service time
        self.out_svc_micro = out_svc_micro  # microsecond portion of out of service time
        self.owner_class = owner_class  # Class pointer; determines structure of object data
        self.parent = parent  # object's parent; determines rank
        self.profiler = Profiler()
        self.properties = []
        self.rank = rank  # OBJECTRANK; object's rank
        self.rng_state = rng_state  # random number generator state
        self.schedule_skew = schedule_skew  # time skew for schedule operations
        self.space = space  # namespace of object
        self.synctime:List[int] = [0, 0] if synctime is None else synctime  # array for total time used by this object
        self.valid_to = TS_NEVER if valid_to is None else valid_to # object's valid-until time

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        print(f"the id: {val} should not be set, it is set to {self._id} during instantiation")
        # self._id = val

    @property
    def first_object(cls):
        """The getter method for the first object property."""
        return Object.global_object_array[0] if Object.global_object_array else None

    @first_object.setter
    def first_object(cls, obj):
        """Instance-level setter for the first object of the global list."""
        if Object.global_object_array:
            Object.global_object_array.insert(0, obj)
        else:
            Object.global_object_array.append(obj)

    @property
    def last_object(self):
        """Instance-level getter for the last item of the global list."""
        return Object.global_object_array[-1] if Object.global_object_array else None

    @last_object.setter
    def last_object(self, obj):
        """Instance-level setter for the last item of the global list."""
        if obj in Object.global_object_array:
            print(f"{obj} is already in the global list.")
        Object.global_object_array.append(obj)

    @staticmethod
    def convert_from_latitude(v) -> [None, int]:
        if math.isnan(v):
            return None

        d = math.floor(abs(v))
        r = abs(v) - d
        m = math.floor(r * 60.0)
        s = (r - m / 60.0) * 3600.0
        ns = 'S' if v < 0 else 'N'

        return f"{d}{ns}{m}:{s:.2f}"

    @staticmethod
    def convert_from_longitude(v) -> [None, int]:
        if math.isnan(v):
            return None

        d = math.floor(abs(v))
        r = abs(v) - d
        m = math.floor(r * 60)
        s = (r - m / 60.0) * 3600
        ew = 'W' if v < 0 else 'E'

        return f"{d}{ew}{m}:{s:.2f}"

    @staticmethod
    def convert_from_object(oname):
        pass

    @staticmethod
    def convert_from_set(data, prop) -> (int, str):
        """
        Converts a set property to a string.
    .
        :param data: A pointer to the data.
        :param prop: A pointer to keywords that are supported.
        :return: The number of characters written to the string and the string
        """
        SETDELIM = "|"
        value = data
        ISZERO = (value == 0)
        filtered_keys = []
        for keys in prop.keywords:
            if (not ISZERO and keys.value != 0 and (keys.value & value) == keys.value) or (keys.value == 0 and ISZERO):
                value &= ~keys.value
                filtered_keys.append(f"{keys.name}={keys.value}")

        buffer = SETDELIM.join(filtered_keys)
        return len(buffer), buffer

    @staticmethod
    def convert_to_set(buffer, data, prop):
        """
        Converts a string to a set property.

        :param buffer: A pointer to the string buffer.
        :param data: A pointer to the data.
        :param prop: A pointer to keywords that are supported.
        :return: Number of values read on success, 0 on failure, -1 if conversion was incomplete.
        """
        SETDELIM = "|"
        keys = prop.keywords
        temp = ""
        ptr = ""
        value = 0
        count = 0

        if buffer.startswith("0x"):
            return int(buffer[2:], 16)
        elif buffer.isdigit():
            return int(buffer)

        if len(buffer) > len(temp) - 1:
            return 0

        temp = buffer

        if (prop.flags & PropertyFlags.PF_CHARSET) and "|" not in buffer:
            for ptr in buffer:
                found = False
                for key in keys:
                    if ptr == key.name[0]:
                        value |= key.value
                        count += 1
                        found = True
                        break
                if not found:
                    print(f"set member '{ptr}' is not a keyword of property {prop.name}")
                    return 0
        else:
            parts = temp.split(SETDELIM)
            for ptr in parts:
                found = False
                for key in keys:
                    if ptr == key.name:
                        value |= key.value
                        count += 1
                        found = True
                        break
                if not found:
                    print(f"set member '{ptr}' is not a keyword of property {prop.name}")
                    return 0

        data = value
        return count

    @staticmethod
    def convert_to_latitude(buffer: str) -> float:
        # Pattern matching for degrees, minutes, and seconds with cardinal direction
        pattern_dms = re.compile(r"(\d+)([NS])?(\d*):?(\d*\.?\d*)")
        match = pattern_dms.match(buffer)

        if match:
            degrees = float(match.group(1))
            direction = match.group(2)
            minutes = float(match.group(3)) if match.group(3) else 0
            seconds = float(match.group(4)) if match.group(4) else 0

            latitude = degrees + minutes / 60.0 + seconds / 3600.0

            if direction == 'S':
                latitude = -latitude
        else:
            # Try to directly convert if it's a simple numeric value
            try:
                latitude = float(buffer)
                if latitude < 0:
                    direction = 'S'
                else:
                    direction = 'N'
            except ValueError:
                return math.nan  # Return NaN if conversion fails

        if 0.0 <= abs(latitude) <= 90.0:
            return latitude
        else:
            return math.nan

    @staticmethod
    def convert_to_longitude(buffer: str) -> float:
        # Pattern matching for degrees, minutes, and seconds with cardinal direction
        pattern_dms = re.compile(r"(\d+)([EW])?(\d*):?(\d*\.?\d*)")
        match = pattern_dms.match(buffer)

        if match:
            degrees = float(match.group(1))
            direction = match.group(2)
            minutes = float(match.group(3)) if match.group(3) else 0
            seconds = float(match.group(4)) if match.group(4) else 0

            longitude = degrees + minutes / 60.0 + seconds / 3600.0

            if direction == 'W':
                longitude = -longitude
        else:
            # Try to directly convert if it's a simple numeric value
            try:
                longitude = float(buffer)
                if longitude < 0:
                    direction = 'W'
                else:
                    direction = 'E'
            except ValueError:
                return math.nan  # Return NaN if conversion fails

        if 0.0 <= abs(longitude) <= 180.0:
            return longitude
        else:
            return math.nan

    @staticmethod
    def get_address(obj, prop):
        """
        Get the address of an object's property.
        Assumes that the 'addr' attribute of prop is an offset from the start of the object data.
        """
        return (obj + 1 + prop.addr) if obj and prop else None

    def object_access_property(self) -> dict:
        flags = {
            "access": PropertyAccess.PA_PUBLIC,
            "addr": 0,
            #  "data": None,
            #  "function_pointer": self.oaccess,
            "delegation": None,
            "description": "",
            "keywords": oaccess,
            "name": "access",
            "owner_class": 0,
            #  "other": None
            #  "pointer": id(self),
            "global_property_types": PropertyType.PT_enumeration,
            #  "precision": 8,
            "size": 1,
            #  "global_property_types": "enumeration",
            "unit": None,
            # "value": 0,
            "width": 8
        }
        return flags

    def object_build_name(self, buffer_len: int) -> str:

        name_to_use = self.name if self.name else f"{self.owner_class.name} {self.id}"

        if len(name_to_use) > buffer_len:
            raise ValueError(f"Unable to build name for '{name_to_use}', input buffer too short")

        return name_to_use

    def object_build_object_array(self):
        global object_array_size, object_array
        tcount = self.object_get_count()
        optr = self.object_get_first()
        object_array = []
        for i in range(tcount):
            object_array.append(Object(0,self.owner_class, f"{i}"))
        object_array_size = tcount
        for i in range(tcount):
            object_array[i] = optr
            optr = optr.contents.next

        return object_array_size

    def object_close_namespace(self, ) -> int:  # close the current namespace and restore the previous one */
        """
        # Example usage
            try:
                if object_close_namespace():
                    print("Namespace closed successfully.")
            except Exception as e:
                print(e)
        :return:
        """
        if not Object.namespace['next']:
            raise Exception("object_close_namespace(): no current namespace to close")
        Object.namespace = {'current': Object.namespace['next'], 'next': None}
        return 1

    def object_commit(self, t1: TimeStamp, t2: TimeStamp) -> TimeStamp:
        t = Exec.exec_clock()
        rv = TS_NEVER  # Default return value if no commit function is defined or returns "old school" indicator

        if hasattr(self.owner_class, 'commit') and callable(getattr(self.owner_class, 'commit')):
            # Directly invoke the commit method if it exists
            rv = self.owner_class.commit(self, t1, t2)
        else:
            # Handle the case where no commit method is defined
            rv = TS_NEVER

        self.object_profile(OPI_PROFILEITEM.OPI_COMMIT, t)

        if global_debug_output:
            # Simplified debug output
            dt = time.ctime(rv) if rv != TS_NEVER else "(invalid)"
            timestamp_type = "SOFT" if is_soft_timestamp(rv) else "HARD"
            debug_message = f"object {self.owner_class.name}:{self.id} commit -> {timestamp_type} {dt}"

            print(debug_message)

        return rv


    def object_create_array(self, owner_class: DynamicClass, n_objects: int):
        """
        Create multiple objects of a given class.

        :param owner_class: A reference to the class of objects to be created.
        :param n_objects: The number of objects to create.
        :return: The first object created or None if an error occurred.
        """
        first = None
        last = None  # Keep track of the last object created to maintain the chain


        for _ in range(n_objects):
            obj = self.object_create_single(owner_class)
            if obj is None:
                return None
            if first is None:
                first = obj
            if last is not None:
                last.next = obj  # Assuming 'next' attribute is used to chain objects
            last = obj

        return first

    def object_create_foreign(self, obj: DynamicClass):
        if obj is None:
            raise Exception("object_create_foreign(self=None): object is None")

        if obj.owner_class is None:
            raise Exception("object_create_foreign(self=<new>): self.owner_class is None")

        if obj.owner_class.magic != DynamicClass.CLASSVALID:
            raise Exception("object_create_foreign(self=<new>): self.owner_class is not really a class")

        obj.synctime = [0] * 64
        obj.id = next_object_id
        next_object_id += 1
        obj.next = None
        obj.name = None
        obj.parent = None
        obj.rank = 0
        obj.clock = 0
        obj.latitude = QNAN
        obj.longitude = QNAN
        obj.in_svc = TS_ZERO
        obj.in_svc_micro = 0
        obj.in_svc_double = float(obj.in_svc)
        obj.out_svc = TS_NEVER
        obj.out_svc_micro = 0
        obj.out_svc_double = float(obj.out_svc)
        obj.flags = OBJECT_FLAG.OF_FOREIGN

        if Object.first_object['id'] is None:
            Object.first_object = {'id': obj.id, 'owner_class': obj.owner_class, 'name': 'FirstObject', 'next': None}

        else:
            Object.last_object = {'id': obj.id, 'owner_class': obj.owner_class, 'name': 'FirstObject', 'previous': Object.first_object}

        last_object = obj
        obj.owner_class.profiler.numobjs += 1

        return obj

    @staticmethod
    def object_create_single(owner_class):
        # global tp_next, tp_count

        # if tp_count == 0:
        #     tp_count = processor_count()  # assuming processor_count is a defined function

        if owner_class is None:
            raise Exception("object_create_single(Class *owner_class=None): class is NULL")

        if owner_class.passconfig & PASSCONFIG.PC_ABSTRACTONLY:
            raise Exception(
                "object_create_single(Class *owner_class='%s'): abstract class '%s' cannot be instantiated" % owner_class.name)

        obj = Object(None, owner_class, None)  # allocating memory with size of OBJECT + owner_class size

        # obj.parent = None
        # obj.child_count = 0
        # obj.rank = 0
        # obj.clock = 0
        # obj.latitude = QNAN
        # obj.longitude = QNAN
        # obj.in_svc = TS_ZERO
        # obj.in_svc_micro = 0
        # obj.in_svc_double = float(obj.in_svc)
        # obj.out_svc = TS_NEVER
        # obj.out_svc_micro = 0
        # obj.out_svc_double = float(obj.out_svc)
        # obj.space = self.object_current_namespace()
        # obj.flags = OBJECT_FLAG.OF_NONE
        # obj.rng_state = randwarn  # assuming randwarn is a defined function
        # obj.heartbeat = 0



        # iterating over properties and create them
        prop = owner_class.pmap
        while prop is not None:
            prop = PropertyMap(prop, "")

            if prop.next is not None:
                prop = prop.next
            elif prop.owner_class.parent is not None:
                prop = prop.owner_class.parent.pmap
            else:
                prop = None

        if Object.first_object is None:
            Object.first_object = obj
        else:
            Object.last_object = obj

        owner_class.profiler.numobjs += 1

        return obj

    def object_current_namespace(self, ):  # #  access the current namespace */
        """
        Example usage
            current_ns = object_current_namespace()
            print("Current Namespace:", "::".join(reversed(_object_namespace(current_ns))) if current_ns else "Global")
        :return:
        """
        return Object.namespace['current']

    def object_data(self):  # todo this is broken
        """
        Get the object data structure.
        """
        return self if self else None

    def object_dump(self) -> str:
        """
        Dump an object to a string
        :return: the dump string
        """
        buffer = [f"object {self.owner_class.name}:{self.id} {{\n"]

        if self.parent is not None:
            parent_name = self.parent.name if self.parent.name else ""
            buffer.append(f"\tparent = {self.parent.owner_class.name}:{self.parent.id} ({parent_name})\n")
        else:
            buffer.append("\troot object\n")

        if self.name is not None:
            buffer.append(f"\tname {self.name}\n")

        # Assuming convert_from_timestamp is a function that formats timestamps
        # For simplicity, let's use the clock value directly
        buffer.append(f"\trank = {self.rank};\n")
        t = TimeStamp.from_timestamp(self.clock)
        buffer.append(f"\tclock = {t if t > 0 else 'invalid'} {self.clock}\n")

        if not math.isnan(self.latitude):
            buffer.append(f"\tlatitude = {self.latitude};\n")
        if not math.isnan(self.longitude):
            buffer.append(f"\tlongitude = {self.longitude};\n")

        buffer.append("\tflags = (flags);\n")
        c, flag_list = self.convert_from_set(self.flags, self.object_flag_property())

        buffer.append(f"\tflags = {flag_list if flag_list else '(invalid)'}\n")

        # Dump properties and inherited properties
        for prop in self.owner_class.pmap:
            value = self.object_property_to_string(prop)
            buffer.append(f"\t{prop} = {value};\n")

        buffer.append("}\n")
        result = ''.join(buffer)
        return result

    def object_finalize(self, ):
        """
        Finalize is the last function callback that is made for an object.  It
        provides an opportunity to close files, collate answers, come to
        conclusions, and destroy network objects.

        :return: The return value is if the function successfully completed.
        """
        t = Exec.exec_clock()
        rv = SUCCESS

        if hasattr(self.owner_class, 'finalize') and callable(getattr(self.owner_class, 'finalize')):
            rv = self.owner_class.finalize(self)
        else:
            rv = SUCCESS  # Assuming success if no finalize method is defined

        self.object_profile(OPI_PROFILEITEM.OPI_FINALIZE, t)

        if global_debug_output:
            print(f"object {self.owner_class.name}:{self.id} finalize -> {'ok' if rv else 'failed'}")
        return rv

    def object_find_by_id(self, id):
        """
        Find an object by its id number.
        :param id: object id number
        :return: the object if found, None otherwise
        """
        for obj in Object.global_object_array:
            if obj.id == id:
                return obj
        return None

    @staticmethod
    def object_find_name(name: str)->[None, 'Object']:
        """
        Example usage assuming the ObjectTree class, and the object structure have been defined
        and the binary search tree has been populated
            found_obj = object_find_name("someObjectName")
            if found_obj:
                print("Object found:", found_obj)
            else:
                print("Object not found.")
        :param name:
        :return:
        """

        global top

        def find_in_tree(tree, name):
            if tree is None:
                return None
            elif tree.name == name:
                return tree
            elif tree.name > name:
                return find_in_tree(tree.before, name)
            else:
                return find_in_tree(tree.after, name)

        item = find_in_tree(top, name)
        if item is not None:
            return item.obj
        else:
            return None


    def object_flag_property(self):
        flags = PropertyMap(
            access=PropertyAccess.PA_PUBLIC,
            addr=None,
            # "attribute": "public",
            # "callback": None,
            # "data": -4,
            # "default": 0,
            delegation=None,
            description="",
            # "field": None,
            # "function1": None,
            # "function2": oflags,
            # "function3": None,
            keys=self.object_get_oflags(),
            # "max_size": 8,
            name = "flags",
            # "next": None,
            owner_class = None,
            # "offset": -4,
            # "options": oflags,
            # "option_flags": oflags,
            # "pointer": self.id,
            property_type=PropertyType.PT_set,
            # "readable": 1,
            size=1,
            # "global_property_types": "set",
            units=None,
            # "validate": None,
            # "value": 0,
            width=8,
            #"writable": 8,
            )
        return flags

    def object_get_addr(self, name: str):
        prop = ClassRegistry.find_property(self, name)
        if prop is not None and prop.access != PropertyAccess.PA_PRIVATE:
            # In Python, instead of returning a memory address, return the value directly
            return getattr(self, prop.addr, None)
        else:
            # Python does not use errno in the same way as C; you might raise an exception or return None
            return None

    def object_get_bool(self, prop: PropertyMap) -> bool:
        if prop.property_type == PropertyType.PT_bool and prop.access != PropertyAccess.PA_PRIVATE:
            # Directly return the boolean property value
            return prop.value
        else:
            # In Python, exceptions are used instead of modifying errno
            raise ValueError("Is private, or is not of boolean global_property_types")

    def object_get_bool_by_name(self, name: str) -> bool:
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop and prop.access != 'PA_PRIVATE' and prop.global_property_types == 'PT_bool':
            # Directly access and return the attribute if it exists and is a boolean
            value = prop.value
            if isinstance(value, bool):
                return value
            else:
                raise ValueError(f"The property '{name}' is not of boolean global_property_types.")
        else:
            raise ValueError(f"PropertyMap '{name}' not found or is private.")

    def object_get_child_count(self, ) -> int:
        return self.child_count

    def object_get_complex(self, prop: PropertyMap):
        if prop is None:
            return None

        if (self.object_prop_in_class(prop) and prop.property_type == PropertyType.PT_complex
                and prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the complex property value
            return prop.value
        else:
            # Pythonic way to indicate an error is by raising an exception
            raise ValueError("PropertyMap not found, is private, or is not of global_property_types complex")

    def object_get_complex_by_name(self, name: str):

        prop = ClassRegistry.find_property(self.owner_class, name)

        if prop and prop.access != PropertyAccess.PA_PRIVATE:
            # Directly return the complex property value by name
            return prop.value
        else:
            # Pythonic way to indicate an error is by raising an exception
            raise ValueError("PropertyMap not found or is private")

    def object_get_complex_quick(self, prop: PropertyMap):
        # Assuming quick access skips checks for simplicity in Python
        return prop.value

    @staticmethod
    def object_get_count():
        return len(Object.global_object_array)

    def object_get_double(self, pObj: Any, prop: PropertyMap) -> [None, float]:
        if prop is None:
            return None

        if (self.object_prop_in_class(prop) and (
                prop.property_type in [PropertyType.PT_double, PropertyType.PT_random])
                and prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the double property value
            return prop.value
        else:
            # Pythonic way to indicate an error is by raising an exception
            raise ValueError("PropertyMap not found, is private, or is not of the correct global_property_types")

    def object_get_double_by_name(self, name: str) -> float:
        prop = ClassRegistry.find_property(self.owner_class, name)

        if prop and prop.access != PropertyAccess.PA_PRIVATE:
            # Directly return the double property value by name
            return prop.value
        else:
            # Pythonic way to indicate an error is by raising an exception
            raise ValueError("PropertyMap not found or is private")

    def object_get_double_quick(self, pObj: Any, prop: PropertyMap) -> float:
        # Assuming quick access skips checks for simplicity in Python
        return prop.value

    def object_get_enum(self, prop: PropertyMap) -> Enum:

        if (self.object_prop_in_class(prop) and prop.property_type == PropertyType.PT_enumeration
                and prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the enumeration property value
            return prop.value
        else:
            # In Python, exceptions are used instead of modifying errno
            raise ValueError("PropertyMap not found, is private, or is not an enumeration")

    def object_get_enum_by_name(self, name: str) -> Enum:
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop and prop.access != PropertyAccess.PA_PRIVATE:
            return prop.value
        else:
            raise ValueError("PropertyMap not found, is private")

    @staticmethod
    def object_get_first():
        global first_object
        return first_object

    def object_get_function(self, classname: str, functionname: str):
        pass

    def object_get_int16(self, prop: PropertyMap) -> [None, int]:
        if prop is None:
            return None

        if (self.object_prop_in_class(prop) and prop.property_type == PropertyType.PT_int16
                and prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the integer property value
            return prop.value
        else:
            # Instead of setting errno, Pythonic way is to raise an exception
            raise ValueError("PropertyMap not found, is private, or is not of global_property_types int16")

    def object_get_int16_by_name(self, name: str) -> int:
        prop = ClassRegistry.find_property(self.owner_class, name)

        if prop and prop.access != PropertyAccess.PA_PRIVATE:
            # Directly return the integer property value by name
            return prop.value
        else:
            # Instead of setting errno, Pythonic way is to raise an exception
            raise ValueError("PropertyMap not found or is private")

    def object_get_int32(self, prop: PropertyMap) -> [int, None]:
        if prop is None:
            return None

        if (Object.object_prop_in_class(self, prop) and prop.property_type == PropertyType.PT_int32
                and prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the 32-bit integer property value
            return prop.value
        else:
            # Pythonic way to indicate an error is raising an exception
            raise ValueError("PropertyMap not found, is private, or is not of global_property_types int32")

    def object_get_int32_by_name(self, name: str) -> int:
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop and prop.access != PropertyAccess.PA_PRIVATE:
            # Directly return the 32-bit integer property value by name
            return prop.value
        else:
            # Pythonic way to indicate an error is raising an exception
            raise ValueError("PropertyMap not found or is private")

    def object_get_int64(self, prop: PropertyMap) -> [int, None]:
        if prop is None:
            return None

        if (self.object_prop_in_class(prop) and prop.property_type == PropertyType.PT_int64
                and prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the 64-bit integer property value
            return prop.value
        else:
            # Pythonic way to indicate an error is by raising an exception
            raise ValueError("PropertyMap not found, is private, or is not of global_property_types int64")

    def object_get_int64_by_name(self, name: str) -> int:
        prop = ClassRegistry.find_property(self.owner_class, name)

        if prop and prop.access != PropertyAccess.PA_PRIVATE:
            # Directly return the 64-bit integer property value by name
            return prop.value
        else:
            # Pythonic way to indicate an error is by raising an exception
            raise ValueError("PropertyMap not found or is private")

    def object_get_namespace(self) -> (int, str):  # get the object's namespace */
        """
        Assuming an Object instance with a namespace
            obj = Object("MyObject", current_namespace)
            is_subspace, namespace = object_get_namespace(obj)
            print(f"Is in subspace: {is_subspace}, Namespace: {namespace}")
        :return:
        """
        if self.space:
            return 1, "::".join(reversed(self._object_namespace(self.space)))
        return 0, ""

    @staticmethod
    def object_get_next(current_obj):
        global first_object, next_object_id, object_array
        """Get the next object in the model starting from 'current_obj'."""
        if current_obj in object_array:
            current_index = object_array.index(current_obj)
            if current_index + 1 < len(object_array):
                return object_array[current_index + 1]
        return None

    def object_get_object(self, prop: PropertyMap):
        if prop is None:
            return None

        if (self.object_prop_in_class(prop) and prop.property_type == PropertyType.PT_object and
                prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the reference to the object property
            return prop.value
        else:
            # Python does not use errno in the same way as C; you might raise an exception or return None
            raise ValueError("Is private, or is not of DynamicObject global_property_types")

    def object_get_object_by_name(self, name: str):

        prop = ClassRegistry.find_property(self.owner_class, name)

        if prop and prop.access != PropertyAccess.PA_PRIVATE and prop.global_property_types == PropertyType.PT_object:
            # Directly access the attribute by name (prop.value) if it exists
            return prop.value
        else:
            # In Python, you might raise an exception or return None if the property doesn't meet the criteria
            raise ValueError("Is private, or is not found.")

    def object_get_oflags(self) -> int:
        #     flag_size = ctypes.sizeof(oflags)
        #
        #     extflags.contents = ctypes.cast(module_malloc(flag_size), ctypes.POINTER(Keyword))
        #
        #     if not extflags.contents:
        #         output_error("object_get_oflags: malloc failure")
        #         errno = ENOMEM
        #         return -1
        #
        #     ctypes.memmove(extflags.contents, oflags, flag_size)
        #
        #     return flag_size // ctypes.sizeof(Keyword)

        # flag_size = ctypes.sizeof(oflags)  # todo this is broken
        self.extflags = oflags
        # if self.extflags is None:
        #     output_error("object_get_oflags: malloc failure")
        #     errno = Class.ENOMEM
        #     return -1
        # ctypes.memcpy(extflags[0], oflags, flag_size)
        return 1

    def object_get_part(self, x: Any, name: str) -> float:
        # Direct attribute access cases
        direct_attrs = ["id", "rng_state", "latitude", "longitude", "schedule_skew"]
        if name in direct_attrs:
            return float(getattr(self, name, float('nan')))

        # Handling composite names indicating subattributes or special processing
        parts = name.split('.')
        if len(parts) == 2:
            root, part = parts
            # Define a map for special timestamp attributes that might require custom handling
            timestamp_map = {
                "clock": self.clock,
                "valid_to": self.valid_to,
                "in_svc": self.in_svc,
                "out_svc": self.out_svc,
                "heartbeat": self.heartbeat,
            }
            if root in timestamp_map:
                # Placeholder for timestamp_get_part logic
                # Assuming timestamp_get_part is a function to extract parts of a timestamp attribute
                return timestamp_get_part(timestamp_map[root], part)

        return np.nan

    def object_get_property(self, name: str, pstruct: [PropertyStruct, None] = None) -> [PropertyMap, None]:
        """
        Get a named property of an object.

        Note that you must use object_get_value_by_name to retrieve the value of the property.
        If part is specified, failed searches for given name will be parsed for a part.

        :param self: a pointer to the object
        :param name: the name of the property
        :param pstruct: buffer in which to store part info, if found
        :return: a pointer to the PropertyMap structure

        Example Usage
        class Object:
            def __init__(self, id, rng_state, latitude, longitude, schedule_skew):
                self.id = id
                self.rng_state = rng_state
                self.latitude = latitude
                self.longitude = longitude
                self.schedule_skew = schedule_skew
                # Placeholder for timestamp attributes
                self.clock = self.valid_to = self.in_svc = self.out_svc = self.heartbeat = 0

        obj = Object(1, 0, 45.0, -73.0, 0)
        print(object_get_part(obj, "latitude"))
        """
        if self is None:
            return None

        prop = ClassRegistry.find_property(self.owner_class, name)
        if pstruct:
            pstruct.prop = prop
            pstruct.part = ''

        if prop:
            return prop

        if pstruct is None:
            return None

        # possible part specified, so search for it
        if '.' in name:
            root, part = name.rsplit('.', 1)
        else:
            return None  # no part, no result

        # check the root
        prop = ClassRegistry.find_property(self.owner_class, root)
        if not prop:
            return None  # root isn't valid either

        # check part directly (note this fails if the part is valid but the value is NaN)
        spec = PropertSpec.property_getspec(prop.global_property_types)
        if not spec.get_part or spec.get_part(self, part) is None:
            return None

        # part is valid
        pstruct.prop = prop
        pstruct.part = part[:len(pstruct.part)]
        return prop

    def get_property_at_addr(self, name):
        for prop in self.owner_class.properties:
            if prop.name == name:
                if prop.access != PropertyAccess.PA_PRIVATE:
                    return prop
                else:
                    raise Exception(f"Trying to access private property {prop.name} in class {self.owner_class.name}")
        return None

    def object_get_reference(self, name: str):
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop is None or prop.access == PropertyAccess.PA_PRIVATE or prop.global_property_types != PropertyType.PT_object:
            # Handle the case where the property doesn't exist, is private, or isn't an object reference
            print("Error: PropertyMap not found, is private, or is not an object reference.")
            return None

        # Directly return the object reference
        return self.name

    def object_get_set(self, prop: PropertyMap):
        if (self.object_prop_in_class(prop) and prop.property_type == PropertyType.PT_set
                and prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the set property value
            return prop.value
        else:
            # In Python, exceptions are used instead of modifying errno
            raise ValueError("PropertyMap not found, is private, or is not a set")

    def object_get_set_by_name(self, name: str):
        prop = ClassRegistry.find_property(self, name)
        if (prop and prop.global_property_types == PropertyType.PT_set and
                prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the set property value
            return prop.value
        else:
            # In Python, exceptions are used instead of modifying errno
            raise ValueError("PropertyMap not found, is private, or is not a set")

    def object_get_string(self, pObj: Any, prop: PropertyMap) -> [str, None]:
        if prop is None:
            return None

        if (self.object_prop_in_class(prop) and prop.property_type in [PropertyType.PT_string,
                                                                       PropertyType.PT_string32]
                and prop.access != PropertyAccess.PA_PRIVATE):
            # Directly return the string property value
            return prop.value
        else:
            # Pythonic way to indicate an error is by raising an exception
            raise ValueError("PropertyMap not found, is private, or is not of the correct string global_property_types")

    def object_get_string_by_name(self, name: str) -> str:
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop and prop.access != PropertyAccess.PA_PRIVATE:
            # Directly return the string property value by name
            return prop.value
        else:
            # Pythonic way to indicate an error is by raising an exception
            raise ValueError("PropertyMap not found or is private")

    def object_get_unit(self, obj, name):
        global dimless
        prop = self.object_get_property(name, None)

        if prop is None:
            buffer = bytearray(64)
            buffer = buffer.ljust(64, b'\0')
            message = "property '{}' not found in object '{}'".format(name, self.object_name(obj))
            raise Exception(f"property '{name}' not found in object '{self.object_name(obj)}'")

        # rlock(unitlock)
        # if dimless is None:
        #     runlock(unitlock)
        #     wlock(unitlock)
        #     dimless = unit_find("1")
        #     wunlock(unitlock)
        # else:
        #     runlock(unitlock)

        if prop.unit is not None:
            return prop.unit.name
        else:
            return dimless.name
    def object_get_value_by_addr(self, addr: Any, prop: PropertyMap) -> (str, int):
        prop = prop if prop else self.get_property_at_addr(addr)
        if prop is None or prop.access == PropertyAccess.PA_PRIVATE:
            print(
                f"Trying to read the value of private property "
                f"{prop.name if prop is not None else 'Unknown property'} in {self.name}")
            return "", 0

        # Simulate getting the value from the object based on the property; in real usage, this would depend on your application's structure
        property_value = prop.value
        value_str = str(property_value)

        return value_str, len(value_str)

    def object_get_value_by_name(self, name: str) -> (str, int):
        """Gets a property value by name and returns its string representation.

        Returns the string representation of the value or None if an error occurred.
        """
        if name is None:
            print("object_get_value_by_name: 'name' is None")
            return "", 0

        # Use the object_property_to_string function to get the string representation of the property
        value_str = self.object_property_to_string(name)
        if value_str is None:
            return "", 0

        # In Python, there's no direct equivalent to strncpy; the assignment copies the string.
        # However, we can simulate size limitation by slicing the string if necessary.
        # Assuming 'size' is a parameter indicating the maximum size of the output,
        # you can limit the length of 'value_str' here if needed.

        return value_str, len(value_str)

    def object_header(self):
        """ Get the header from the object's data structure """
        return id(self) - 1 if self else None  # todo this is broken

    def object_heartbeat(self) -> TimeStamp:
        t = Exec.exec_clock()
        t1 = self.owner_class.heartbeat() if self.owner_class.heartbeat else TS_NEVER
        self.object_profile(OPI_PROFILEITEM.OPI_HEARTBEAT, t)

        if global_debug_output:
            # Simplified debug output
            dt = "(invalid)" if t1 == TS_NEVER else time.ctime(t1)
            heartbeat_type = "(SOFT)" if t1 != TS_NEVER else "(HARD)"
            print(f"object {self.owner_class.name}:{self.id} heartbeat -> {heartbeat_type} {dt}")
        return t1

    def object_id(self):
        """ Get the id of the object """
        return self.id if self else -1

    def object_init(self, ) -> int:
        """
        Initialize an object.  This should not be called until
        all objects that are needed are created

        :return: 1 on success; 0 on failure
        """
        global global_starttime
        t = Exec.exec_clock()
        rv = 1  # Assume success by default
        self.clock = global_starttime

        if self.owner_class.init is not None:
            # Directly call the init method if it exists
            rv = self.owner_class.init(self, self.parent)

        self.object_profile(OPI_PROFILEITEM.OPI_INIT, t)
        if global_debug_output:
            print(f"object {self.owner_class.name}:{self.id} init -> {'ok' if rv else 'failed'}")
        return rv

    def object_isa(self, obj: [int,'Object'] = 0, type_: str = "") -> bool:
        """
        Tests the global_property_types of an object and returns whether it is as a boolean
        :param obj: the object to test
        :param type_: the global_property_types of test
        :return:
        """
        if obj == 0:
            return False
        if obj.owner_class.name == type_:
            return True
        elif obj.owner_class.isa:
            return obj.owner_class.isa(obj, type_)
        else:
            return False

    def object_loadmethod(self, name: str, value: str) -> Any:
        """
        :param name:
        :param value:
        :return:
        Example usage
            class Object:
                def load_example_method(self, value):
                    print(f"Loading with {value}")
                    return 1

            obj = Object()
            result = object_loadmethod(obj, 'load_example_method', 'example_value')
            print("Load method result:", result)
        """
        method = self.owner_class.get_loadmethod(name)
        if callable(method):
            return method(value)
        else:
            return None

    def object_locate_property(self, matcher: Any, pObj: Any, pProp: PropertyMap) -> int:
        """
        # Example usage:
            first_object = Object("Class1", [PropertyMap("Prop1", 100, "matcher1"), PropertyMap("Prop2", 200, "matcher2")])
            pObj = []  # Lists to hold the results, simulating pointer behavior in a high-level way
            pProp = []
            result = object_locate_property("matcher1", pObj, pProp)
            if result == SUCCESS:
                print(f"Found property: {pProp[0].name} in object of class {pObj[0].owner_class}")
            else:
                print("PropertyMap not found.")
        :param matcher:
        :param pObj:
        :param pProp:
        :return:
        """
        global first_object
        obj = first_object
        while obj is not None:
            for prop in obj.properties:
                if prop.identifier == matcher:  # Using a matcher instead of direct memory address
                    pObj.append(obj)  # Assuming pObj and pProp are lists for storing found objects/properties
                    pProp.next = prop
                    return SUCCESS
            obj = obj.next
        return FAILURE

    @staticmethod
    def object_name(oname: str) -> str:
        """Get the name of an object."""
        Object.convert_from_object(oname)
        return oname

    def _object_namespace(self, space):
        """Recursive helper function to collect namespace parts."""
        if space is None:
            return []
        parts = self._object_namespace(space.next)
        parts.append(space.name)
        return parts

    def object_namespace(self, current_namespace):
        ## Example namespace chain (equivalent to C++ linked list structure)
        ## Assuming a scenario where namespaces are nested as 'Global::Subspace::Subsubspace'
        # current_namespace = Namespace('Global', Namespace('Subspace', Namespace('Subsubspace')))

        """Get the full namespace of the current space."""
        parts = self._object_namespace(current_namespace)
        full_namespace = "::".join(reversed(parts))
        return full_namespace


    def object_open_namespace(self, space: str) -> int:  # open a new namespace and make it current */
        """
        Example usage
            if object_open_namespace("NewSpace"):
                print("Namespace opened successfully.")
            else:
                print("Failed to open namespace.")
        :param space:
        :return:
        """
        try:
            old_namespace = Object.namespace
            Object.namespace = {'current':space, 'next':old_namespace}
            return 1
        except Exception as e:
            print(f"object_open_namespace(char *space='{space}'): memory allocation failure", e)
            return 0

    def object_parent(self):
        """ Get the parent of the object """
        return self.parent if self else None

    def object_pop_namespace(self, ):  # restore the previous namespace from stack */
        pass

    def object_precommit(self, t1: TimeStamp) -> int:
        """
        Run events that should only occur at the start of a timestep.
        The input timestamp is that of the new time that is being synchronized to.

        This function should not affect other objects, and should not rely on
        calculations that are performed by other objects in precommit, since there
        is no order.

        :param t1:
        :return: The return value is if the function successfully completed.
        """
        t = Exec.exec_clock()
        rv = SUCCESS

        if hasattr(self.owner_class, 'precommit') and callable(getattr(self.owner_class, 'precommit')):
            rv = self.owner_class.precommit(self, t1)

        if rv == 1:  # If 'old school' or no precommit callback, treat as SUCCESS
            rv = SUCCESS

        self.object_profile(OPI_PROFILEITEM.OPI_PRECOMMIT, t)
        if global_debug_output:
            print(f"object {self.owner_class.name}:{self.id} precommit -> {'ok' if rv == SUCCESS else 'failed'}")
        return rv

    def object_profile(self, pass_, t):
        global global_profiler_enabled
        if global_profiler_enabled == 1:
            dt = time.time() - t
            self.synctime[pass_] += dt
            with self.owner_class.profiler.lock:
                self.owner_class.profiler.count += 1
                self.owner_class.profiler.clocks += dt

    def object_prop_in_class(self, prop: PropertyMap) -> [PropertyMap, None]:

        if prop is None:
            return None

        return self.owner_class.class_prop_in_class(self.owner_class, prop)

    def object_property_to_string(self, name: str) -> [None, str]:
        prop = ClassRegistry.find_property(self.name, name)
        value = prop.value
        if value is None:
            print(f"PropertyMap {name} not found")
            return None
        return str(value)

    def object_push_namespace(self, space: str) -> int:  # change to another namespace and push the one onto a stack */
        pass

    def object_rank(self):
        """ Get the rank of the object """
        return self.rank if self else -1
    # /* remote data access */

    def object_remote_read(self, obj: Any, prop: PropertyMap):  # access remote object data */
        """
        A class MyObject simulates an object with a dictionary properties to store its properties, mimicking C++
        object properties.
        The object_remote_read function provides threadsafe access to these properties. For single-threaded scenarios,
        it directly returns the property value. For multi-threaded access, it uses a lock to ensure that property
        reads are threadsafe.
        The global_multirun_mode and global_threadcount simulate the global variables from the C++ code,
        dictating whether the access needs to be locked based on the execution environment.
        The remote object read for multihost environments is mentioned as to do to implementing a distributed
        object system in Python and requires additional infrastructure (e.g.,  network communication, serialization).

        :param obj:  object from which to get data
        :param prop:  property from which to get data
        :return: The property
        """
        if global_multirun_mode == 'MRM_STANDALONE':
            if global_threadcount == 1:
                # Single-threaded, direct access
                return obj.properties.get(prop)
            else:
                # Multithreaded, access with lock
                with obj.lock:
                    return obj.properties.get(prop)
        else:
            # TODO: Implement multihost remote object read
            return None

    def object_remote_write(self, value: Any, obj: Any, prop: PropertyMap):  # access remote object data */
        """

        :param value:
        :param obj:
        :param prop:
        :return:

        Threadsafe remote object write.

        The MyObject class represents an object with properties. It includes a recursive lock _lock to synchronize
        access to these properties.

        The object_remote_write function writes data to an object's property. In a single-threaded environment,
        it updates the property directly. In a multithreaded environment, it acquires a lock to ensure that the
        write operation is threadsafe.

        The global variables global_multirun_mode and global_threadcount are used to determine the execution context,
        mimicking the original C++ function's behavior.

        For a multi-host scenario (not covered by this adaptation), implementing remote object write operations would
        involve network communication and potentially a serialization/deserialization mechanism,
        which is significantly more complex and beyond this simple example.

        Example usage:
            obj = MyObject()

        Writing to a property in a threadsafe manner
            object_remote_write(obj, 'temperature', 26.5)
            print(f"Updated Temperature: {obj.properties['temperature']}")
        """
        if global_multirun_mode == 'MRM_STANDALONE':
            if global_threadcount == 1:
                # Single-threaded, direct write
                obj.properties[prop] = value
            else:
                # Multithreaded, write with lock
                with obj.lock:
                    obj.properties[prop] = value
        else:
            # TODO: Implement multihost remote object write
            pass

    def object_remove_by_id(self, id: Any):
        """
        :param id: Unique ID of the object to remove
        :return: Returns the object after the one that was removed.
        """
        global first_object, deleted_object_count
        target = self.object_find_by_id(id)
        prev = None
        next_obj = None

        if target is not None:
            if first_object == target:
                first_object = target.next
                next_obj = target.next
            else:
                current = first_object
                while current.next and current.next != target:
                    prev = current
                    current = current.next

                if prev is not None:
                    prev.next = target.next
                    next_obj = target.next

            target = object_tree_delete(target, target.name if target.name else f"{target.owner_class.name}:{target.id}")
            target.owner_class.profiler.numobjs -= 1
            deleted_object_count += 1
            # No need to explicitly free the object as Python's garbage collector will take care of it

        return next_obj

    def object_save(self) -> str:
        """
        Example usage

        example_class = ObjectClass("ExampleClass")
        example_obj = Object(example_class, id=1, name="ExampleObject", rank=10, clock=1000000)

        serialized_str = object_save(example_obj)
        print(serialized_str)
        :return: a string of the object
        """
        lines = [f"object {self.owner_class.name}:{self.id} {{\n\n\t// header properties\n"]

        if self.parent is not None:
            # Assuming convert_from_object returns a string representation of the object
            parent_str = "parent_representation"
            lines.append(f"\tparent {parent_str};\n")

        lines.append(f"\trank {self.rank};\n")

        if self.name is not None:
            lines.append(f"\tname {self.name};\n")

        # Simplified conversion functions for demonstration
        clock_str = str(self.clock)
        lines.append(f"\tclock {clock_str};\n")

        if not math.isnan(self.latitude):
            latitude_str = str(self.latitude)
            lines.append(f"\tlatitude {latitude_str};\n")

        if not math.isnan(self.longitude):
            longitude_str = str(self.longitude)
            lines.append(f"\tlongitude {longitude_str};\n")

        # Simplified flags conversion for demonstration
        flags_str = "flags_representation"
        lines.append(f"\tflags {flags_str};\n")

        # Add class-defined properties
        # This would involve iterating over properties defined in the class and obj,
        # converting each to a string as done above.

        lines.append("}\n")
        serialized_obj = "".join(lines)

        # Debug output

        if global_debug_output:
            print(f"saving object {self.owner_class.name}:{self.id}")

        return serialized_obj

    def object_save_x(self, owner_class):
        """
        :param owner_class: the class to save
        :return: the buffer
        """
        lines = [f"\t// {owner_class.name} properties\n"]
        for prop in owner_class.pmap:
            value_str = self.object_property_to_string(prop.name)
            if value_str is not None:
                if prop.global_property_types == PropertyType.PT_timestamp:  # Assuming PT_timestamp needs single quotes
                    lines.append(f"\t{prop.name} '{value_str}';\n")
                else:
                    lines.append(f"\t{prop.name} {value_str};\n")

        output = "".join(lines)
        return output  # Return both the serialized object and the byte count

    def object_saveall(self, filepath: str) -> int:
        """
        Save all the objects in the model to the stream \p fp in the \p .GLM format
        :param filepath: file
        :return: the number of bytes written, 0 on error, with errno set.
        """
        access = PropertyAccess.PA_PUBLIC
        with open(filepath, 'w') as fp:
            count = 0

            count += fp.write("\n////////////////////////////////////////////////////////\n")
            count += fp.write("// objects\n")

            obj = first_object

            while obj:
                count += fp.write(f"object {obj.owner_class.name}:{obj.id} {{\n\n\t// header properties\n")

                if obj.parent is not None:
                    parent_id = f":{obj.parent.id}" if obj.parent.id is not None else ""
                    count += fp.write(f"\tparent {obj.parent.owner_class.name}{parent_id};\n")
                else:
                    count += fp.write("#ifdef INCLUDE_ROOT\n\troot;\n#endif\n")

                count += fp.write(f"\trank {obj.rank};\n")
                if obj.name is not None:
                    count += fp.write(f"\tname {obj.name};\n")
                count += fp.write(f"\tclock {TimeStamp.from_timestamp(obj.clock)};\n")
                if not math.isnan(obj.latitude):
                    count += fp.write(f"\tlatitude {self.convert_from_latitude(obj.latitude)};\n")
                if not math.isnan(obj.longitude):
                    count += fp.write(f"\tlongitude {self.convert_from_longitude(obj.longitude)};\n")
                count += fp.write(f"\tflags {self.convert_from_set(obj.flags,obj.object_flag_property())};\n")

                # dump properties
                prop = obj.owner_class.pmap
                while prop:
                    if buffer:=obj.object_property_to_string(prop.name):
                        if prop.access != access:
                            if ( access != PropertyAccess.PA_PUBLIC):
                                count += fp.write("#endif\n")
                            if prop.access == PropertyAccess.PA_REFERENCE:
                                count += fp.write("#ifdef INCLUDE_REFERENCE\n")
                            elif prop.access == PropertyAccess.PA_PROTECTED:
                                count += fp.write("#ifdef INCLUDE_PROTECTED\n")
                            elif prop.access == PropertyAccess.PA_PRIVATE:
                                count += fp.write("#ifdef INCLUDE_PRIVATE\n")
                            elif prop.access == PropertyAccess.PA_HIDDEN:
                                count += fp.write("#ifdef INCLUDE_HIDDEN\n")
                            access = prop.access
                        count += fp.write(f"\t{prop.name} {buffer};\n")
                    if prop.next:
                        prop = prop.next
                    elif prop.owner_class.parent:
                            prop = prop.owner_class.parent.pmap
                    else:
                        prop = None
                if access != PropertyAccess.PA_PUBLIC:
                    count += fp.write("#endif\n")
                count += fp.write("}\n")
                obj = obj.next

        return count

    def object_saveall_xml(self, filepath: str) -> int:
        root = ET.Element("objects")
        obj = first_object

        while obj:

            obj_element = ET.SubElement(root, "object", type=obj.owner_class.name, id=str(obj.id), name=obj.name)

            if obj.parent:
                parent_element = ET.SubElement(obj_element, "parent")
                parent_element.text = obj.parent.name

            ET.SubElement(obj_element, "rank").text = str(obj.rank)
            ET.SubElement(obj_element, "clock").text = str(obj.clock)

            if not math.isnan(obj.latitude):
                ET.SubElement(obj_element, "latitude").text = str(obj.latitude)
            if not math.isnan(obj.longitude):
                ET.SubElement(obj_element, "longitude").text = str(obj.longitude)

            for name, value in obj.properties.items():
                prop_element = ET.SubElement(obj_element, name)
                prop_element.text = str(value)
            obj = obj.next

        # Convert the ElementTree to a string
        xml_str = ET.tostring(root, encoding="unicode")

        with open(filepath, 'w') as fp:
            count = fp.write(f"{xml_str}\n")
        return count

    def object_saveall_xml_old(self, filepath: str) -> int:
        count = 0
        with open(filepath, 'w') as fp:
            fp.write("\t<objects>\n")
            obj = first_object

            while obj:

                fp.write(f"\t\t<object>\n")
                fp.write(f"\t\t\t<name>{obj.name}</name> \n")
                fp.write(f"\t\t\t<class>{obj.owner_class.name}</class> \n")
                fp.write(f"\t\t\t<id>{obj.id}</id>\n")

                if obj.parent:
                    parent_name = obj.parent.name if obj.parent.name else "(unidentified)"
                    fp.write("\t\t\t<parent>\n")
                    fp.write(f"\t\t\t\t<name>{parent_name}</name>\n")
                    fp.write(f"\t\t\t\t<class>{obj.parent.owner_class.name}</class>\n")
                    fp.write(f"\t\t\t\t<id>{obj.parent.id}</id>\n")
                    fp.write("\t\t\t</parent>\n")
                else:
                    fp.write("\t\t\t<parent>root</parent>\n")

                fp.write(f"\t\t\t<rank>{obj.rank}</rank>\n")
                fp.write("\t\t\t<clock>\n")
                fp.write(f"\t\t\t\t<timestamp>{TimeStamp.from_timestamp(obj.clock)}</timestamp>\n")
                fp.write("\t\t\t</clock>\n")

                if not math.isnan(obj.latitude):
                    fp.write(f"\t\t\t<latitude>{self.convert_from_latitude(obj.latitude)}</latitude>\n")
                if not math.isnan(obj.longitude):
                    fp.write(f"\t\t\t<longitude>{self.convert_from_longitude(obj.longitude)}</longitude>\n")

                fp.write("\t\t\t<properties>\n")
                for prop in obj.owner_class.pmap:
                    value = obj.object_property_to_string(prop.name)
                    if value:
                        fp.write("\t\t\t\t<property>\n")
                        fp.write(f"\t\t\t\t\t<global_property_types>{prop.name}</global_property_types>\n")
                        fp.write(f"\t\t\t\t\t<value>{value}</value>\n")
                        fp.write("\t\t\t\t</property>\n")

                fp.write("\t\t\t</properties>\n")
                fp.write("\t\t</object>\n")
                count += 1  # Counting objects instead of bytes for simplicity
                obj = obj.next
            fp.write("\t</objects>\n")

        # Return the number of objects written for simplicity
        return count

    def object_select_namespace(self, space: str) -> int:  # change to another namespace */
        """
        # Example usage
            try:
                object_select_namespace("SomeNamespace")
            except NotImplementedError as e:
                print(e)

        :param space:
        :return:
        """
        raise NotImplementedError("namespace selection not yet supported")


    def object_set_complex_by_name(self, name: str, value: Any) -> int:
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop is None:
            print(f"PropertyMap {name} not found in object.")
            return 0

        if prop.access not in [PropertyAccess.PA_PUBLIC, PropertyAccess.PA_HIDDEN]:
            print(f"Trying to set the value of non-public property {prop.name} in {self.owner_class, name}.")
            return 0

        if prop.global_property_types not in [PropertyType.PT_complex]:
            print(f"PropertyMap '{prop.name}' of '{self.owner_class.name}' cannot be set like a complex.")
            return 0

        # Assuming the property exists on the object, directly set its value
        prop.value = value
        return 1

    def object_set_dependent(self, dependent: Any) -> int:
        if dependent is None or self == dependent:
            raise ValueError("Invalid dependent assignment.")
        return self._set_rank(dependent, self.rank + 1)

    def object_set_double_by_name(self, name: str, value: float) -> int:
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop is None:
            print(f"PropertyMap {name} not found in object.")
            return 0

        if prop.access not in [PropertyAccess.PA_PUBLIC, PropertyAccess.PA_HIDDEN]:
            print(f"Trying to set the value of non-public property {prop.name} in {self.owner_class, name}.")
            return 0

        if prop.global_property_types not in [PropertyType.PT_float, PropertyType.PT_double]:
            print(f"PropertyMap '{prop.name}' of '{self.owner_class.name}' cannot be set like an float.")
            return 0

        # Assuming the property exists on the object, directly set its value
        prop.value = value
        return 1

    def object_set_int16_by_name(self, name: str, value: int) -> int:
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop is None:
            print(f"PropertyMap {name} not found in object.")
            return 0

        if prop.access not in [PropertyAccess.PA_PUBLIC, PropertyAccess.PA_HIDDEN]:
            print(f"Trying to set the value of non-public property {prop.name} in {self.owner_class,name}.")
            return 0

        if prop.global_property_types != PropertyType.PT_int16:
            print(f"PropertyMap '{prop.name}' of '{self.owner_class.name}' cannot be set like an int16.")
            return 0

        # Assuming the property exists on the object, directly set its value
        prop.value = value
        return 1

    def object_set_int32_by_name(self, name: str, value: int) -> int:
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop is None:
            print(f"PropertyMap {name} not found in object.")
            return 0

        if prop.access not in [PropertyAccess.PA_PUBLIC, PropertyAccess.PA_HIDDEN]:
            print(f"Trying to set the value of non-public property {prop.name} in {self.owner_class, name}.")
            return 0

        if prop.global_property_types != PropertyType.PT_int32:
            print(f"PropertyMap '{prop.name}' of '{self.owner_class.name}' cannot be set like an int32.")
            return 0

        # Assuming the property exists on the object, directly set its value
        prop.value = value
        return 1

    def object_set_int64_by_name(self, name: str, value: int) -> int:
        prop = ClassRegistry.find_property(self.owner_class, name)
        if prop is None:
            print(f"PropertyMap {name} not found in object.")
            return 0

        if prop.access not in [PropertyAccess.PA_PUBLIC, PropertyAccess.PA_HIDDEN]:
            print(f"Trying to set the value of non-public property {prop.name} in {self.owner_class,name}.")
            return 0

        if prop.global_property_types != PropertyType.PT_int64:
            print(f"PropertyMap '{prop.name}' of '{self.owner_class.name}' cannot be set like an int64.")
            return 0

        # Assuming the property exists on the object, directly set its value
        prop.value = value
        return 1

    def object_set_name(self, name: str) -> str:
        global top, global_relax_naming_rules
        if not name[0].isalpha() and name[0] != '_':
            if not global_relax_naming_rules:
                raise ValueError(f"Object name '{name}' invalid, names must start with a letter or an underscore")
            else:
                print(
                    f"Warning: object name '{name}' does not follow strict naming rules and may not link correctly during load time")

        if self.name:
            # Assuming a mechanism to delete the old name from the tree
            object_tree_delete(top, self.name)

        if name:
            if self.object_find_name(name):
                raise ValueError(f"An object named '{name}' already exists!")
            else:
                # Assuming object_tree_add returns the added object or raises an exception
                item = object_tree_add(self, name)
                self.name = item.name

        return self.name

    def object_set_parent(self, parent: Any) -> int:
        if self == parent:
            raise ValueError(f"object {self.name} tried to set itself as its parent")

        self.parent = parent
        self.child_count = 0 if not parent else parent.child_count + 1

        if parent:
            parent_rank = self._set_rank(parent, self.rank)
            return parent_rank
        return self.rank

    def object_set_rank(self, rank: Any) -> int:

        if rank <= self.rank:
            return self.rank

            # Example implementation calling a hypothetical set_rank function
            # Assuming set_rank is similar to the provided _set_rank or _set_rankx but adapted to Python
        self.rank = max(self.rank, rank)
        return self.rank

    def _set_rank(self, obj, rank, first=None):
        if obj is None:
            print("set_rank called for a null object")
            return -1

        if rank >= self.object_get_count():
            print(f"{self.object_name(first)}: set_rank internal error, rank > object count")
            return -1

        if obj == first:
            print(f"{self.object_name(first)}: set_rank failed, parent loopback has occurred")
            return -1

        if OBJECT_FLAG.OF_RERANK in obj.flags:
            print(f"{self.object_name(obj)}: object flagged as already re-ranked")
            return -1
        else:
            obj.flags.add(OBJECT_FLAG.OF_RERANK)

        if rank >= obj.rank:
            obj.rank = rank + 1

        if obj.parent is not None:
            parent_rank = self._set_rank(obj.parent, obj.rank, first if first else obj)
            if parent_rank == -1:
                return -1

        obj.flags.remove(OBJECT_FLAG.OF_RERANK)
        return obj.rank

    def _set_rankx(self, obj, rank, first=None):
        n = self.object_get_count()
        if obj is None:
            print("set_rank called for a null object")
            return -1

        original_first = first
        while obj is not None:
            if n < 0:
                print(f"{self.object_name(original_first)}: set_rank internal error, rank > object count")
                return -1
            if first is None:
                first = obj
            elif first == obj:
                print(f"{self.object_name(first)}: set_rank failed, parent loopback has occurred")
                return -1
            if rank >= obj.rank:
                if OBJECT_FLAG.OF_RERANK in obj.flags:
                    print(f"{self.object_name(obj)}: object flagged as already re-ranked")
                    return -1
                else:
                    obj.flags.add(OBJECT_FLAG.OF_RERANK)
                obj.rank = rank + 1
            obj = obj.parent

        # Clear rerank flag after rank update
        obj = original_first
        while obj is not None:
            obj.flags.discard(OBJECT_FLAG.OF_RERANK)
            obj = obj.parent

        return obj.rank if obj else 0

    def object_set_value_by_addr(self, addr: Any, value: str, prop: PropertyMap) -> int:
        pass

    def set_header_value(self, n, v) -> bool:
        if self.object_find_name(n):
            self.object_set_value_by_name(n, v)
            return True
        else:
            return False

    def object_set_value_by_name(self, name: str, value: str) -> int:
        prop = ClassRegistry.find_property(self, name)
        if prop is None:
            if not self.set_header_value(name, value):
                # Handle error case where property is not found and setting header value failed
                print(f"PropertyMap {name} not found in object and setting header value failed.")
                return 0
            else:
                return max(len(value), 1)  # empty string is not necessarily wrong

        if prop.access not in [PropertyAccess.PA_PUBLIC, PropertyAccess.PA_HIDDEN]:
            print(f"Trying to set the value of non-public property {prop.name} in {self.name}")
            return 0

        prop.value = value
        return len(value)

    def object_set_value_by_type(self, p, addr: Any, value: str) -> int:
        pass

    def object_size(self):
        """ Get the size of the object """
        return 1 if self else -1

    def object_stream_fixup(self, class_name: str, obj_name: str):
        global first_object, last_object
        self.owner_class = self.owner_class.class_get_class_from_class_name(class_name)
        self.name = obj_name
        self.next = None
        if first_object is None:
            first_object = self
        else:
            last_object.next = self
        last_object = self

    def _object_sync(self, ts: TimeStamp, pass_conf: PASSCONFIG) -> TimeStamp:
        """
        Synchronizes the object with the given TimeStamp
        :param ts: The desired clock to sync to
        :param pass_conf:  the pass configuration
        :return: A timeStamp
        """
        global global_skipsafe
        effective_valid_to = min(self.clock + global_skipsafe, self.valid_to)  # Adjusted for Python datetime handling

        if (global_skipsafe > 0 and (self.flags & OBJECT_FLAG.OF_SKIPSAFE) and
                TimeStamp.from_timestamp(ts) < effective_valid_to):
            # return valid_to time if skipping
            return effective_valid_to

        if self.owner_class.sync is None:
            print(f"Sync function is not implemented in module {self.owner_class.name}")
            return TS_INVALID

        # Simplified sync call without lock management and alarms
        sync_time = self.owner_class.sync(self, ts, pass_conf) if self.owner_class.sync else TS_NEVER

        # Simplified PLC call logic
        plc_time = self.owner_class.plc(self, ts) if 'PC_BOTTOMUP' in self.owner_class.passconfig and self.owner_class.plc else TS_NEVER

        # Choose the earliest time between PLC and sync times
        sync_time = min(plc_time, sync_time)

        # Compute valid_to time
        self.valid_to = sync_time if sync_time <= TS_MAX else TS_NEVER

        return self.valid_to

    def object_sync(self, ts: TimeStamp, pass_conf: PASSCONFIG) -> TimeStamp:
        """
        Synchronize an object.  The timestamp given is the desired increment.

        If an object is called on multiple passes (see PASSCONFIG) it is
        customary to update the clock only after the last pass is completed.

        For the sake of speed this function assumes that the sync function
        is properly defined in the object class structure.

        :global_property_types pass_conf: object
        :param ts:
        :param pass_conf:
        :return: the time of the next event for this object.
        """
        global global_skipsafe, global_debug_output
        t = Exec.exec_clock()
        t2 = TS_NEVER
        # Assuming _object_sync is a simplified version that calls the object's sync method
        while True:
            t2 = self.owner_class.sync(self,
                                       min(TimeStamp.from_timestamp(ts),
                                           self.valid_to if self.valid_to > 0 else TS_NEVER),
                                 pass_conf) if self.owner_class.sync else TS_NEVER
            if not (t2 > 0 and ts > (abs(t2) if t2 < 0 else t2) and t2 < TS_NEVER):
                break

        # Profiling and debug output are simplified for this example
        if global_profiler_enabled:
            # object_profile logic here, adapted to Python
            match pass_conf:
                case PASSCONFIG.PC_PRETOPDOWN:
                    self.object_profile(OPI_PROFILEITEM.OPI_PRESYNC, t)
                case PASSCONFIG.PC_BOTTOMUP:
                    self.object_profile(OPI_PROFILEITEM.OPI_SYNC, t)
                case PASSCONFIG.PC_POSTTOPDOWN:
                    self.object_profile(OPI_PROFILEITEM.OPI_POSTSYNC, t)
                case _:
                    pass

        if global_debug_output:
            # Simplified debug output
            match pass_conf:
                case PASSCONFIG.PC_NOSYNC:  # used when the class requires no synchronization
                    pass_message = "PRESYNC"
                case PASSCONFIG.PC_PRETOPDOWN:  # used when the class requires synchronization on the first top-down pass
                    pass_message = "PRESYNC"
                case PASSCONFIG.PC_BOTTOMUP:  # used when the class requires synchronization on the bottom-up pass
                    pass_message = "SYNC"
                case PASSCONFIG.PC_POSTTOPDOWN:  # used when the class requires synchronization on the second top-down pass
                    pass_message = "POSTSYNC"
                case _:
                    pass_message = "UNKNOWN"
            dt1 = TimeStamp.from_timestamp(ts)
            dt2 = TimeStamp.from_timestamp(t2)
            type_message = "SOFT" if is_soft_timestamp(t2) else "HARD",
            debug_message = (f"Object {self.owner_class.name}:{self.id} "
                             f"pass {pass_message} sync to {dt1} -> {type_message} {dt2}")
            print(debug_message)
            # print(f"Object :{self.id} synced to {ts} -> {t2}")

        return t2

    @staticmethod
    def remove_objects():
        global first_object, next_object_id

        obj1 = first_object
        while obj1 is not None:
            first_object = obj1.next
            obj1.owner_class.profiler.numobjs -= 1
            # In Python, explicitly freeing objects is not required. The garbage collector handles it.
            obj1 = first_object

        next_object_id = 0


class Forecast:
    """
    Forecast create
    The specifications for a forecast are as follows
	"option: value; [option: value; [...]]" where
	options is as follows:
	'timestep' - identifies the timestep of the forecast
	'length' - identifies the number of values in the forecast
	'property' - identifies the property this forecast applies to
	'external' - identifies the external function call to use to update the forecast

	The external function is specified as 'libname/functionname', the function 'functionname'
	call must be in the DLL/SO/DYLIB file 'libfile' and have the following
	call prototype
		TIMESTAMP functioname(OBJECT *obj, FORECAST *fc);
	where the return value is the new forecast start time or TZ_INVALID is the forecast
	could not be updated (in which case the existing forecast 'fc' is not changed).

	if 'external' is not defined, then the forecast is expected to be updated
	during the object presync operation.  It is up to the class implementation of
	presync to suppress update of the forecast when 'external' is set.

    Example Usage:
        obj = Object()

    Create a forecast for an object
        fc = Forecast(obj, "timestep: 1; length: 5; property: temperature")

    Find a forecast by property name
        found_fc = Forecast.find(obj, "temperature")
        if found_fc:
            print("Forecast found")

    Read a value from the forecast
        value = found_fc.read(2)  # Assuming a timestamp that makes sense
        print("Forecast value:", value)

    Save data to the forecast
        found_fc.save(0, 1, [20.5, 21.0, 22.3, 23.1, 24.0])

    """
    def __init__(self, obj, specs):
        self.next = None  # Link to the next forecast in the chain
        self.specification = specs  # Store the specification string
        self.starttime = None
        self.timestep = None
        self.n_values = 0
        self.values = None
        self.propref = None  # Reference to the property this forecast applies to

        # Link this forecast to the object
        if hasattr(obj, 'forecast'):
            self.next = obj.forecast
        obj.forecast = self

        # TODO: Parse specs to initialize other attributes
        print("Warning: description parsing not implemented")

    @staticmethod
    def find(obj, name):
        fc = obj.forecast
        while fc:
            if fc.propref and fc.propref.name == name:
                return fc
            fc = fc.next
        return None

    def read(self, ts):
        # prevent use of zero or negative timesteps or time request is before start of forecast
        if self.timestep <= 0 or ts < self.starttime or not self.values:
            return np.nan

        # compute offset to data entry
        n = (ts - self.starttime) // self.timestep
        if n >= self.n_values:
            return np.nan
        return self.values[n]

    def save(self, ts, tstep, data):
        self.starttime = ts
        self.timestep = tstep
        self.n_values = len(data)
        self.values = np.array(data, dtype=float)


class Callbacks:
    def __init__(self):
        self.global_clock = None
        self.global_delta_curr_clock = None
        self.global_stoptime = None
        self.global_exit_code = None

        # Assuming the output methods are replaced with appropriate Python functions
        self.output_verbose = lambda format_string, *args: None
        self.output_message = lambda format_string, *args: None
        self.output_warning = lambda format_string, *args: None
        self.output_error = lambda format_string, *args: None
        self.output_fatal = lambda format_string, *args: None
        self.output_debug = lambda format_string, *args: None
        self.output_test = lambda format_string, *args: None

        # Replace C++ function pointers with Python callable
        self.register_class = lambda module, class_name, flags, pass_config: None
        self.create = {
            'single': lambda class_obj: None,
            'array': lambda class_obj, count: None,
            'foreign': lambda obj: None
        }
        self.define_map = lambda class_obj, *args: None
        self.loadmethod = lambda class_obj, name, callback: None
        self.class_getfirst = lambda: None
        self.class_getname = lambda name: None
        # PROPERTY *(*class_add_extended_property)(Class *,char *,PropertyType,char *);
        self.class_add_extended_property = lambda class_obj, name, prop_type, value: None
        # Additional methods and structures
        self.function = {
            'get': lambda class_obj, name: None,
            'define': lambda class_obj, name, funcaddr: None
        }
        # 	int (*define_enumeration_member)(Class*,const char*,const char*,enumeration);
        self.define_enumerated_member = lambda class_obj, name, value, enum_member: None
        # 	int (*define_set_member)(Class*,const char*,const char*,unsigned int64);
        self.define_set_member = lambda class_obj, name, value, digit: None
        # 	struct {
        # 		OBJECT *(*get_first)(void);
        # 		int (*set_dependent)(OBJECT*,OBJECT*);
        # 		int (*set_parent)(OBJECT*,OBJECT*);
        # 		int (*set_rank)(OBJECT*, OBJECTRANK);
        # 	} object;

        self.object = {
            'get_first': lambda: None,
            'set_dependent': lambda obj1, obj2: None,
            'set_parent': lambda obj1, obj2: None,
            'set_rank': lambda obj, rank: None,
            # ... Other object methods ...
        }

        self.properties = {
            'get_property': lambda obj, name, prop_struct: None,
            'set_value_by_addr': lambda obj, addr, value, prop: None,
            # ... Other property methods ...

            # 		int (*get_value_by_addr)(OBJECT *, void*, char*, int size,PROPERTY*);
            # 		int (*set_value_by_name)(OBJECT *, char*, char*);
            # 		int (*get_value_by_name)(OBJECT *, const char*, char*, int size);
            # 		OBJECT *(*get_reference)(OBJECT *, char*);
            # 		char *(*get_unit)(OBJECT *, const char *);
            # 		void *(*get_addr)(OBJECT *, const char *);
            # 		int (*set_value_by_type)(PropertyType,void *data,char *);
            # 		bool (*compare_basic)(PropertyType global_property_types, PROPERTYCOMPAREOP op, void* x, void* a, void* b, char *part);
            # 		PROPERTYCOMPAREOP (*get_compare_op)(PropertyType global_property_types, char *opstr);
            # 		double (*get_part)(OBJECT*,PROPERTY*,const char*);
            # 		PropertSpec *(*get_spec)(PropertyType);
        }

        self.find = {
            'objects': lambda findlist, *args: None,
            'next': lambda findlist, obj: None,
            'copy': lambda findlist: None,
            'add': lambda findlist, obj: None,
            'del': lambda findlist, obj: None,
            'clear': lambda findlist: None,
            # ... Other find methods ...
        }
        # 	PROPERTY *(*find_property)(Class *, const PROPERTYNAME);
        # 	void *(*malloc)(size_t);
        # 	void (*free)(void*);
        # 	struct {
        # 		struct s_aggregate *(*create)(aggregator: str, group_expression: str);
        # 		double (*refresh)(struct s_aggregate *aggregate);
        # 	} aggregate;
        # 	struct {
        # 		double *(*getvar)(MODULE *module, const varname: str);
        # 		MODULE *(*getfirst)(void);
        # 		int (*depends)(const name: str, unsigned char major, unsigned char minor, unsigned short build);
        # 		const : str(*find_transform_function)(TRANSFORMFUNCTION function);
        # 	} module;
        # 	struct {
        # 		double (*uniform)(unsigned int *rng, double a, double b);
        # 		double (*normal)(unsigned int *rng, double m, double s);
        # 		double (*bernoulli)(unsigned int *rng, double p);
        # 		double (*pareto)(unsigned int *rng, double m, double a);
        # 		double (*lognormal)(unsigned int *rng,double m, double s);
        # 		double (*sampled)(unsigned int *rng,unsigned int n, double *x);
        # 		double (*exponential)(unsigned int *rng,double l);
        # 		RANDOMTYPE (*global_property_types)(name: str);
        # 		double (*value)(RANDOMTYPE global_property_types, ...);
        # 		double (*pseudo)(RANDOMTYPE global_property_types, unsigned int *state, ...);
        # 		double (*triangle)(unsigned int *rng,double a, double b);
        # 		double (*beta)(unsigned int *rng,double a, double b);
        # 		double (*gamma)(unsigned int *rng,double a, double b);
        # 		double (*weibull)(unsigned int *rng,double a, double b);
        # 		double (*rayleigh)(unsigned int *rng,double a);
        # 	} random;
        # 	int (*object_isa)(OBJECT *self, const global_property_types: str);
        # 	DelegatedType* (*register_type)(owner_class: Class, global_property_types: str,int (*from_string)(void*,char*),int (*to_string)(void*,char*,int));
        # 	int (*define_type)(Class*,DelegatedType*,...);
        # 	struct {
        # 		TIMESTAMP (*mkdatetime)(DATETIME *dt);
        # 		int (*strdatetime)(DATETIME *t, buffer: str, int size);
        # 		double (*timestamp_to_days)(TIMESTAMP t);
        # 		double (*timestamp_to_hours)(TIMESTAMP t);
        # 		double (*timestamp_to_minutes)(TIMESTAMP t);
        # 		double (*timestamp_to_seconds)(TIMESTAMP t);
        # 		int (*local_datetime)(TIMESTAMP ts, DATETIME *dt);
        #         int (*local_datetime_delta)(double ts, DATETIME *dt);
        # 		TIMESTAMP (*convert_to_timestamp)(const value: str);
        # 		TIMESTAMP (*convert_to_timestamp_delta)(const value: str, unsigned int *microseconds, double *dbl_time_value);
        # 		int (*convert_from_timestamp)(TIMESTAMP ts, buffer: str, int size);
        # 		int (*convert_from_deltatime_timestamp)(double ts_v, buffer: str, int size);
        # 	} time;
        # 	int (*unit_convert)(const from: str, const to: str, double *value);
        # 	int (*unit_convert_ex)(UNIT *pFrom, UNIT *pTo, double *pValue);
        # 	UNIT *(*unit_find)(const unit_name: str);
        # 	struct {
        # 		EXCEPTIONHANDLER *(*create_exception_handler)();
        # 		void (*delete_exception_handler)(EXCEPTIONHANDLER *ptr);
        # 		void (*throw_exception)(const msg: str, ...);
        # 		: str(*exception_msg)(void);
        # 	} exception;
        # 	struct {
        # 		GLOBALVAR *(*create)(const name: str, ...);
        # 		STATUS (*setvar)(const def: str,...);
        # 		: str(*getvar)(const name: str, buffer: str, int size);
        # 		GLOBALVAR *(*find)(const name: str);
        # 	} global;

        self.global_var = {
            'create': lambda name, *args: None,
            'setvar': lambda defn, *args: None,
            'getvar': lambda name, buffer, size: None,
            'find': lambda name: None,
            # ... Other global methods ...
        }

        # 	struct {
        # 		void (*read)(unsigned int *);
        # 		void (*write)(unsigned int *);
        # 	} lock, unlock;
        # 	struct {
        # 		: str(*find_file)(const name: str, const path: str, int mode, buffer: str, int len);
        # 	} file;

        self.lock = lambda *args: None
        self.unlock = lambda *args: None
        self.file = {
            'find_file': lambda name, path, mode, buffer, len: None,
            # ... Other file methods ...
        }

        self.objvar = {
            'bool_var': lambda obj, prop: None,
            'complex_var': lambda obj, prop: None,
            # 		enumeration *(*enum_var)(OBJECT *self, PROPERTY *prop);
            # 		set *(*set_var)(OBJECT *self, PROPERTY *prop);
            # 		int16 *(*int16_var)(OBJECT *self, PROPERTY *prop);
            # 		int32 *(*int32_var)(OBJECT *self, PROPERTY *prop);
            # 		int64 *(*int64_var)(OBJECT *self, PROPERTY *prop);
            # 		double *(*double_var)(OBJECT *self, PROPERTY *prop);
            # 		: str(*string_var)(OBJECT *self, PROPERTY *prop);
            # 		OBJECT **(*object_var)(OBJECT *self, PROPERTY *prop);
        }

        self.objvarname = {
            'bool_var': lambda obj, name: None,
            'complex_var': lambda obj, name: None,
            # enumeration *(*enum_var)(OBJECT *self, const name: str);
            # 		set *(*set_var)(OBJECT *self, const name: str);
            # 		int16 *(*int16_var)(OBJECT *self, const name: str);
            # 		int32 *(*int32_var)(OBJECT *self, const name: str);
            # 		int64 *(*int64_var)(OBJECT *self, const name: str);
            # 		double *(*double_var)(OBJECT *self, const name: str);
            # 		: str(*string_var)(OBJECT *self, const name: str);
            # 		OBJECT **(*object_var)(OBJECT *self, const name: str);
        }

        self.convert = {
            'string_to_property': lambda prop, addr, value: None,
            'property_to_string': lambda prop, addr, value, size: None,
            # ... Other convert methods ...
        }

        self.module_find = lambda name: None
        self.get_object = lambda name: None
        self.object_find_by_id = lambda obj_id: None
        self.name_object = lambda obj, buffer, len: None
        self.get_oflags = lambda extflags: None
        self.object_count = lambda: None
        self.schedule = {
            'create': lambda name, definition: None,
            'index': lambda sch, ts: None,
            'value': lambda sch, index: None,
            'dtnext': lambda sch, index: None,
            'find': lambda name: None,
            'getfirst': lambda: None,
            # ... Other schedule methods ...
        }

        self.loadshape = {
            'create': lambda s: None,
            'init': lambda s: None,
            # ... Other loadshape methods ...
        }

        self.enduse = {
            'create': lambda e: None,
            'sync': lambda e, pass_config, t1: None,
            # ... Other enduse methods ...
        }

        self.interpolate = {
            'linear': lambda t, x0, y0, x1, y1: None,
            'quadratic': lambda t, x0, y0, x1, y1, x2, y2: None,
            # ... Other interpolate methods ...
        }

        self.forecast = {
            'create': lambda obj, specs: None,
            'find': lambda obj, name: None,
            'read': lambda fc, ts: None,
            'save': lambda fc, ts, tstep, n_values, data: None,
            # ... Other forecast methods ...
        }

        self.remote = {
            'readobj': lambda local, obj, prop: None,
            'writeobj': lambda local, obj, prop: None,
            'readvar': lambda local, var: None,
            'writevar': lambda local, var: None,
            # ... Other remote methods ...
        }

        self.objlist = {
            'create': lambda owner_class, match_property, match_part, match_op, match_value1, match_value2: None,
            'search': lambda group: None,
            'destroy': lambda list: None,
            'add': lambda list, match_property, match_part, match_op, match_value1, match_value2: None,
            'del': lambda list, match_property, match_part, match_op, match_value1, match_value2: None,
            'size': lambda list: None,
            'get': lambda list, n: None,
            'apply': lambda list, arg, function: None,
            # ... Other objlist methods ...
        }

        self.geography = {
            'latitude': {
                'to_string': lambda v, buffer, size: None,
                'from_string': lambda buffer: None,
            },
            'longitude': {
                'to_string': lambda v, buffer, size: None,
                'from_string': lambda buffer: None,
            },
            # ... Other geography methods ...
        }

        self.http = {
            'read': lambda url, maxlen: None,
            'free': lambda result: None,
            # ... Other http methods ...
        }

        self.transform = {
            'getnext': lambda transform: None,
            'add_linear': lambda source, double_ptr, void_ptr, a, b, obj, prop, sch: None,
            'add_external': lambda obj, prop, name, obj2, prop2: None,
            'apply': lambda ts, transform, double_ptr, double_ptr2: None,
            # ... Other transform methods ...
        }

        self.randomvar = {
            'getnext': lambda randomvar_struct: None,
            'getspec': lambda char, size, randomvar_struct: None,
            # ... Other randomvar methods ...
        }

        self.version = {
            'major': lambda: None,
            'minor': lambda: None,
            'patch': lambda: None,
            'build': lambda: None,
            'branch': lambda: None,
            # ... Other version methods ...
        }

        self.magic = 0  # Placeholder for structure alignment check




