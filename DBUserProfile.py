import mysql.connector
import logging
from mysql.connector import Error
from OTExceptions import DuplicateProfileException

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Ainnie123$"
DB_NAME = "register_db"

class DBUserProfile:
    def __init__(self):
        self.db_connection = None

    def get_connection(self):
        try:
            self.db_connection = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,database=DB_NAME)
            if self.db_connection.is_connected():
                print("Connected to the database.")
        except Error as e:
            print(f"Error connecting to database: {e}")
            logging.exception("Error connecting to database")
        return self.db_connection

    def insert_profile(self, user_id, name, age, address, phone_number):
        sql = "INSERT INTO userprofile(userId, name, age, address, phoneNumber) VALUES (%s, %s, %s, %s, %s)"
        val = (user_id, name, age, address, phone_number)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Database connection could not be established.")
                return None

            db_cursor = db_connection.cursor()
            logging.debug(f"Checking for existing profile with userId: {user_id}")
            existing_profile_check_sql = "SELECT 1 FROM userprofile WHERE userId = %s"
            db_cursor.execute(existing_profile_check_sql, (user_id,))
            existing_profile = db_cursor.fetchone()

            if existing_profile:
                logging.warning(f"Profile with userId {user_id} already exists.")
                raise DuplicateProfileException("Profile already exists.")

            logging.debug("Inserting new profile.")
            print(f"Executing SQL: {sql}")
            print(f"SQL Parameters: {val}")
            db_cursor.execute(sql, val)
            db_connection.commit()

            db_cursor.execute("SELECT LAST_INSERT_ID()")
            result = db_cursor.fetchone()

            if result:
                return {"userprofileId": result[0]}
            else:
                raise Exception("Failed to create user profile")

        except DuplicateProfileException as e:
            logging.error(f"Duplicate profile detected for userId: {user_id}: {e}")
            raise e
        except Error as e:
            logging.error(f"Error inserting profile: {e}")
            if db_connection:
                db_connection.rollback()
            raise e

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
                logging.info("Database connection closed.")

    def update_profile(self, user_id, name, age, address, phone_number, userprofileId):
        sql = "UPDATE userprofile SET name = %s, age = %s, address = %s, phoneNumber = %s WHERE userprofileId = %s AND userId = %s"
        val = (name, age, address, phone_number, userprofileId, user_id)
        print(f"DBUserProfile: Preparing to execute SQL update for user_id {user_id}")

        logging.debug(f"SQL Statement: {sql}")
        logging.debug(f"Values: {val}")

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                print("DBUserProfile: Database connection could not be established.")
                logging.error("Database connection could not be established.")
                return None

            db_cursor = db_connection.cursor()
            print(f"DBUserProfile: Executing update for userId {user_id}")
            logging.debug(f"Executing update for userId {user_id}")
            db_cursor.execute(sql, val)
            db_connection.commit()

            if db_cursor.rowcount == 0:
                print(f"DBUserProfile: No profile found for userId {user_id}; update may have failed.")
                logging.warning(f"No profile found for userId {user_id}; update may have failed.")
                return False
            else:
                print(f"DBUserProfile: Profile updated successfully for userId: {user_id}")
                logging.info(f"Profile updated successfully for userId: {user_id}")
                return True

        except Error as e:
            print(f"DBUserProfile: Failed to update user profile for userId {user_id}: {e}")
            logging.error(f"Failed to update user profile for userId {user_id}: {e}")
            if db_connection:
                db_connection.rollback()
                print("DBUserProfile: Transaction rolled back due to error.")
                logging.info("Transaction rolled back due to error.")
            return False

        finally:
            if db_cursor:
                db_cursor.close()
                print("DBUserProfile: Database cursor closed.")
            if db_connection and db_connection.is_connected():
                db_connection.close()
                print("DBUserProfile: Database connection closed.")
                logging.info("Database connection closed.")


#create_profile test
# dbUserProfile = DBUserProfile()
# course_record = dbUserProfile.insert_profile(174, "noor", 35, "lahore", "3259654445")
# print(course_record)

#update_profile test
# dbUserProfile = DBUserProfile()
# course_record = dbUserProfile.update_profile(177, "Huzgha", 39, "lahori", "325968045", 11)
# print(course_record)