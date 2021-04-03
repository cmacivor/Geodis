import unittest
import MessageProcessor
import KeepAlive as KeepAliveMessage
import datetime
import json

class TestKeepAliveMethods(unittest.TestCase):

    def test_json_to_keepalive(self):
        testJson = '{"sequenceNumber":"2", "timeStamp": "2020-09-21T23:04:59", "messageName": "KEEP_ALIVE", "correlationId": "d9abc8ec-1253-4a1b-9230-6a085babd3bb", "status": "ACK" }'
        deserializedKeepAlivObj = MessageProcessor.ConvertJsonToMessage(self, testJson)
        
        keepAlive = KeepAliveMessage.KeepAlive(deserializedKeepAlivObj.sequenceNumber, deserializedKeepAlivObj.timeStamp, deserializedKeepAlivObj.correlationId)

        self.assertEqual(keepAlive.sequenceNumber, "2")
        self.assertEqual(keepAlive.timeStamp, "2020-09-21T23:04:59")
        self.assertEqual(keepAlive.messageName, "KEEP_ALIVE")
        self.assertEqual(keepAlive.correlationId, "d9abc8ec-1253-4a1b-9230-6a085babd3bb")

    def test_keepAlive_toJson(self):
        sequenceNumber = 2
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        correlationID = "ABC12345"

        keepAlive = KeepAliveMessage.KeepAlive(sequenceNumber, timestamp, correlationID)
        keepAliveJSON = MessageProcessor.ConvertMessageToJson(self, keepAlive)
        keepAliveDict = json.loads(keepAliveJSON)

        parsedSequenceNumber = keepAliveDict['sequenceNumber']
        self.assertEqual(sequenceNumber, parsedSequenceNumber)

        parsedTimeStamp = keepAliveDict['timeStamp']
        self.assertEqual(timestamp, parsedTimeStamp)

        parsedCorrelationId = keepAliveDict['correlationId']
        self.assertEqual(correlationID, parsedCorrelationId)
        self.assertEqual("KEEP_ALIVE", keepAliveDict["messageName"])


    def test_KeepAliveResponse_ToJson(self):
        #test data
        sequenceNumber = 2
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        correlationID = "ABC12345"

        keepAlive = KeepAliveMessage.KeepAliveResponse(sequenceNumber, timestamp, correlationID)
        keepAliveJSON = MessageProcessor.ConvertMessageToJson(self, keepAlive)
        keepAliveDict = json.loads(keepAliveJSON)

        parsedSequenceNumber = keepAliveDict['sequenceNumber']
        self.assertEqual(sequenceNumber, parsedSequenceNumber)

        parsedTimeStamp = keepAliveDict['timeStamp']
        self.assertEqual(timestamp, parsedTimeStamp)

        parsedCorrelationId = keepAliveDict['correlationId']
        self.assertEqual(correlationID, parsedCorrelationId)

        self.assertEqual("ACK", keepAliveDict['status'])
        self.assertEqual("KEEP_ALIVE", keepAliveDict["messageName"])

    def test_Json_ToKeepAliveResponse(self):
        testJson = '{"sequenceNumber":"2", "timeStamp": "2020-09-21T23:04:59", "messageName": "KEEP_ALIVE", "correlationId": "d9abc8ec-1253-4a1b-9230-6a085babd3bb", "status": "ACK" }'
        deserializedKeepAlivObj = MessageProcessor.ConvertJsonToMessage(self, testJson)

        keepAlive = KeepAliveMessage.KeepAliveResponse(deserializedKeepAlivObj.sequenceNumber, deserializedKeepAlivObj.timeStamp, deserializedKeepAlivObj.correlationId)

        self.assertEqual(keepAlive.sequenceNumber, "2")
        self.assertEqual(keepAlive.timeStamp, "2020-09-21T23:04:59")
        self.assertEqual(keepAlive.messageName, "KEEP_ALIVE")
        self.assertEqual(keepAlive.correlationId, "d9abc8ec-1253-4a1b-9230-6a085babd3bb")
        self.assertEqual(keepAlive.status, "ACK")
     

        

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()