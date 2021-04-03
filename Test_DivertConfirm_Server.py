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

#End='something useable as an end marker'
Start=GlobalConstants.StartTransmissionCharacter
End=GlobalConstants.EndTransmissionCharacter
def recv_end(the_data):
    #this is always the size set in conn.recv
    size = len(the_data)

  
    if End in the_data:
        print('the end is in here')
    if Start in the_data:
        print('the start is in here')

    # total_data=[];data=''
    # while True:
    #         data= the_data #the_socket.recv(8192)
    #         if End in data:
    #             total_data.append(data[:data.find(End)])
    #             break
    #         total_data.append(data)
    #         if len(total_data)>1:
    #             #check if end_of_data was split
    #             last_pair=total_data[-2]+total_data[-1]
    #             if End in last_pair:
    #                 total_data[-2]=last_pair[:last_pair.find(End)]
    #                 total_data.pop()
    #                 break
    # return ''.join(total_data)




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    loggingConfig = python_config.read_logging_config()
    auth = loggingConfig.get('auth')
    domain = loggingConfig.get('domain')
    api = loggingConfig.get("api")
    url = domain + api

    serverParams = python_config.read_server_config()
    host = serverParams.get('host')
    #port = int(serverParams.get('port'))
    ctrinackport = int(serverParams.get('dvtcfport'))
    print('Listening on HOST: ' + str(host) + ' and PORT: ' + str(ctrinackport))


    s.bind((host, ctrinackport))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            try:

                data = conn.recv(8192)

                if not data:
                    break

                #recv_end(data.decode('ascii'))
                #print(allData)
                
                #print(' wrote ' + allData)
                printable = data.decode('ascii')
                print(' wrote ' + printable)
                
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