import unittest
import MessageProcessor
import SortMessage
import SortMessagePositiveResponse
import SortMessageNegativeResponse
import datetime
import json

class TestSortMessageMethods(unittest.TestCase):

    def test_json_to_sortmessage(self):
        sortMessageJson = self.getSortMessageJson()

        convertedJson = MessageProcessor.ConvertJsonToMessage(self, sortMessageJson)
        
        msg = convertedJson.message
        sortMessageContent = SortMessage.SortMessageContent(msg.status, msg.lpId, msg.orderId, msg.shipId, msg.wave, msg.taskId, msg.weight, msg.width, msg.length, msg.height, msg.containerType, 
                                        msg.carrier, msg.trackingNumber, msg.route, msg.sscc, msg.accountNumber, msg.shipToPostalCode, msg.shipToState, msg.shipToCountry, msg.shipDate, msg.ASNHDRPASSTHRUCHAR19)


        sortMessage = SortMessage.SortMessage(convertedJson.sequenceNumber, convertedJson.timeStamp, convertedJson.correlationId, sortMessageContent)
        
        self.assertEqual("00003", sortMessage.sequenceNumber)
        self.assertEqual("2020-10-06T10:42:55", sortMessage.timeStamp)
        self.assertEqual("CTRIN", sortMessage.messageName)
        self.assertEqual("473d41b6-f914-4f80-906d-1fe41250e598", sortMessage.correlationId)

        self.assertEqual("N", sortMessage.message.status)
        self.assertEqual("090000078760455", sortMessage.message.lpId)
        self.assertEqual("121294578", sortMessage.message.orderId)
        self.assertEqual("1", sortMessage.message.shipId)
        self.assertEqual("2525166", sortMessage.message.wave)
        self.assertEqual("287159079", sortMessage.message.taskId)
        self.assertEqual("2.25", sortMessage.message.weight)
        self.assertEqual("14", sortMessage.message.width)
        self.assertEqual("12", sortMessage.message.length)
        self.assertEqual("7.25", sortMessage.message.height)
        self.assertEqual("LG2", sortMessage.message.containerType)
        self.assertEqual("FEDX", sortMessage.message.carrier)
        self.assertEqual("", sortMessage.message.trackingNumber)
        #self.assertEqual("", sortMessage.message.manifestId)
        self.assertEqual("", sortMessage.message.route)
        self.assertEqual("00000000000379916117", sortMessage.message.sscc)
        self.assertEqual("", sortMessage.message.accountNumber)
        self.assertEqual("80013", sortMessage.message.shipToPostalCode)
        self.assertEqual("CO", sortMessage.message.shipToState)
        self.assertEqual("US", sortMessage.message.shipToCountry)
        self.assertEqual("", sortMessage.message.shipDate)
        self.assertEqual("USAMZON", sortMessage.message.ASNHDRPASSTHRUCHAR19)

    def test_sortMessage_to_json(self):
        #set up the SortMessage object
        sequenceNumber = "00003"
        timeStamp = "2020-10-06T10:42:55"
        messageName = "CTRIN"
        correlationId = "473d41b6-f914-4f80-906d-1fe41250e598"

        status = "N"
        lpid = "090000078760455"
        orderId = "121294578"
        shipId = "1"
        wave = "2525166"
        taskId = "287159079"
        weight = "2.25"
        width = "14"
        length = "12"
        height = "7.25"
        containerType = "LG2"
        carrier = "FEDX"
        trackingNumber = ""
        #manifestId = ""
        route = ""
        sscc = "00000000000379916117"
        accountNumber = ""
        shipToPostalCode = "80013"
        shipToState = "CO"
        shipToCountry = "US"
        shipDate = ""
        ASNHDRPASSTHRUCHAR19 = "USAMZON"

        content = SortMessage.SortMessageContent(status, lpid, orderId, shipId, wave, taskId, weight, width, length, height, containerType,
                                                    carrier, trackingNumber, route, sscc, accountNumber, shipToPostalCode, shipToState, shipToCountry, shipDate, ASNHDRPASSTHRUCHAR19)

        sortMessage = SortMessage.SortMessage(sequenceNumber, timeStamp, correlationId, content)

        #Convert the SortMessage to JSON
        sortMessageJson = MessageProcessor.ConvertMessageToJson(self, sortMessage)
     
        #get the values of the JSON string
        sortMessageDict = json.loads(sortMessageJson)

        self.assertEqual(sortMessageDict["sequenceNumber"], sequenceNumber)
        self.assertEqual(sortMessageDict["timeStamp"], timeStamp)
        self.assertEqual(sortMessageDict["messageName"], messageName)
        self.assertEqual(sortMessageDict["correlationId"], correlationId)

        message = sortMessageDict["message"]

        self.assertEqual(message["status"], status)
        self.assertEqual(message["lpId"], lpid)
        self.assertEqual(message["orderId"], orderId)
        self.assertEqual(message["shipId"], shipId)
        self.assertEqual(message["wave"], wave)
        self.assertEqual(message["taskId"], taskId)
        self.assertEqual(message["weight"], weight)
        self.assertEqual(message["width"], width)
        self.assertEqual(message["length"], length)
        self.assertEqual(message["height"], height)
        self.assertEqual(message["containerType"], containerType)
        self.assertEqual(message["carrier"], carrier)
        self.assertEqual(message["trackingNumber"], trackingNumber)
        #self.assertEqual(message["manifestId"], manifestId)
        self.assertEqual(message["route"], route)
        self.assertEqual(message["sscc"], sscc)
        self.assertEqual(message["accountNumber"], accountNumber)
        self.assertEqual(message["shipToPostalCode"], shipToPostalCode)
        self.assertEqual(message["shipToState"], shipToState)
        self.assertEqual(message["shipToCountry"], shipToCountry)
        self.assertEqual(message["shipDate"], shipDate)
        self.assertEqual(message["ASNHDRPASSTHRUCHAR19"],  ASNHDRPASSTHRUCHAR19)
    

    def test_positive_sortMessage_To_Json(self):
        sequenceNumber = "00005"
        timestamp = "2020-10-06T10:43:08"
        messageName = " CTRIN "
        correlationId = "673d41b6-f914-4f80-906d-1fe41250e598"
        lpid = "090000078765459"

        content = SortMessagePositiveResponse.SortMessagePositiveResponseContent(lpid)
        positiveResponse = SortMessagePositiveResponse.SortMessagePositiveResponse(sequenceNumber, timestamp, correlationId, content)

        jsonResponse = MessageProcessor.ConvertMessageToJson(self, positiveResponse)

        parsedJson = json.loads(jsonResponse)

        content = parsedJson["message"]

        self.assertEqual(sequenceNumber, parsedJson["sequenceNumber"])
        self.assertEqual(timestamp, parsedJson["timeStamp"])
        self.assertEqual(correlationId, parsedJson["correlationId"])
        self.assertEqual(lpid, content["LPID"])
        self.assertEqual("ACK", content["status"])
    
    def test_json_to_positive_sortMessageResponse(self):
        json = self.getPositiveSortMessageResponse()

        positiveMessage = MessageProcessor.ConvertJsonToMessage(self, json)
        content = SortMessagePositiveResponse.SortMessagePositiveResponseContent(positiveMessage.message.lpId)
        response = SortMessagePositiveResponse.SortMessagePositiveResponse(positiveMessage.sequenceNumber, positiveMessage.timestamp, positiveMessage.correlationId, content)

        self.assertEqual("00005", response.sequenceNumber)
        self.assertEqual("2020-10-06T10:43:08", response.timeStamp)
        self.assertEqual("CTRIN", response.messageName)
        self.assertEqual("673d41b6-f914-4f80-906d-1fe41250e598", response.correlationId)
        self.assertEqual("ACK", response.message.status)
        self.assertEqual("090000078760738", response.message.LPID)
    
    def test_json_to_negative_sortMessageResponse(self):
        json = self.getNegativeSortMessageResponse()
        error = "error occurred"

        negativeMessage = MessageProcessor.ConvertJsonToMessage(self, json)
        content = SortMessageNegativeResponse.SortMessageNegativeResponseContent(error)
        response = SortMessageNegativeResponse.SortMessageNegativeResponse(negativeMessage.sequenceNumber, negativeMessage.timestamp, negativeMessage.correlationId, content)
   
        self.assertEqual("00005", response.sequenceNumber)
        self.assertEqual("2020-10-06T10:43:08", response.timeStamp)
        self.assertEqual("CTRIN", response.messageName)
        self.assertEqual("673d41b6-f914-4f80-906d-1fe41250e598", response.correlationId)
        self.assertEqual("NAK", response.message.status)
        self.assertEqual("error occurred", response.message.error)

    
    def getNegativeSortMessageResponse(self):
        negativeSortMessageResponse = '''
        {
            "sequenceNumber": "00005",
            "timestamp": "2020-10-06T10:43:08",
            "messageName": " CTRIN ",
            "correlationId": "673d41b6-f914-4f80-906d-1fe41250e598",
            "message": {
                "status": "NAK",
                "error": "error occurred"
            }
        }
        '''
        return negativeSortMessageResponse

    def getPositiveSortMessageResponse(self):
        positiveSortMessageResponse = '''
        {
            "sequenceNumber": "00005",
            "timestamp": "2020-10-06T10:43:08",
            "messageName": " CTRIN ",
            "correlationId": "673d41b6-f914-4f80-906d-1fe41250e598",
            "message": {
                "status": "ACK",
                "lpId": "090000078760738"
            }
        }
        '''
        return positiveSortMessageResponse

    
    def getSortMessageJson(self):
        sortMessageJson = ''' 
        {
            "sequenceNumber": "00003",
            "timeStamp": "2020-10-06T10:42:55",
            "messageName": "CTRIN",
            "correlationId": "473d41b6-f914-4f80-906d-1fe41250e598",
            "message": {
                "status": "N",
                "lpId": "090000078760455",
                "orderId": "121294578",
                "shipId": "1",
                "wave": "2525166",
                "taskId": "287159079",
                "weight": "2.25",
                "width": "14",
                "length": "12",
                "height": "7.25",
                "containerType": "LG2",
                "carrier": "FEDX",
                "trackingNumber": "",
                "manifestId": "",
                "route": "",
                "sscc": "00000000000379916117",
                "accountNumber": "",
                "shipToPostalCode": "80013",
                "shipToState": "CO",
                "shipToCountry": "US",
                "shipDate": "",
                "ASNHDRPASSTHRUCHAR19": "USAMZON" 
            }
        }'''

        return sortMessageJson


        




if __name__ == '__main__':
    unittest.main()
