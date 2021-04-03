class SortMessagePositiveResponse:
    def __init__(self, sequenceNumber, timestamp, correlationId, message):
        self.sequenceNumber = sequenceNumber
        self.timestamp = timestamp
        self.messageName = "CTRIN"
        self.correlationId = correlationId
        self.message = message

class SortMessagePositiveResponseContent:

    def __init__(self, lpid):
        self.status = "ACK"
        self.lpId = lpid

