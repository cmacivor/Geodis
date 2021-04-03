import pyodbc
import python_config

def get():
    dbConfig = python_config.read_db_config()
    servername = dbConfig.get('host')
    username = dbConfig.get('user')
    password = dbConfig.get('password')

    conn = pyodbc.connect('Driver={SQL Server};'
                'Server=' + servername + ';'
                'Database=lego_outbound;'
                'UID=' + username + ';'
                'PWD=' + password + ';' )
    
    return conn
    
