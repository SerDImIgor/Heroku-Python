import sqlite3
import sys 
import io

class DB:
    def __init__(self,app):
        self.app = app

    def create_table(self):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS new_employee 
            ( id INTEGER NOT NULL, name TEXT NOT NULL, photo BLOB NOT NULL);'''

            cursor = sqliteConnection.cursor()
            self.app.logger.info("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            self.app.logger.info("SQLite table created")

            cursor.close()

        except sqlite3.Error as error:
            self.app.logger.error("Error while creating a sqlite table {}".format(error))
            return 0
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                self.app.logger.info("sqlite connection is closed")
                return 1
    

    def readBlobData(self,empId):
        result_photo = None
        name_file = None
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = sqliteConnection.cursor()
            self.app.logger.info("Connected to SQLite")

            sql_fetch_blob_query = """SELECT * from new_employee where id = ?"""
            cursor.execute(sql_fetch_blob_query, (empId,))
            record = cursor.fetchall()
            for row in record:
                self.app.logger.info("Id = ", row[0], "Name = ", row[1])
                name = row[1]
                photo = row[2]
                result_photo = photo
                name_file = name
                print("Storing employee image and resume on disk \n")
                self.app.logger.info("Storing employee image and resume on disk \n")
            cursor.close()
        except sqlite3.Error as error:
            self.app.logger.error("Failed to read blob data from sqlite table {} ".format(error))
            print("Failed to read blob data from sqlite table {} ".format(error))
            return None
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                self.app.logger.info("sqlite connection is closed")
                print("sqlite connection is closed OK")
                return name_file

    def insertBLOB(self,empId, name, empPhoto):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = sqliteConnection.cursor()
            self.app.logger.info("Connected to SQLite")
            sqlite_insert_blob_query = """ INSERT INTO new_employee
                                          (id, name, photo) VALUES (?, ?, ?)"""


            # Convert data into tuple format
            #io.BytesIO(empPhoto)
            data_tuple = (empId, name,empPhoto)
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            sqliteConnection.commit()
            self.app.logger.info("Image and file inserted successfully as a BLOB into a table")
            print("Image and file inserted successfully as a BLOB into a table")
            cursor.close()
            return 1
        except sqlite3.Error as error:
            self.app.logger.error("Failed to insert blob data into sqlite table {}".format(error))
            print("Failed to insert blob data into sqlite table {}".format(error))
            return 0
        except Exception as e:
            exception_name, exception_value, _ = sys.exc_info()
            print("Failed to insert blob data into sqlite table {} {} {}".format(exception_name,exception_value,e))

        finally:
            if sqliteConnection:
                sqliteConnection.close()
                self.app.logger.info("the sqlite connection is closed")
                print('the sqlite connection is closed')
                return 0
    
    def deleteBLOB(self,empId):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            #sqliteConnection.execute("VACUUM")
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            sqlite_insert_blob_query = "DELETE FROM new_employee WHERE id={};".format(empId)
            print(sqlite_insert_blob_query)
            cursor.execute(sqlite_insert_blob_query)
            sqliteConnection.commit()
            print("Image and file DELETE successfully as a BLOB into a table")
            cursor.close()
            sqliteConnection.execute("vacuum")

        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("the sqlite connection is closed")