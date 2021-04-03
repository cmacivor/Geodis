class SortMessage:

    def __init__(self, sequenceNumber, timeStamp, correlationId, sortMessageContent):
        self.sequenceNumber = sequenceNumber
        self.timeStamp = timeStamp
        self.messageName = "CTRIN"  
        self.correlationId = correlationId
        self.message = sortMessageContent



class SortMessageContent:
    def __init__(self, status, lpid, orderID, shipID, wave, taskID, weight, width, length, height, containerType, carrier, trackingNumber, 
    route, sscc, accountNumber, shipToPostalCode, shipToState, shipToCountry, shipDate, asdnHDR):
        self.status = status
        self.lpId = lpid
        self.orderId = orderID
        self.shipId = shipID
        self.wave = wave
        self.taskId = taskID
        self.weight = weight
        self.width = width
        self.length = length
        self.height = height
        self.containerType = containerType
        self.carrier = carrier
        self.trackingNumber = trackingNumber
        self.route = route
        self.SSCC = sscc
        self.accountNumber = accountNumber
        self.shipToPostalCode = shipToPostalCode
        self.shipToState = shipToState
        self.shipToCountry = shipToCountry
        self.shipDate = shipDate
        self.ASNHDRPASSTHRUCHAR19 = asdnHDR





