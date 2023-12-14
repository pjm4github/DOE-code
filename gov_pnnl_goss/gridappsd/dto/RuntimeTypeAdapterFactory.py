
import json
from collections import OrderedDict

import json

def custom_type_adapter(in_json, base_type, type_field_name, maintain_type, label_to_delegate):
    """
    # Example usage:
        base_type = "YourBaseType"
        type_field_name = "type"
        maintain_type = True  # Set to True if you want to keep the type field
        label_to_delegate = {
            "subtype1": lambda json_str: json.loads(json_str),  # Replace with actual delegate functions
            "subtype2": lambda json_str: json.loads(json_str),
        }

        json_input = '{"type": "subtype1", "other_field": "value"}'
        result = custom_type_adapter(json_input, base_type, type_field_name, maintain_type, label_to_delegate)
        print(result)

    :param in_json:
    :param base_type:
    :param type_field_name:
    :param maintain_type:
    :param label_to_delegate:
    :return:
    """
    json_dict = json.loads(in_json)

    if type_field_name not in json_dict:
        raise ValueError(f"cannot deserialize {base_type} because it does not define a field named {type_field_name}")

    label = json_dict[type_field_name]

    if maintain_type:
        label_json_element = json_dict[type_field_name]
    else:
        label_json_element = json_dict.pop(type_field_name)

    if label not in label_to_delegate:
        raise ValueError(f"cannot deserialize {base_type} subtype named {label}; did you forget to register a subtype?")

    delegate = label_to_delegate[label]

    return delegate(json.dumps(json_dict))


