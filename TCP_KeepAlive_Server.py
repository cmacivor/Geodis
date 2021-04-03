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
import uuid
import datetime
import subprocess


def constructKeepAliveMessage(counter):
 
    currentTimeStamp =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    correlationId = str(uuid.uuid4())

    keepAlive = KeepAliveMessage.KeepAlive(counter, currentTimeStamp, correlationId)
    
    keepAliveJSON = MessageProcessor.ConvertMessageToJson(None, keepAlive)

    concatMessage = GlobalConstants.StartTransmissionCharacter + keepAliveJSON + GlobalConstants.EndTransmissionCharacter

    encodedMessage = concatMessage.encode('ascii')

    return encodedMessage


#start the other process
#p = subprocess.Popen(['python', 'TCP_SortMessage_Receiver.py'])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    loggingConfig = python_config.read_logging_config()
    auth = loggingConfig.get('auth')
    domain = loggingConfig.get('domain')
    api = loggingConfig.get("api")
    url = domain + api

    serverParams = python_config.read_server_config()
    host = serverParams.get('host')
    port = int(serverParams.get('ctrinport'))
    print('Listening on HOST: ' + str(host) + ' and PORT: ' + str(port))

    reconnectionAttempts = 0  
    reconnAttemptLimit = int(serverParams.get('reconnattemptlimit'))
    sequenceCounter = 0
    keepAliveInterval = int(serverParams.get('keepaliveinterval'))


    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            try:

                #data = conn.recv(1024)

                # if not data:
                #     break

                sequenceCounter = sequenceCounter + 1
                keepAlive = constructKeepAliveMessage(sequenceCounter)
                conn.sendall(keepAlive)

                #get back the response
                response = conn.recv(1024)
                print(response)

                time.sleep(keepAliveInterval)

            except socket.error:
                #print(e)
                #set connection status and recreate socket
                sequenceCounter = 0
                connected = False

                #clientSocket = socket.socket()
                print("connection lost...reconnecting")
                while not connected:
                    if reconnectionAttempts == reconnAttemptLimit:
                        print("reconnection limit reached...exiting...")
                        #p.terminate()
                        quit()
                    else: 
                        reconnectionAttempts = reconnectionAttempts + 1
                        print('reconnection attempt number: ' + str(reconnectionAttempts))
                        # attempt to reconnect, otherwise sleep for 2 seconds
                        try:
                            #clientSocket.connect((host, port))
                            s.bind((host, port))
                            s.listen()
                            conn, addr = s.accept()
                            connected = True
                            print("re-connection successful")
                        except socket.error:
                            time.sleep(10) # this is the pause between reconnection attempt


                # print(sys.exc_info()[0])
                # print(traceback.format_exc())
                # print("press enter to continue...")
                # input()