import mysql.connector
import logging
from mysql.connector import Error
from OTExceptions import DuplicateAssignmentException

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Ainnie123$"
DB_NAME = "register_db"
OPEN = "OPEN"
ACTIVE = "ACTIVE"

class DBStudentHomework:
    def __init__(self):
        self.db_connection = None

    def get_connection(self):
        try:
            self.db_connection = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,database=DB_NAME)
            if self.db_connection.is_connected():
                logging.info("Connected to the database.")
                return self.db_connection
        except Error as e:
            logging.exception(f"Error {e} connecting to database")
            return None

    def submit_homework(self, course_id, file_id, student_id, homework_name, file_type, file_path, submitted_at, status):
        sql = "INSERT INTO student_homework (course_id, file_id, student_id, homework_name, file_type, file_path, submitted_at, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (course_id, file_id, student_id, homework_name, file_type, file_path, submitted_at, status)

        print(sql)
        print(val)
        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                raise Exception("Database connection failed")

            db_cursor = db_connection.cursor()
            print(f"Executing SQL: {sql}")
            print(f"SQL Parameters: {val}")
            db_cursor.execute(sql, val)
            db_connection.commit()

            homework_id = db_cursor.lastrowid
            print(f"Assignment record inserted with homework_id: {homework_id}")
            return {"homework_id": homework_id, "homework_name": homework_name, "file_type": file_type, "file_path": file_path, "status": status}

        except Error as e:
            if e.errno == 1062:
                logging.warning(f"Duplicate assignment entry detected: {e}")
                raise DuplicateAssignmentException("Assignment with this name already exists.")
            else:
                logging.error(f"Failed to insert assignment: {e}")
                raise e

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def get_course_homework(self, course_id):
        sql = "SELECT file_id, homework_name, file_type, file_path FROM teacher_assignments WHERE course_id = %s AND status IN ('ACTIVE');"
        val = (course_id,)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database.")
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            homework = db_cursor.fetchall()

            if homework:
                logging.info(f"Homework found for teacher_id {course_id}: {homework}")
                work_list = [
                    {
                        "file_id": work[0],
                        "homework_name": work[1],
                        "file_type": work[2],
                        "file_path": work[3],
                    }
                    for work in homework
                ]
                return work_list
            else:
                logging.warning(f"No courses found for teacher_id: {course_id}")
                return []

        except Error as e:
            logging.error(f"Error retrieving courses for user_id {course_id}: {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()