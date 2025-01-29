import mysql.connector
import logging
from mysql.connector import Error
from OTExceptions import CourseNotFoundException, EnrollmentException

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Ainnie123$"
DB_NAME = "register_db"

class DBCourseEnrollment:
    def __init__(self):
        self.db_connection = None

    def get_connection(self):
        try:
            self.db_connection = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            if self.db_connection.is_connected():
                logging.info("Connected to the database.")
                print("Connected to the database.")
                return self.db_connection
        except Error as e:
            logging.exception("Error connecting to database")
            print("Error connecting to database:", e)
            return None

    def get_course_status(self, course_id):
        db_connection = None
        db_cursor = None
        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database")
                return None

            db_cursor = db_connection.cursor()
            sql = "SELECT state FROM course WHERE course_id = %s"
            val = course_id,

            print(sql)
            print(val)

            db_cursor.execute(sql, val)
            result = db_cursor.fetchone()

            print(result)

            if result:
                logging.info(f"Course ID {course_id} status retrieved: {result[0]}")
                print(result[0])
                return result[0]
            else:
                logging.warning(f"No course found with ID {course_id}")
                raise CourseNotFoundException("Course not found.")

        except Error as e:
            logging.exception("Error retrieving course status")
            return None
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
                logging.info("Database connection closed.")

    def select_course(self, course_id):
        db_connection = None
        db_cursor = None
        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database")
                print("Failed to connect to the database.")
                return None

            db_cursor = db_connection.cursor()
            sql = "SELECT * FROM course WHERE course_id = %s"
            val = course_id

            db_cursor.execute(sql, val)
            result = db_cursor.fetchone()

            if result:
                logging.info(f"Course details for course_id {course_id} retrieved.")
                print(f"Course details retrieved: {result}")
                return result
            else:
                logging.warning(f"No course found with ID {course_id}")
                print(f"No course found with ID {course_id}")
                raise CourseNotFoundException("Course not found.")

        except Error as e:
            logging.exception("Error retrieving course details")
            print("Error retrieving course details:", e)
            return None
        finally:
            if db_cursor:
                db_cursor.close()
                logging.info("Database cursor closed.")
                print("Database cursor closed.")
            if db_connection and db_connection.is_connected():
                db_connection.close()
                logging.info("Database connection closed.")
                print("Database connection closed.")

    def enroll_student(self, course_id, student_id):
        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                raise EnrollmentException("Database connection failed")

            db_cursor = db_connection.cursor()
            db_cursor.execute("SELECT available_seats FROM course WHERE course_id = %s", (course_id,))
            result = db_cursor.fetchone()

            if result and result[0] > 0:
                sql_enroll = "INSERT INTO course_enrollment (course_id, student_id, enrollment_date) VALUES (%s, %s, NOW())"
                val_enroll = (course_id, student_id,)
                print(sql_enroll)
                print(val_enroll)
                db_cursor.execute(sql_enroll, val_enroll)

                sql_update_seats = "UPDATE course SET available_seats = available_seats - 1 WHERE course_id = %s AND available_seats > 0"
                val_update_seats = (course_id,)
                print(sql_update_seats)
                print(val_update_seats)
                db_cursor.execute(sql_update_seats, val_update_seats)
                db_connection.commit()

                logging.info(f"Student {student_id} successfully enrolled in course {course_id}.")
                return True
            else:
                logging.warning(f"No available seats for course {course_id}.")
                return False

        except Error as e:
            logging.error(f"Failed to enroll student {student_id} in course {course_id}: {e}")
            if db_connection:
                db_connection.rollback()
            return False

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def cancel_enrollment(self, course_id, student_id):
        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                raise EnrollmentException("Database connection failed")

            db_cursor = db_connection.cursor()
            sql_cancel = "DELETE FROM course_enrollment WHERE course_id = %s AND student_id = %s"
            val_cancel = (course_id, student_id)
            print(sql_cancel)
            print(val_cancel)
            db_cursor.execute(sql_cancel, val_cancel)

            if db_cursor.rowcount > 0:
                sql_update_seats = "UPDATE course SET available_seats = available_seats + 1 WHERE course_id = %s"
                val_update_seats = (course_id,)
                print(sql_update_seats)
                print(val_update_seats)
                db_cursor.execute(sql_update_seats, val_update_seats)
                db_connection.commit()

                logging.info(f"Enrollment request for student {student_id} in course {course_id} canceled.")
                return True
            else:
                logging.warning(f"No enrollment found to cancel for student {student_id} in course {course_id}.")
                return False

        except Error as e:
            logging.error(f"Failed to cancel enrollment for student {student_id} in course {course_id}: {e}")
            if db_connection:
                db_connection.rollback()
            return False

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

