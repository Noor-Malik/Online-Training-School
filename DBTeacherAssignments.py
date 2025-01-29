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

class DBTeacherAssignments:
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

    def create(self, course_id, teacher_id, assignment_name, file_type, file_path, uploaded_at, status):
        sql = "INSERT INTO teacher_assignments (course_id, teacher_id, assignment_name, file_type, file_path, uploaded_at, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (course_id, teacher_id, assignment_name, file_type, file_path, uploaded_at, status)

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

            file_id = db_cursor.lastrowid
            print(f"Assignment record inserted with file_id: {file_id}")
            return {"file_id": file_id, "assignment_name": assignment_name, "file_type": file_type, "file_path": file_path, "status": status}

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

    def get_homework(self):
        sql = "SELECT file_id, assignment_name, file_type, file_path, status FROM teacher_assignments;"
        print(sql)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database.")
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql)
            homework = db_cursor.fetchall()

            if homework:
                logging.info("All homework retrieved successfully.")
                work_list = [
                    {
                        "file_id": work[0],
                        "assignment_name": work[1],
                        "file_type": work[2],
                        "file_path": work[3],
                        "state": work[4]
                    }
                    for work in homework
                ]
                return work_list
            else:
                logging.warning("No homework found in the database.")
                return []

        except Error as e:
            logging.error(f"Error retrieving all homework: {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def get_course_homework(self, course_id):
        sql = "SELECT file_id, assignment_name, file_type, status FROM teacher_assignments WHERE course_id = %s;"
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
                        "assignment_name": work[1],
                        "file_type": work[2],
                        "status": work[3],
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

    def get_student_homework(self, course_id):
        sql = "SELECT file_id, assignment_name, file_type, file_path FROM teacher_assignments WHERE course_id = %s AND status IN ('ACTIVE');"
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
                        "assignment_name": work[1],
                        "file_type": work[2],
                        "file_path": f"http://127.0.0.1:5000/download/{work[3].split('/')[-1]}"
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

    def assign_work(self, file_id):
        sql = "UPDATE teacher_assignments SET status = %s WHERE file_id= %s AND status = %s"
        new_status = ACTIVE
        current_status = OPEN
        val = (new_status, file_id, current_status)

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

            if db_cursor.rowcount == 0:
                logging.warning(f"No work found with file_id: {file_id} in OPEN status.")
                return False

            logging.info(f"Course with file_id {file_id} assigned successfully, status set to ACTIVE.")
            return True

        except Error as e:
            logging.error(f"Failed to assign work: {e}")
            if db_connection:
                db_connection.rollback()
            raise e

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

# dbTeacherAssignments = DBTeacherAssignments()
# course_record = dbTeacherAssignments.get_homework()
# print(course_record)