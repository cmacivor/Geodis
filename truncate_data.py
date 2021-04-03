
import SQLServerConn

def truncateContainerMaster():
    try:
        conn = SQLServerConn.get()
        cursor = conn.cursor()
        sql = "DELETE FROM container_master WHERE UpdatedAt < (getdate() - 14)"
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close() 

    except Exception as e:
        print(e)

truncateContainerMaster()
