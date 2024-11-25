"""
This module sets up and manages the database connection for the application.
It uses MySQL as the database engine and handles connection errors gracefully.
"""
import mysql.connector
from mysql.connector import errorcode

# Configure the database connection
config = {
    'user': 'root',
    'password': '0000',  # password
    'host': 'localhost',
    'port': '3306',
    'database': 'client_db'
}


def get_db():
    """
    Provides a database connection using the configured MySQL settings.
    The connection is yielded to the caller and closed automatically after use.

    Yields:
        MySQLConnection: A live connection to the MySQL database.

    Raises:
        mysql.connector.Error: If there is an issue with the connection.
    """
    try:
        db_connection = mysql.connector.connect(**config)
        yield db_connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        db_connection.close()
