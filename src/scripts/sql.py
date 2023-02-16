import sqlite3

def getAllRows():
    try:
        connection = sqlite3.connect('../db/mainDB.db')
        cursor = connection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * FROM Users WHERE username = 'admin'"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print(row)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print("The Sqlite connection is closed")

getAllRows()