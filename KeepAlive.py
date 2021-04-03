class KeepAlive:
    def __init__(self, sequenceNumber, timeStamp, correlationId):
        self.sequenceNumber = sequenceNumber
        self.timestamp = timeStamp
        self.messageName = "KEEP_ALIVE"
        self.correlationId = correlationId
        

class KeepAliveResponse:
    def __init__(self, sequenceNumber, timeStamp, correlationId):
        self.sequenceNumber = sequenceNumber
        self.messageName = "KEEP_ALIVE"
        self.timestamp = timeStamp
        self.correlationId = correlationId
        self.status = "ACK"
