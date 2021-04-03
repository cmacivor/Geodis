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
import DivertConfirmation
import Logger
import logging
from logging.handlers import RotatingFileHandler
import decimal

loggingConfig = python_config.read_logging_config()
logFileLocation = loggingConfig.get('divertclientfilelocation')

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = logFileLocation #'C:\\socketserver\\DivertConfirmationClientLog'

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)


#this needs to look for the most recent Acknowledged message
def getMostRecentMessage():
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        sql = "select top 1 * from dbo.container_master WHERE VerifyProcessed = 1 and IsAck = 0 order by CreatedAt desc"

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


def getContainerMasterRecordsToProcess():
    try:

        conn = SQLServerConn.get()

        cursor = conn.cursor()

        sql = "select * from dbo.container_master WHERE VerifyProcessed = 1 and IsAck = 0 order by CreatedAt desc"

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




def constructKeepAliveMessage(counter):
 
    currentTimeStamp =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    correlationId = str(uuid.uuid4())

    keepAlive = KeepAliveMessage.KeepAlive(counter, currentTimeStamp, correlationId)
    
    keepAliveJSON = MessageProcessor.ConvertMessageToJson(None, keepAlive)

    concatMessage = GlobalConstants.StartTransmissionCharacter + keepAliveJSON + GlobalConstants.EndTransmissionCharacter

    encodedMessage = concatMessage.encode('ascii')

    return encodedMessage


def constructDivertConfirmMessage(counter):
    serverParams = python_config.read_server_config()
    cycleinterval = float(serverParams.get('divertconfirmclientinterval'))
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
    
    responses = list()
    containerMasterRecords =  getContainerMasterRecordsToProcess()
    for record in containerMasterRecords:
        divertConfirmMessage = DivertConfirmation.DivertConfirmationMessage(record)

        currentTimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        divertConfirm = DivertConfirmation.DivertConfirmation(counter, currentTimeStamp, record[2], divertConfirmMessage)

        convertedJson = MessageProcessor.ConvertMessageToJson(None, divertConfirm)
            
        #concatenate the STX and ETX characters
        concatenatedMessage = GlobalConstants.StartTransmissionCharacter + convertedJson + GlobalConstants.EndTransmissionCharacter

        encodedMessage = concatenatedMessage.encode('ascii')
        #Logger.log("WXS", "DVTCF", "Divert Confirm sent to Geodis")
        responses.append(encodedMessage)
        #return encodedMessage
    
    return responses


    

serverParams = python_config.read_server_config()
host = serverParams.get('remotehost')
dvtcfport = serverParams.get('dvtcfport')

HOST = host # The server's hostname or IP address
PORT = int(dvtcfport) # The port used by the server


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


        #1. build and send the Divert Confirm message
        strCounter = str(counter)
        divertConfirmMessage = constructDivertConfirmMessage(strCounter)
        if divertConfirmMessage and not isinstance(divertConfirmMessage, list):
            clientSocket.sendall(divertConfirmMessage)
        elif divertConfirmMessage and len(divertConfirmMessage) > 0:
            for message in divertConfirmMessage:
                clientSocket.sendall(message)
                print("message sent.")
        
    except socket.error:
        #print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exceptionDetails = ''.join('!! ' + line for line in lines)
        print(''.join('!! ' + line for line in lines))
        app_log.error(exceptionDetails)

        #set connection status and recreate socket
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
