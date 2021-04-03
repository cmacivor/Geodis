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
import datetime
import SQLServerConn
import Logger
import json
import logging
from logging.handlers import RotatingFileHandler

loggingConfig = python_config.read_logging_config()
logFileLocation = loggingConfig.get('sortserverfilelocation')

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = logFileLocation 

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)


def setUpAckResponse(ackResponse):
    ackResponseJSON = MessageProcessor.ConvertMessageToJson(None, ackResponse)

    concatMessage = GlobalConstants.StartTransmissionCharacter + ackResponseJSON + GlobalConstants.EndTransmissionCharacter

    encodedMessage = concatMessage.encode('ascii')

    return encodedMessage


def constructAckMessage(data):
    deserializedSortMessageObj = MessageProcessor.ConvertJsonToMessage(None, data)
    if deserializedSortMessageObj.messageName == "CTRIN":  
        ackResponse = KeepAliveMessage.KeepAliveResponse(deserializedSortMessageObj.sequenceNumber, deserializedSortMessageObj.timeStamp, deserializedSortMessageObj.correlationId)
        encodedAckResponse = setUpAckResponse(ackResponse)
        return encodedAckResponse
    if  deserializedSortMessageObj.messageName == "KEEP_ALIVE": #it's a keep alive 
        ackResponse = KeepAliveMessage.KeepAliveResponse(deserializedSortMessageObj.sequenceNumber, deserializedSortMessageObj.timestamp, deserializedSortMessageObj.correlationId)
        encodedAckResponse = setUpAckResponse(ackResponse)
        return encodedAckResponse


def removeHexadecimalsFromMessage(message):
      #get rid of the ASCII characters
      decoded = message.decode('ascii')
      processedMessage = decoded.replace("\x02", "").replace("\x03", "")

      return processedMessage

def convertJsonToAnonymousObject(message):
    preProcessedMessage = removeHexadecimalsFromMessage(message)

    convertedObj = MessageProcessor.ConvertJsonToMessage(None, preProcessedMessage)

    return convertedObj


def saveSortMessage(sortMessage):
      messageObj = MessageProcessor.ConvertJsonToMessage(None, sortMessage)

      if messageObj.messageName == "KEEP_ALIVE":
          Logger.log("WMS", "KEEP_ALIVE", "")
      else:
          addMessageToSortMessageTable(sortMessage, False)
          #Logger.log("WMS", "CTRIN", sortMessage)

def addMessageToSortMessageTable(sortMessage, isKeepAlive):    
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        currentTimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = 'INSERT INTO lego_outbound.dbo.SortMessages (Content, IsAck, IsProcessed, Type, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)'

        if isKeepAlive:
            cursor.execute(sql, sortMessage, str(0), str(0), "KEEP_ALIVE", currentTimeStamp, currentTimeStamp)
        else:
            cursor.execute(sql, sortMessage, str(0), str(0), "CTRIN", currentTimeStamp, currentTimeStamp)

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exceptionDetails = ''.join('!! ' + line for line in lines)
        print(''.join('!! ' + line for line in lines))
        app_log.error(exceptionDetails)


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
    port = int(serverParams.get('ctrinport')) #31000
    bufferSize = int(serverParams.get('sortmessageserverbuffer'))
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

                if "KEEP_ALIVE" in decodedData and "ACK" not in decodedData: #and decodedData.startswith(GlobalConstants.StartTransmissionCharacter) and decodedData.endswith(GlobalConstants.EndTransmissionCharacter):
                    separatedMessages = multi_split(decodedData, [GlobalConstants.StartTransmissionCharacter, GlobalConstants.EndTransmissionCharacter])
                    for message in separatedMessages:
                        if is_json(message):
                            ackResponse = constructAckMessage(message)
                            conn.sendall(ackResponse)
                            print("Responded to Keep Alive.")
                            
                else:
                    #otherwise, assume it's arriving in chunks. Split the strings, loop through and save them
                    separatedMessages = multi_split(decodedData, [GlobalConstants.StartTransmissionCharacter, GlobalConstants.EndTransmissionCharacter])
                    for message in separatedMessages:
                        if is_json(message):
                            saveSortMessage(message)
                            print("CTRIN message saved")
               
                data = b''
                                 
            except socket.error:
                
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                exceptionDetails = ''.join('!! ' + line for line in lines)
                print(''.join('!! ' + line for line in lines))
                app_log.error(exceptionDetails)