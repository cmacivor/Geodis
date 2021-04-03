class DivertConfirmationNegativeResponse:
    def _init_(self, sequenceNumber, timestamp, messageName, correlationID, message):
        self.SequenceNumber = sequenceNumber
        self.Timestamp = timestamp
        self.MessageName = "DVCTF"
        self.CorrelationID = correlationID
        self.Message = message

class DivertConfirmNegMessage:
    def _init_(self):
        self.Status = "NAK"
        self.Error = "ManifestId missing"