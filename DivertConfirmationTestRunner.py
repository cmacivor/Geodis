import unittest
import MessageProcessor
import SortMessage
import DivertConfirmation
import datetime
import json

class TestDivertConfirmationMethods(unittest.TestCase):

    def test_json_to_divertConfirmationMessage(self):
        divertConfirmJson = self.getDivertConfirmationJson()
        convertedMessage = MessageProcessor.ConvertJsonToMessage(self, divertConfirmJson)

        divertConfirmationMsg = DivertConfirmation.DivertConfirmationMessage(convertedMessage.message)

        convertedDivertConfirmation = MessageProcessor.ConvertJsonToMessage(self, divertConfirmJson)

        divertConfirmatation = DivertConfirmation.DivertConfirmation(convertedDivertConfirmation.sequenceNumber, convertedDivertConfirmation.timeStamp, convertedDivertConfirmation.correlationId, divertConfirmationMsg)

        self.assertEqual(divertConfirmatation.sequenceNumber, "00004")
        self.assertEqual(divertConfirmatation.timeStamp, "2020-10-06T10:42:55")
        self.assertEqual(divertConfirmatation.messageName, "DVTCF")
        self.assertEqual(divertConfirmatation.correlationID, "20989c0a-7340-4fcb-a2ec-1564f64ed3fb")
        self.assertEqual(divertConfirmatation.message.reasonCode, "")
        self.assertEqual(divertConfirmatation.message.LaneActual, "L2")
        self.assertEqual(divertConfirmatation.message.status, "S")
        self.assertEqual(divertConfirmatation.message.lpId, "090000078760455")
        self.assertEqual(divertConfirmatation.message.orderId, "121294578")
        self.assertEqual(divertConfirmatation.message.shipId, "1")
        self.assertEqual(divertConfirmatation.message.wave, "2525166")
        self.assertEqual(divertConfirmatation.message.taskId, "287159079")
        self.assertEqual(divertConfirmatation.message.weight, "2.25")
        self.assertEqual(divertConfirmatation.message.width, "14")
        self.assertEqual(divertConfirmatation.message.length, "12")
        self.assertEqual(divertConfirmatation.message.containerType, "LG2")
        self.assertEqual(divertConfirmatation.message.carrier, "FEDX")
        self.assertEqual(divertConfirmatation.message.trackingNumber, "")
        self.assertEqual(divertConfirmatation.message.manifestId, "")
        self.assertEqual(divertConfirmatation.message.route, "")
        self.assertEqual(divertConfirmatation.message.sscc, "00000000000379916117")
        self.assertEqual(divertConfirmatation.message.accountNumber, "")
        self.assertEqual(divertConfirmatation.message.shipToPostalCode, "80013")
        self.assertEqual(divertConfirmatation.message.shipToState, "CO")
        self.assertEqual(divertConfirmatation.message.shipToCountry, "US")
        self.assertEqual(divertConfirmatation.message.shipDate, "")
    

    def getDivertConfirmationJson(self):
        divertConfirmationJson = '''
        {
            "sequenceNumber": "00004",
            "timeStamp": "2020-10-06T10:42:55",
            "messageName": "DVTCF",
            "correlationId": "20989c0a-7340-4fcb-a2ec-1564f64ed3fb",
            "message": {
                "reasonCode":"",
                "LaneActual":"L2",
                "status": "S",
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
                "shipDate": ""
            }
        }
        '''
        return divertConfirmationJson


if __name__ == '__main__':
    unittest.main()
    
