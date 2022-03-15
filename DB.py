import sqlite3
class DB:
    def __init__(self,app):
        self.app = app

    def create_table(self):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS new_employee 
            ( id INTEGER PRIMARY KEY, name TEXT NOT NULL, photo BLOB NOT NULL);'''

            cursor = sqliteConnection.cursor()
            self.app.logger.info("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            self.app.logger.info("SQLite table created")

            cursor.close()
            return 1

        except sqlite3.Error as error:
            self.app.logger.error("Error while creating a sqlite table {}".format(error))
            return 0
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                self.app.logger.info("sqlite connection is closed")
            return 0
    

    def readBlobData(self,empId):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = sqliteConnection.cursor()
            self.app.logger.info("Connected to SQLite")

            sql_fetch_blob_query = """SELECT * from new_employee where id = ?"""
            cursor.execute(sql_fetch_blob_query, (empId,))
            record = cursor.fetchall()
            result_photo = None
            for row in record:
                self.app.logger.info("Id = ", row[0], "Name = ", row[1])
                name = row[1]
                photo = row[2]
                result_photo = photo 
                self.app.logger.info("Storing employee image and resume on disk \n")
            cursor.close()
            return result_photo
        except sqlite3.Error as error:
            self.app.logger.error("Failed to read blob data from sqlite table {} ".format(error))
            return None
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                self.app.logger.info(("sqlite connection is closed")
            return None

    def insertBLOB(self,empId, name, empPhoto):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = sqliteConnection.cursor()
            self.app.logger.info("Connected to SQLite")
            sqlite_insert_blob_query = """ INSERT INTO new_employee
                                          (id, name, photo) VALUES (?, ?, ?)"""


            # Convert data into tuple format
            data_tuple = (empId, name, empPhoto)
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            sqliteConnection.commit()
            self.app.logger.info("Image and file inserted successfully as a BLOB into a table")
            cursor.close()
            return 1
        except sqlite3.Error as error:
            self.app.logger.error("Failed to insert blob data into sqlite table {}".format(error))
            return 0
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                self.app.logger.info("the sqlite connection is closed")
                return 0