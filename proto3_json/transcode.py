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
        message = self.message_cls()
        for key, value in json_encoded_message.iteritems():
            setattr(message, key, value)
        return message

    def to_json(self, message):
        return {
            name: getattr(message, name)
            for name in message.DESCRIPTOR.fields_by_name
        }
