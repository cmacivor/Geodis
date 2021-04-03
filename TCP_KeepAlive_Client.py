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



serverParams = python_config.read_server_config()
host = serverParams.get('remotehost')
ctrinackport = serverParams.get('ctrinackport')

HOST = host #'127.0.0.1'  # The server's hostname or IP address
PORT = int(ctrinackport)  #65432  # The port used by the server


clientSocket = socket.socket()
clientSocket.connect((HOST, PORT))

connected = True
print("connected to server")

reconnectionAttempts = 0  
reconnAttemptLimit = int(serverParams.get('reconnattemptlimit'))
sequenceCounter = 0
keepAliveInterval = int(serverParams.get('keepaliveinterval'))

while True:
    try:
        sequenceCounter = sequenceCounter + 1
        keepAlive = constructKeepAliveMessage(sequenceCounter)
        clientSocket.sendall(keepAlive)

        #get back the response
        response = clientSocket.recv(1024)
        print(response)

        time.sleep(keepAliveInterval)

    except socket.error:
        #set connection status and recreate socket
        sequenceCounter = 0
        connected = False
        clientSocket = socket.socket()
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
                    clientSocket.connect((HOST, PORT))
                    connected = True
                    print("re-connection successful")
                except socket.error:
                    time.sleep(2) # this is the pause between reconnection attempt
              
