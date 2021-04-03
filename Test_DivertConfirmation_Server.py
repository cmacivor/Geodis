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

                data = conn.recv(4096)

                if not data:
                    break

                printable = data.decode('ascii')
                print(' wrote ' + printable)
                
                #conn.sendall(data)
                time.sleep(5)
                #print('response: ' + response.decode('ascii'))
                #conn.sendall(response)

            except Exception as e:
                if isinstance(e, ConnectionResetError):
                    pass
                print(sys.exc_info()[0])
                print(traceback.format_exc())
                print("press enter to continue...")
                input()