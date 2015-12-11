from unittest import TestCase

from google.protobuf import reflection
from google.protobuf.descriptor import Descriptor, FieldDescriptor
from hypothesis import given, strategies

from proto3_json.transcode import Transcoder


full_name = strategies.binary()
index = strategies.integers(min_value=0)
tag_number = strategies.integers(
    min_value=1,
    max_value=FieldDescriptor.MAX_FIELD_NUMBER,
)
field_type = strategies.sampled_from(
    [
        FieldDescriptor.TYPE_DOUBLE,
        FieldDescriptor.TYPE_FLOAT,
        FieldDescriptor.TYPE_INT64,
        FieldDescriptor.TYPE_UINT64,
        FieldDescriptor.TYPE_INT32,
        FieldDescriptor.TYPE_FIXED64,
        FieldDescriptor.TYPE_FIXED32,
        FieldDescriptor.TYPE_BOOL,
        FieldDescriptor.TYPE_STRING,
        FieldDescriptor.TYPE_GROUP,
        FieldDescriptor.TYPE_MESSAGE,
        FieldDescriptor.TYPE_BYTES,
        FieldDescriptor.TYPE_UINT32,
        FieldDescriptor.TYPE_ENUM,
        FieldDescriptor.TYPE_SFIXED32,
        FieldDescriptor.TYPE_SFIXED64,
        FieldDescriptor.TYPE_SINT32,
        FieldDescriptor.TYPE_SINT64,
    ],
)
cpp_type = strategies.sampled_from(
    [
        FieldDescriptor.CPPTYPE_INT32,
        FieldDescriptor.CPPTYPE_INT64,
        FieldDescriptor.CPPTYPE_UINT32,
        FieldDescriptor.CPPTYPE_UINT64,
        FieldDescriptor.CPPTYPE_DOUBLE,
        FieldDescriptor.CPPTYPE_FLOAT,
        FieldDescriptor.CPPTYPE_BOOL,
        FieldDescriptor.CPPTYPE_ENUM,
        FieldDescriptor.CPPTYPE_STRING,
        FieldDescriptor.CPPTYPE_MESSAGE,
    ],
)
label = strategies.just(FieldDescriptor.LABEL_OPTIONAL)
default_value = strategies.none()
field = strategies.builds(
    FieldDescriptor,
    name=strategies.binary(),
    full_name=full_name,
    index=index,
    number=tag_number,
    type=field_type,
    cpp_type=cpp_type,
    label=label,
    default_value=default_value,
    message_type=strategies.none(),
    enum_type=strategies.none(),
    containing_type=strategies.none(),
    is_extension=strategies.just(False),
    extension_scope=strategies.none(),
)
descriptor = strategies.builds(
    Descriptor,
    name=strategies.binary(),
    full_name=full_name,
    containing_type=strategies.none(),  # TODO: strategies.recursive?
    filename=strategies.none(),
    fields=strategies.lists(field),
    nested_types=strategies.just([]),
    enum_types=strategies.just([]),
    extensions=strategies.just([]),
)
Message = strategies.builds(reflection.MakeClass, descriptor)
message = strategies.builds(Message)


class TestTranscode(TestCase):
    @given(Message)
    def test_it_round_trips(self, Message):
        transcoder = Transcoder(message_cls=Message)
        self.assertEqual(
            transcoder.from_json(transcoder.to_json(Message())),
            Message(),
        )

    def test_it_round_trips_an_empty_descriptor(self):
        descriptor = Descriptor(
            name="Empty",
            full_name="Empty",
            containing_type=None,
            filename=None,
            fields=[],
            nested_types=[],
            enum_types=[],
            extensions=[],
        )
        Message = reflection.MakeClass(descriptor)
        transcoder = Transcoder(message_cls=Message)
        self.assertEqual(
            transcoder.from_json(transcoder.to_json(Message())),
            Message(),
        )
