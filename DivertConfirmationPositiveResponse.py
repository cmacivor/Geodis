class DivertConfirmationPositiveResponse:
    def _init_(self, sequenceNumber, timestamp, messageName, correlationID, message):
        self.SequenceNumber = sequenceNumber
        self.MessageName = "DVTCF"
        self.TimeStamp = timestamp
        self.CorrelationID = correlationID
        self.Message = message

class DivertConfirmPosMessage:
    def _init_(self):
        self.Status = "ACK"

