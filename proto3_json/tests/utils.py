class MessageMixin(object):
    """
    Helpers for Protobuf messages.

    """

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
