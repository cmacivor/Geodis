import socket
from time import sleep
import python_config
import GlobalConstants

    
def getSortMessageJson():
    sortMessageJson = ''' 
    {
        "sequenceNumber": "00003",
        "timeStamp": "2020-10-06T10:42:55",
        "messageName": "CTRIN",
        "correlationId": "473d41b6-f914-4f80-906d-1fe41250e598",
        "message": {
            "status": "N",
            "lpId": "090000078760455",
            "orderId": "121294578",
            "shipId": "1",
            "wave": "2525166",
            "taskId": "287159079",
            "weight": "2.25",
            "width": "14",
            "length": "12",
            "height": "7.25",
            "containerType": "LG2",
            "carrier": "FEDX",
            "trackingNumber": "",
            "manifestId": "",
            "route": "",
            "sscc": "00000000000379916117",
            "accountNumber": "",
            "shipToPostalCode": "80013",
            "shipToState": "CO",
            "shipToCountry": "US",
            "shipDate": "",
            "ASNHDRPASSTHRUCHAR19": "USAMZON" 
        }
    }'''

    return sortMessageJson

serverParams = python_config.read_server_config()
host = serverParams.get('host')
port = int(serverParams.get('ctrinport'))

HOST = host #'127.0.0.1'  # The server's hostname or IP address
PORT = port #65432        # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    testJson = '{"sequenceNumber":"2", "timeStamp": "2020-09-21T23:04:59", "messageName": "KEEP_ALIVE", "correlationId": "d9abc8ec-1253-4a1b-9230-6a085babd3bb", "status": "ACK" }'
    #testJson = getSortMessageJson()
    concatMessage = GlobalConstants.StartTransmissionCharacter + testJson + GlobalConstants.EndTransmissionCharacter
    encodedMessage = concatMessage.encode('ascii')

    s.connect((HOST, PORT))

    while True:
        data = s.recv(1024)
        print(data)
        #sleep(15)
        s.sendall(encodedMessage)