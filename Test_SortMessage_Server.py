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
import uuid

def constructKeepAliveMessage(counter):
 
    currentTimeStamp =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    correlationId = str(uuid.uuid4())

    keepAlive = KeepAliveMessage.KeepAlive(counter, currentTimeStamp, correlationId)
    
    keepAliveJSON = MessageProcessor.ConvertMessageToJson(None, keepAlive)

    concatMessage = GlobalConstants.StartTransmissionCharacter + keepAliveJSON + GlobalConstants.EndTransmissionCharacter

    encodedMessage = concatMessage.encode('ascii')

    return encodedMessage



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    loggingConfig = python_config.read_logging_config()
    auth = loggingConfig.get('auth')
    domain = loggingConfig.get('domain')
    api = loggingConfig.get("api")
    url = domain + api

    serverParams = python_config.read_server_config()
    host = serverParams.get('host')
    #port = int(serverParams.get('port'))
    ctrinackport = int(serverParams.get('ctrinackport'))
    print('Listening on HOST: ' + str(host) + ' and PORT: ' + str(ctrinackport))


    s.bind((host, ctrinackport))
    s.listen()
    conn, addr = s.accept()
    counter = 0
    with conn:
        print("Connected by", addr)
        while True:
            try:
                counter = counter + 1
                data = conn.recv(4096)

                if not data:
                    break

                printable = data.decode('ascii')
                print(' wrote ' + printable)

                response = constructKeepAliveMessage(counter)
                
                #conn.sendall(data)
                #time.sleep(5)
                #print('response: ' + response.decode('ascii'))
                #conn.sendall(response)

            except Exception as e:
                if isinstance(e, ConnectionResetError):
                    pass
                print(sys.exc_info()[0])
                print(traceback.format_exc())
                print("press enter to continue...")
                input()