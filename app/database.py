"""
Database connection utilities for the application.
"""
import mysql.connector
from mysql.connector import errorcode

# Configure the database connection
config = {
    'user': 'root',
    'password': '0000', #password
    'host': 'localhost',
    'port': '3306',
    'database': 'client_db'
}


def get_db():
    """
    Get a database connection instance.
    """
    try:
        db = mysql.connector.connect(**config)
        yield db
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        db.close()
