import socket
import time
import sys
import traceback
import python_config
import MessageProcessor
import KeepAlive as KeepAliveMessage
import GlobalConstants
import pyodbc
import datetime
import SQLServerConn
import Logger
import json
import logging
from logging.handlers import RotatingFileHandler

loggingConfig = python_config.read_logging_config()
logFileLocation = loggingConfig.get('divertserverfilelocation')

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = logFileLocation 

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)


def removeHexadecimalsFromMessage(message):
      #get rid of the ASCII characters
      decoded = message.decode('ascii')
      processedMessage = decoded.replace("\x02", "").replace("\x03", "")

      return processedMessage


def saveDivertConfirmationResponse(message):
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        currentTimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = "INSERT INTO dbo.DivertConfirmationResponses (Content, IsProcessed, CreatedAt, UpdatedAt) VALUES (?, ?, ?, ?)"

        cursor.execute(sql, message, 0, currentTimeStamp, currentTimeStamp)

        conn.commit()

        cursor.close()
        conn.close()


    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exceptionDetails = ''.join('!! ' + line for line in lines)
        print(''.join('!! ' + line for line in lines))
        app_log.error(exceptionDetails)


def updateContainerMasterRecordByCorrelationId(correlationId):

    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        currentTimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = "UPDATE dbo.container_master SET IsAck = 1, UpdatedAt = ? WHERE correlationId = ?"

        cursor.execute(sql, currentTimeStamp, correlationId)
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exceptionDetails = ''.join('!! ' + line for line in lines)
        print(''.join('!! ' + line for line in lines))
        app_log.error(exceptionDetails)


def setUpAckResponse(ackResponse):
    ackResponseJSON = MessageProcessor.ConvertMessageToJson(None, ackResponse)

    concatMessage = GlobalConstants.StartTransmissionCharacter + ackResponseJSON + GlobalConstants.EndTransmissionCharacter

    encodedMessage = concatMessage.encode('ascii')

    return encodedMessage


def constructAckMessage(data):
    preProcessedMessage = data.replace("\x02", "").replace("\x03", "")  
    deserializedKeepAliveMessageObj = MessageProcessor.ConvertJsonToMessage(None, preProcessedMessage) 
    ackResponse = KeepAliveMessage.KeepAliveResponse(deserializedKeepAliveMessageObj.sequenceNumber, deserializedKeepAliveMessageObj.timestamp, deserializedKeepAliveMessageObj.correlationId)
    encodedAckResponse = setUpAckResponse(ackResponse)
    return encodedAckResponse

def multi_split(s, sep):
    stack = [s]
    for char in sep:
        pieces = []
        for substr in stack:
            pieces.extend(substr.split(char))
        stack = pieces
    return stack

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    loggingConfig = python_config.read_logging_config()
    auth = loggingConfig.get('auth')
    domain = loggingConfig.get('domain')
    api = loggingConfig.get("api")
    url = domain + api

    serverParams = python_config.read_server_config()
    host = serverParams.get('host')
    port = int(serverParams.get('dvtcfackport'))
    bufferSize = int(serverParams.get('divertconfirmserverbuffer'))
    print('Listening on HOST: ' + str(host) + ' and PORT: ' + str(port))


    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    data = b''
    with conn:
        print("Connected by", addr)
        while True:
            try:

                chunk = conn.recv(bufferSize)

                if not chunk:
                    break

                data += chunk
                
                decodedData = data.decode('ascii')
                
                print(' wrote ' + decodedData)

                if "KEEP_ALIVE" in decodedData and "ACK" not in decodedData: 
                    separatedMessages = multi_split(decodedData, [GlobalConstants.StartTransmissionCharacter, GlobalConstants.EndTransmissionCharacter])
                    for message in separatedMessages:
                        if is_json(message):
                            ackResponse = constructAckMessage(message)
                            conn.sendall(ackResponse)
                            print("Responded to Keep Alive.")
                else:
                    separatedMessages = multi_split(decodedData, [GlobalConstants.StartTransmissionCharacter, GlobalConstants.EndTransmissionCharacter])
                    for message in separatedMessages:
                        if is_json(message):
                            saveDivertConfirmationResponse(message)
                            #Logger.log("WMSDVTCF", "INFO", "divert confirm response saved")
                            convertedMessage = MessageProcessor.ConvertJsonToMessage(None, message)
                            updateContainerMasterRecordByCorrelationId(convertedMessage.correlationId)
                            print("DVTCF response saved, master record updated")

               #clear the buffer
                data = b''
              

            except socket.error:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                exceptionDetails = ''.join('!! ' + line for line in lines)
                print(''.join('!! ' + line for line in lines))
                app_log.error(exceptionDetails)