class RuntimeTypeAdapterFactory:
    """
    Adapts values whose runtime type may differ from their declaration type. This
    is necessary when a field'status type is not the same type that GSON should create
    when deserializing that field. For example, consider these types:
    <pre>   {@code
      abstract class Shape {
        int x;
        int y;
      }
      class Circle extends Shape {  int radius;}class Rectangle extends Shape {  int width;  int height;
       }
       class Diamond extends Shape {
         int width;
         int height;
       }
       class Drawing {
         Shape bottomShape;
         Shape topShape;
       }
        }</pre>
        <precisions>Without additional type information, the serialized JSON is ambiguous. Is
        the bottom shape in this drawing a rectangle or a diamond? <pre>   {@code
          {
            "bottomShape": {
              "width": 10,
              "height": 5,
              "x": 0,
              "y": 0
            },
            "topShape": {
              "radius": 2,
              "x": 4,
              "y": 1
            }
          }}</pre>
        This class addresses this problem by adding type information to the
        serialized JSON and honoring that type information when the JSON is
        deserialized: <pre>   {@code
          {
            "bottomShape": {
              "type": "Diamond",
              "width": 10,
              "height": 5,
              "x": 0,
              "y": 0
            },
            "topShape": {
              "type": "Circle",
              "radius": 2,
              "x": 4,
              "y": 1
            }
          }}</pre>
        Both the type field name ({@code "type"}) and the type labels ({@code
        "Rectangle"}) are configurable.

        <h3>Registering Types</h3>
        Create a {@code RuntimeTypeAdapterFactory} by passing the base type and type field
        name to the {@link #of} factory method. If you don't supply an explicit type
        field name, {@code "type"} will be used. <pre>   {@code
          RuntimeTypeAdapterFactory<Shape> shapeAdapterFactory
              = RuntimeTypeAdapterFactory.of(Shape.class, "type");
        }</pre>
        Next register all of your subtypes. Every subtype must be explicitly
        registered. This protects your application from injection attacks. If you
        don't supply an explicit type label, the type'status simple name will be used.
        <pre>   {@code
          shapeAdapterFactory.registerSubtype(Rectangle.class, "Rectangle");
          shapeAdapterFactory.registerSubtype(Circle.class, "Circle");
          shapeAdapterFactory.registerSubtype(Diamond.class, "Diamond");
        }</pre>
        Finally, register the type adapter factory in your application'status GSON builder:
        <pre>   {@code
          Gson gson = new GsonBuilder()
              .registerTypeAdapterFactory(shapeAdapterFactory)
              .create();
        }</pre>
        Like {@code GsonBuilder}, this API supports chaining: <pre>   {@code
          RuntimeTypeAdapterFactory<Shape> shapeAdapterFactory = RuntimeTypeAdapterFactory.of(Shape.class)
              .registerSubtype(Rectangle.class)
              .registerSubtype(Circle.class)
              .registerSubtype(Diamond.class);
        }</pre>

`    """

    def __init__(self, base_type, type_field_name=None, maintain_type=None):
        """
        Creates a new runtime type adapter using for {@code baseType} using {@code
        typeFieldName} as the type field name. Type field names are case sensitive.
        {@code maintainType} flag decide if the type will be stored in pojo or not.

        :param base_type:
        :param type_field_name:
        :param maintain_type:
        """
        # Form 1 (All arguments filled in)
        #RuntimeTypeAdapterFactory(baseType, String
        #                          typeFieldName,
        #                          boolean maintainType) {
        #     return new RuntimeTypeAdapterFactory<T>(baseType, typeFieldName, maintainType);
        #   /**
        #    * Creates a new runtime type adapter using for {@code baseType} using {@code
        #    * typeFieldName} as the type field name. Type field names are case sensitive.
        #    */
        # Form 2 (maintainType is missing)
        #   RuntimeTypeAdapterFactory(baseType, String
        #                             typeFieldName) {
        #     return new RuntimeTypeAdapterFactory<T>(baseType, typeFieldName, false);

        # Form 3
        #   /**
        #    * Creates a new runtime type adapter for {@code baseType} using {@code "type"} as
        #    * the type field name.
        #    */
        #   RuntimeTypeAdapterFactory(baseType) {
        #     return new RuntimeTypeAdapterFactory<T>(baseType, "type", false);
        #   }
        # Form 4
        #   /**
        #    * Registers {@code type} identified by {@code label}. Labels are case
        #    * sensitive.
        #    *
        #    * @throws IllegalArgumentException if either {@code type} or {@code label}
        #    *     have already been registered on this type adapter.
        #    */
        #   RuntimeTypeAdapterFactory registerSubtype(GClass<? extends T> type, String label) {
        #     if (type == null || label == null) {
        #       throw new NullPointerException();
        #     }
        #     if (subtypeToLabel.containsKey(type) || labelToSubtype.containsKey(label)) {
        #       throw new IllegalArgumentException("types and labels must be unique");
        #     }
        #     labelToSubtype.put(label, type);
        #     subtypeToLabel.put(type, label);
        #     return this;
        #   }

        self.base_type = base_type
        self.type_field_name = type_field_name if type_field_name else  "type"
        self.maintain_type = maintain_type if maintain_type else False
        self.label_to_subtype = OrderedDict()
        self.subtype_to_label = OrderedDict()
        self.label_to_delegate = OrderedDict()
        self.subtype_to_delegate = OrderedDict()

    @classmethod
    def of(cls, base_type, type_field_name, maintain_type):
        return RuntimeTypeAdapterFactory(base_type, type_field_name, maintain_type)

    def register_subtype(self, subtype, label=None):
        if subtype is None:
            raise ValueError("No type values passed")
        if label == None:
            self.register_subtype(subtype, subtype.getSampleName())
        if subtype in self.subtype_to_label or label in self.label_to_subtype:
            raise ValueError("types and labels must be unique")
        self.label_to_subtype[label] = subtype
        self.subtype_to_label[subtype] = label
        return self

    def create(self, gson, type):
        if type != self.base_type:
            return None
        self.label_to_delegate = OrderedDict()
        self.subtype_to_delegate = OrderedDict()
        for entry in self.label_to_subtype.items():
            delegate = gson.get_delegate_adapter(self, entry[1])
            self.label_to_delegate[entry[0]] = delegate
            self.subtype_to_delegate[entry[1]] = delegate

        return custom_type_adapter(gson, type,
                                   self.type_field_name,
                                   self.maintain_type,
                                   self.label_to_delegate)

    def read(self, input):
        json_element = input.parse()
        label_json_element = None
        if self.maintain_type:
            label_json_element = json_element.as_json_object().get(self.type_field_name)
        else:
            label_json_element = json_element.as_json_object().remove(self.type_field_name)
        if label_json_element is None:
            raise json.JSONDecodeError("cannot deserialize " + self.base_type + " because it does not define a field named " + self.type_field_name)
        label = label_json_element.get_as_string()
        delegate = self.label_to_delegate.get(label)
        if delegate is None:
            raise json.JSONDecodeError("cannot deserialize " + self.base_type + " subtype named " + label + "; did you forget to register a subtype?")
        return delegate.from_json_tree(json_element)

    def write(self, out, value):
        src_type = value.__class__
        label = self.subtype_to_label.get(src_type)
        delegate = self.subtype_to_delegate.get(src_type)
        if delegate is None:
            raise json.JSONDecodeError("cannot serialize " + src_type.name + "; did you forget to register a subtype?")
        json_object = delegate.to_json_tree(value).as_json_object()
        if self.maintain_type:
            json.dump(json_object, out)
            return
        clone = OrderedDict()
        if json_object.has(self.type_field_name):
            raise json.JSONDecodeError("cannot serialize " + src_type.name + " because it already defines a field named " + self.type_field_name)
        clone[self.type_field_name] = {label: None}
        for entry in json_object.items():
            clone[entry[0]] = entry[1]
        json.dump(clone, out)


def object_hook(dct):
    pass


def parse_string(string, object_hook=None, parse_float=None, parse_int=None):
    pass
