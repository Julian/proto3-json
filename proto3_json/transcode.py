from characteristic import Attribute, attributes



@attributes(
    [
        Attribute(name="message_cls"),
    ],
)
class Transcoder(object):
    """
    Convert between Protobufs and JSON using the canonical JSON encoding.

    """

    def from_json(self, json_encoded_message):
        return self.message_cls()

    def to_json(self, message):
        return {}
