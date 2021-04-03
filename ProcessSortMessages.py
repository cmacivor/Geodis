import time
import schedule
import SQLServerConn
import MessageProcessor
import SortMessage
import datetime
import Logger
import traceback
import sys
import python_config
import logging
from logging.handlers import RotatingFileHandler

loggingConfig = python_config.read_logging_config()
logFileLocation = loggingConfig.get('batchjobfilelocation')

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = logFileLocation 

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)



def processSortMessagesIntoContainerMaster():
    unprocessedMessages = getUnprocessedMessages()
    for message in unprocessedMessages:
        sortMessageJson = message[1]
        convertedMessage = MessageProcessor.ConvertJsonToMessage(None, sortMessageJson)
        #test = convertedMessage
        content = convertedMessage.message
        sortMessageContent = SortMessage.SortMessageContent(content.status, content.lpId, content.orderId, content.shipId, content.wave, content.taskId, 
                                                            content.weight, content.width, content.length, content.height, content.containerType,
                                                            content.carrier, content.trackingNumber, content.route, content.SSCC, content.accountNumber, 
                                                            content.shipToPostalCode, content.shipToState, content.shipToCountry, content.shipDate, content.ASNHDRPASSTHRUCHAR19)
        

        saveToContainerMaster(sortMessageContent, convertedMessage.correlationId)
        #save to the container_master table

        #now need to update the SortMessage record - set IsProcessed = 1
        updateSortMessageRecordAsProcessed(message)



def updateSortMessageRecordAsProcessed(sortMessage):
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        currentTimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = "UPDATE dbo.SortMessages SET IsProcessed = 1, updated_at = ? WHERE Id = ?"

        cursor.execute(sql, currentTimeStamp, sortMessage.Id)

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


#TODO: add created_at, updated_at columns to container_master, rename "Carrrier" to "Carrier"
def saveToContainerMaster(sortMessage, correlationId):
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        currentTimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = '''IF NOT EXISTS (SELECT * FROM dbo.container_master WHERE LPID = ? AND CorrelationId = ?)
        INSERT INTO lego_outbound.dbo.container_master (LPID, CorrelationId, Status, OrderId, ShipId, Wave, TaskId, Weight, Width, Length, Height, ContainerType, Carrier, TrackingNumber, SSCC, AccountNumber,
                                                             ZipCode, State, Country, ShipDate, ASNHDRPASSTHRUCHAR19, LaneAssign, LaneActual, ReasonCode, ReasonDescription, IsAck, VerifyProcessed, CreatedAt, UpdatedAt)
                                                             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

        cursor.execute(sql, sortMessage.lpId, correlationId, sortMessage.lpId, correlationId, sortMessage.status, sortMessage.orderId, sortMessage.shipId, sortMessage.wave, sortMessage.taskId, sortMessage.weight, sortMessage.width, sortMessage.length, 
                            sortMessage.height, sortMessage.containerType, sortMessage.carrier, sortMessage.trackingNumber, sortMessage.SSCC, sortMessage.accountNumber, 
                            sortMessage.shipToPostalCode, sortMessage.shipToState, sortMessage.shipToCountry, sortMessage.shipDate, sortMessage.ASNHDRPASSTHRUCHAR19,
                            0, 0, 0, None, 0, 0, currentTimeStamp, currentTimeStamp)

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
    



def getUnprocessedMessages():
    # first get all SortMessages where IsProcessed is false
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        sql = "select * from dbo.SortMessages WHERE Type = 'CTRIN' and IsProcessed = 0"

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



# do it every x amount of  seconds
serverParams = python_config.read_server_config()
runInterval = int(serverParams.get('processsortmessageinterval'))
schedule.every(runInterval).seconds.do(processSortMessagesIntoContainerMaster)
#schedule checking and deleting of tables
while 1:
    print("processing sort messages..")
    schedule.run_pending()
    time.sleep(1)



