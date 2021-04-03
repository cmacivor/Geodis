import socket
import time
import sys
import traceback
import python_config
import MessageProcessor
import KeepAlive as KeepAliveMessage
import GlobalConstants
import SortMessage
import SortMessagePositiveResponse
import SortMessageNegativeResponse
import pyodbc
import SQLServerConn
import datetime
import uuid
import Logger
import logging
from logging.handlers import RotatingFileHandler

loggingConfig = python_config.read_logging_config()
logFileLocation = loggingConfig.get('sortclientfilelocation')

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = logFileLocation #'C:\\socketserver\\DivertConfirmationClientLog'

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)

def constructKeepAliveMessage(counter):
 
    currentTimeStamp =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    correlationId = str(uuid.uuid4())

    keepAlive = KeepAliveMessage.KeepAlive(counter, currentTimeStamp, correlationId)
    
    keepAliveJSON = MessageProcessor.ConvertMessageToJson(None, keepAlive)

    concatMessage = GlobalConstants.StartTransmissionCharacter + keepAliveJSON + GlobalConstants.EndTransmissionCharacter

    encodedMessage = concatMessage.encode('ascii')

    return encodedMessage


def getMostRecentMessage():
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        sql = "select top 1 * from dbo.SortMessages WHERE IsAck = 0 AND Type='CTRIN' order by created_at asc"

        cursor.execute(sql)

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exceptionDetails = ''.join('!! ' + line for line in lines)
        print(''.join('!! ' + line for line in lines))
        app_log.error(exceptionDetails)
        #Logger.log("TCP_SortMessage_Server", "Error", exceptionDetails)



#will use this to save to the database, after sending the ACK message
#this gets the oldest message
def getNextSortMessageToProcess():
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        sql = "select top 1 * from dbo.SortMessages where isAck = 0 order by Id"

        cursor.execute(sql)

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exceptionDetails = ''.join('!! ' + line for line in lines)
        print(''.join('!! ' + line for line in lines))
        app_log.error(exceptionDetails)


def getSortMessagesToProcess():
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        sql = "select * from dbo.SortMessages where isAck = 0 order by Id"

        cursor.execute(sql)

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exceptionDetails = ''.join('!! ' + line for line in lines)
        print(''.join('!! ' + line for line in lines))
        app_log.error(exceptionDetails)




def updateMessageAsAcknowledged(sortMessageId):
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        currentTimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #sql = "UPDATE dbo.SortMessages SET IsAck = 1 WHERE Id = " + str(sortMessageId)
        sql = "UPDATE dbo.SortMessages SET IsAck = 1, updated_at = ? WHERE Id = ?"

        cursor.execute(sql, currentTimeStamp, sortMessageId)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exceptionDetails = ''.join('!! ' + line for line in lines)
        print(''.join('!! ' + line for line in lines))
        app_log.error(exceptionDetails)
        #Logger.log("TCP_SortMessage_Server", "Error", exceptionDetails)


def handleInboundSortMessage(convertedMessage):

    if not convertedMessage.message.lpId:
       negativeResponseContent = SortMessageNegativeResponse.SortMessageNegativeResponseContent(convertedMessage.message.lpId, "No LPID")
       negativeResponse = SortMessageNegativeResponse.SortMessageNegativeResponse(convertedMessage.sequenceNumber, convertedMessage.timestamp, convertedMessage.correlationId, negativeResponseContent)
       negativeResponseJSON = MessageProcessor.ConvertMessageToJson(None, negativeResponse)
       return negativeResponseJSON
       
    if not convertedMessage.message.weight:
       negativeResponseContent = SortMessageNegativeResponse.SortMessageNegativeResponseContent(convertedMessage.message.lpId, "No Weight")
       negativeResponse = SortMessageNegativeResponse.SortMessageNegativeResponse(convertedMessage.sequenceNumber, convertedMessage.timestamp, convertedMessage.correlationId, negativeResponseContent)
       negativeResponseJSON = MessageProcessor.ConvertMessageToJson(None, negativeResponse)
       return negativeResponseJSON

    if not convertedMessage.message.carrier:
       negativeResponseContent = SortMessageNegativeResponse.SortMessageNegativeResponseContent(convertedMessage.message.lpId, "No Carrier")
       negativeResponse = SortMessageNegativeResponse.SortMessageNegativeResponse(convertedMessage.sequenceNumber, convertedMessage.timestamp, convertedMessage.correlationId, negativeResponseContent)
       negativeResponseJSON = MessageProcessor.ConvertMessageToJson(None, negativeResponse)
       return negativeResponseJSON

    
    positiveResponseContent = SortMessagePositiveResponse.SortMessagePositiveResponseContent(convertedMessage.message.lpId)
    positiveResponse = SortMessagePositiveResponse.SortMessagePositiveResponse(convertedMessage.sequenceNumber, convertedMessage.timestamp, convertedMessage.correlationId, positiveResponseContent)
    positiveResponseJSON = MessageProcessor.ConvertMessageToJson(None, positiveResponse)
    decodedPositiveResponseJSON = positiveResponseJSON

    return decodedPositiveResponseJSON



