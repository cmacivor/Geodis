class DivertConfirmation:
    def __init__(self, sequenceNumber, timestamp, correlationId, message):
        self.sequenceNumber = sequenceNumber
        self.timestamp = timestamp
        self.messageName = "DVTCF"
        self.correlationId = correlationId
        self.message = message

#used to convert container_master table to JSOn
class DivertConfirmationMessage:
    def __init__(self, message):
        self.status = message[3]
        self.lpId = str(message[1])
        self.laneActual = str(message[23])
        self.reasonCode = str(message[24])
        self.orderId = str(message[4])
        self.shipId = str(message[5])
        self.wave = str(message[6])
        self.taskId = str(message[7])
        self.weight = str(message[8])
        self.width = str(message[9])
        self.length = str(message[10])
        self.height = str(message[11])
        self.containerType = str(message[12])
        self.carrier = str(message[13])
        self.trackingNumber = str(message[14])
        self.manifestId = ""
        self.route = ""
        self.SSCC = str(message[15])
        self.accountNumber = str(message[16])
        self.shipToPostalCode = str(message[17])
        self.shipToState = message[18]
        self.shipToCountry = message[19]
        self.shipDate = str(message[20])




        
        
        


        
        
        
