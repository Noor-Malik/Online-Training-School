import mysql.connector
import logging
from mysql.connector import Error
from OTExceptions import DuplicateRecordException, InvalidCredentialsException

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Ainnie123$"
DB_NAME = "register_db"

class DBUser:
    def __init__(self):
        self.db_connection = None

    def get_Connection(self):
        try:
            self.db_connection = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            if self.db_connection.is_connected():
                print("Connected to the database.")
        except Error as e:
            print(f"Error connecting to database: {e}")
            logging.exception("Error connecting to database")
        return self.db_connection

    def create(self, email, password, userType, securityQuestion, passwordHint):
        sql = "INSERT INTO user (email, password, userType, securityQuestion, passwordHint) VALUES (%s, %s, %s, %s,%s)"
        val = (email, password, userType, securityQuestion, passwordHint)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_Connection()
            if db_connection is None:
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            db_connection.commit()

            userId = db_cursor.lastrowid
            print(f"User record inserted with userId: {userId}")
            return userId

        except Error as e:
            print(f"Failed to insert user: {e}")
            if e.errno == 1062:
                logging.log(1,"Duplicate record found in user table")
                raise DuplicateRecordException(9000, "Duplicate record found in user table")
            return None
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def delete(self, email):
        sql = "DELETE FROM user WHERE email = %s"
        val = email

        db_connection = None
        db_cursor = None
        try:
            db_connection = self.get_Connection()
            if db_connection is None:
                return

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            db_connection.commit()
            print(f"{db_cursor.rowcount} record deleted.")
            logging.info(f"User {email} successfully deleted")
        except Error as e:
            print(f"Failed to delete user: {e}")
            logging.error(f"Failed to delete user {email}: {e}")
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
                logging.info("Database connection closed")

    def updatePassword(self, email, userType, newPassword):
        sql = "UPDATE user SET password = %s WHERE email = %s AND userType = %s"
        val = (newPassword, email, userType)

        db_connection = None
        db_cursor = None
        try:
            db_connection = self.get_Connection()
            if db_connection is None:
                return

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            db_connection.commit()

            print(f"{db_cursor.rowcount} password changed updated.")
            logging.info(f"Password updated for user {email}")
        except Error as e:
            print(f"Failed to update user: {e}")
            logging.error(f"Failed to update user {email}: {e}")
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
                logging.info("Database connection closed")

    def select_login(self, email, password, userType):
        sql = "SELECT * FROM user WHERE email = %s AND password =%s AND userType = %s"
        val = (email, password, userType)

        print(sql)
        print(val)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_Connection()
            if db_connection is None:
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            result = db_cursor.fetchone()

            if result:
                print(f"User found: {result}")
                logging.info(f"User {email} found in the database")
                return result
            else:
                logging.warning(f"No user found with email {email} and the provided credentials.")
                raise InvalidCredentialsException(9001, "No user found with the given credentials.")

        except Error as e:
            print(f"Failed to retrieve user: {e}")
            logging.error(f"Failed to retrieve user {email}: {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
                logging.info("Database connection closed")

    def select_hint(self, email, userType, securityQuestion, passwordHint):
        sql = "SELECT * FROM user WHERE email = %s AND userType = %s AND securityQuestion = %s AND passwordHint = %s"
        val = (email, userType, securityQuestion, passwordHint)

        print(f"Executing SQL: {sql}")
        print(f"Values: {val}")

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_Connection()
            if db_connection is None:
                logging.error("Database connection failed")
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            result = db_cursor.fetchone()

            if result:
                print(f"User found: {result}")
                logging.info(f"User {email} found in the database")
                return result
            else:
                logging.warning(f"No user found with email {email} and the provided credentials.")
                raise InvalidCredentialsException(9001, "No user found with the given credentials.")

        except Exception as e:
            print(f"Failed to retrieve user: {e}")
            logging.error(f"Failed to retrieve user {email}: {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
                logging.info("Database connection closed")