def constructAckMessage(counter):
    serverParams = python_config.read_server_config()
    cycleinterval = float(serverParams.get('sortmessageclientinterval'))
    time.sleep(cycleinterval)

    keepAliveInterval = serverParams.get('keepaliveinterval')
    keepAliveTimeDelay = serverParams.get('keepalivetimedelay')

    mostRecentMessage = getMostRecentMessage()
    if mostRecentMessage is None or len(mostRecentMessage) == 0:
        print("no unprocessed and unacknowledged records in container master table.")
        
        global currentTimeStampKeepAlive
        timeDifference = datetime.datetime.now() - currentTimeStampKeepAlive
        if timeDifference.total_seconds() > int(keepAliveTimeDelay):
            keepAlive = constructKeepAliveMessage(counter)
            Logger.log("WXS", "KEEP_ALIVE", "")
            print("More than 60 seconds since last Divert Confirm Response sent from Geodis...sending Keep Alive...")
            #time.sleep(int(keepAliveInterval))
            currentTimeStampKeepAlive = datetime.datetime.now()
            return keepAlive
        else:
            return
    else:
        currentTimeStampKeepAlive = datetime.datetime.now()



    #if it's been less than 30 seconds, get the most recent message not marked as Acknowledged
    #mostRecentUnProcessedMessage = getNextSortMessageToProcess()

    unprocessedMessages = getSortMessagesToProcess()

    if unprocessedMessages is None or len(unprocessedMessages) == 0: 
            return

    responses = list()
    for message in unprocessedMessages:
        
        #convert the JSON to an object
        convertedMessage = MessageProcessor.ConvertJsonToMessage(None, message[1])

        if "CTRIN" in message[1]:
            
            #make the ACK message from the CTRIN message
            sortMessageReponse = handleInboundSortMessage(convertedMessage)
            concatSortMessageResponse = GlobalConstants.StartTransmissionCharacter + sortMessageReponse + GlobalConstants.EndTransmissionCharacter
            encodedSortMessageResponse = concatSortMessageResponse.encode('ascii')
            responses.append(encodedSortMessageResponse)

                #update the db record as ACK
            updateMessageAsAcknowledged(message[0])
            #Logger.log("WXS", "INFO",  "Sort Message updated")
            
            #return encodedSortMessageResponse
    return responses


serverParams = python_config.read_server_config()
host = serverParams.get('remotehost')
ctrinackport = serverParams.get('ctrinackport')

HOST = host #'127.0.0.1'  # The server's hostname or IP address
PORT = int(ctrinackport)  #31001  # The port used by the server



clientSocket = socket.socket()
clientSocket.connect((HOST, PORT))

connected = True
print("connected to server")
counter = 0
reconnectionAttempts = 0
global currentTimeStampKeepAlive 
currentTimeStampKeepAlive = datetime.datetime.now() 
while True:
    try:
        counter = counter + 1
        currentTimeStamp = datetime.datetime.now() 

        #mark the record as acknowledged, then build and send the ACK message
        ackMessages = constructAckMessage(str(counter))
        if ackMessages and not isinstance(ackMessages, list):
            clientSocket.sendall(ackMessages)
        elif ackMessages and len(ackMessages) > 0:
            for message in ackMessages:
                #print('sending ACK: ' + message)
                clientSocket.sendall(message)
            #clientSocket.sendall(ackMessage)
           

    except socket.error:
        #set connection status and recreate socket
        
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exceptionDetails = ''.join('!! ' + line for line in lines)
        print(''.join('!! ' + line for line in lines))
        app_log.error(exceptionDetails)
        connected = False
        clientSocket = socket.socket()
        print("connection lost...reconnecting")

        while not connected:
            reconnectionAttempts = reconnectionAttempts + 1
            print('reconnection attempt number: ' + str(reconnectionAttempts))
            # attempt to reconnect, otherwise sleep for 2 seconds
            try:
                clientSocket.connect((HOST, PORT))
                connected = True
                print("re-connection successful")
            except socket.error:
                time.sleep(2) # this is the pause between reconnection attempt






   