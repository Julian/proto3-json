from unittest import TestCase

from google.protobuf import reflection
from google.protobuf.descriptor import Descriptor
from hypothesis import given, strategies

from proto3_json.transcode import Transcoder


descriptor = strategies.builds(
    Descriptor,
    name=strategies.binary(),
    full_name=strategies.binary(),
    containing_type=strategies.none(),  # TODO: strategies.recursive?
    filename=strategies.none(),
    fields=strategies.just([]),
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
