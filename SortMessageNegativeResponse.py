class SortMessageNegativeResponse:
    def __init__(self, sequenceNumber, timestamp, correlationId, message):
        self.sequenceNumber = sequenceNumber
        self.timestamp = timestamp
        self.messageName = "CTRIN"
        self.correlationId = correlationId
        self.message = message

class SortMessageNegativeResponseContent:
     def __init__(self, lpId, error):
        self.status = "NAK"
        self.lpId = lpId
        self.error = error
