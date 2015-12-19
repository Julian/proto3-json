from unittest import TestCase

from google.protobuf import reflection
from google.protobuf.descriptor import Descriptor
from hypothesis import example, given
from hypothesis_protobuf.strategies import message

from proto3_json.transcode import Transcoder


class TestTranscode(TestCase):
    def assertMessagesEqual(self, message, other):
        # We don't use addTypeEqualityFunc, it doesn't work on
        # subclasses so you'd have to add it before comparing any
        # descriptors / messages anyhow.
        if message == other:
            return
        self.assertEqual(
            message.SerializeToString(), other.SerializeToString(),
        )
        self.assertEqual(message.ListFields(), other.ListFields())
        self.fail("XXX")

    def assertRoundtrips(self, message, transcoder=None):
        if transcoder is None:
            transcoder = Transcoder(message_cls=message.__class__)
        roundtripped = transcoder.from_json(transcoder.to_json(message))
        self.assertMessagesEqual(roundtripped, message)

    @example(
        message=reflection.MakeClass(
            descriptor=Descriptor(
                name="Empty",
                full_name="Empty",
                containing_type=None,
                filename=None,
                fields=[],
                nested_types=[],
                enum_types=[],
                extensions=[],
            ),
        )()
    )
    @given(message)
    def test_it_round_trips(self, message):
        self.assertRoundtrips(message=message)
