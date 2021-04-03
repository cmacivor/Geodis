import python_config
import SQLServerConn
import datetime

def log(source, messageType, message):
    try:
        conn = SQLServerConn.get()

        cursor = conn.cursor()

        #sql = "select top 1 * from dbo.container_master WHERE IsAck = 0 order by Id"
        currentTimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = 'INSERT INTO lego_outbound.dbo.Logs (Source, Type, Message, CreatedAt, UpdatedAt) VALUES (?, ?, ?, ?, ?)'

        cursor.execute(sql, source, messageType, message, currentTimeStamp, currentTimeStamp)

        conn.commit()

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        print(e)
