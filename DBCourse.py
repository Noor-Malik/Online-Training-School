import mysql.connector
import logging
from mysql.connector import Error
from OTExceptions import DuplicateCourseException, CourseNotFoundException

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Ainnie123$"
DB_NAME = "register_db"
PENDING_FOR_APPROVAL = "PENDING FOR APPROVAL"
OPEN = "OPEN"
ACTIVE = "ACTIVE"
COMPLETED = "COMPLETED"
CANCELLED = "CANCELLED"
REJECTED = "REJECTED"
ADMIN = "ADMIN"
TEACHER = "TEACHER"
STUDENT = "STUDENT"

class DBCourse:
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

    def get_status(self, course_id):
        db_connection = None
        db_cursor = None
        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database")
                return None

            db_cursor = db_connection.cursor()
            query = "SELECT state FROM course WHERE course_id = %s"
            db_cursor.execute(query, (course_id,))
            result = db_cursor.fetchone()

            if result:
                print(result)
                course_status = result[0]
                logging.info(f"Course ID {course_id} status retrieved: {course_status}")
                return course_status
            else:
                logging.warning(f"No course found with ID {course_id}")
                return None

        except Error as e:
            logging.exception(f"Error {e} retrieving course status")
            return None
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
                logging.info("Database connection closed.")

    def get_all_courses(self):
        sql = "SELECT course_id, course_name, course_details, duration, start_date, end_date, available_seats, state, user_id FROM course;"

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database.")
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql)
            courses = db_cursor.fetchall()

            if courses:
                logging.info("All courses retrieved successfully.")
                course_list = [
                    {
                        "course_id": course[0],
                        "course_name": course[1],
                        "course_details": course[2],
                        "duration": course[3],
                        "start_date": course[4].strftime("%d-%m-%y") if course[4] else None,
                        "end_date": course[5].strftime("%d-%m-%y") if course[5] else None,
                        "available_seats": course[6],
                        "state": course[7],
                        "user_id": course[8],
                    }
                    for course in courses
                ]
                return course_list
            else:
                logging.warning("No courses found in the database.")
                return []

        except Error as e:
            logging.error(f"Error retrieving all courses: {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def get_courses_by_state(self, user_id, state):
        sql = "SELECT course_id, course_name, course_details, duration, start_date, end_date, available_seats, state, user_id FROM course WHERE user_id = %s AND state = %s;"
        val = (user_id, state,)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database.")
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            courses = db_cursor.fetchall()

            if courses:
                logging.info(f"Courses with state '{state}' retrieved successfully for user_id {user_id}")
                course_list = [
                    {
                        "course_id": course[0],
                        "course_name": course[1],
                        "course_details": course[2],
                        "duration": course[3],
                        "start_date": course[4].strftime("%d-%m-%y") if course[4] else None,
                        "end_date": course[5].strftime("%d-%m-%y") if course[5] else None,
                        "available_seats": course[6],
                        "state": course[7],
                        "user_id": course[8],
                    }
                    for course in courses
                ]
                print(course_list)
                return course_list
            else:
                logging.warning(f"No courses found with state '{state}' for user_id {user_id}")
                return []

        except Error as e:
            logging.error(f"Error retrieving courses with state '{state}' for user_id {user_id}: {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def filtered_courses(self, course_name=None, start_date=None, end_date=None, state=None):
        filters = []
        values = []

        filters.append("state IN ('OPEN', 'ACTIVE')")

        if course_name:
            filters.append("course_name LIKE %s")
            values.append(f"%{course_name}%")
        if start_date:
            filters.append("start_date = %s")
            values.append(start_date)
        if end_date:
            filters.append("end_date = %s")
            values.append(end_date)
        if state:
            filters.append("state = %s")
            values.append(state)

        sql = f"SELECT course_id, course_name, course_details, duration, start_date, end_date, available_seats, state, user_id FROM course WHERE {" AND ".join(filters)};"
        print(sql)
        print(values)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database.")
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, values)
            courses = db_cursor.fetchall()
            print(courses)

            if courses:
                logging.info(f"Courses retrieved successfully for user.")
                course_list = [
                    {
                        "course_id": course[0],
                        "course_name": course[1],
                        "course_details": course[2],
                        "duration": course[3],
                        "start_date": course[4].strftime("%d-%m-%y") if course[4] else None,
                        "end_date": course[5].strftime("%d-%m-%y") if course[5] else None,
                        "available_seats": course[6],
                        "state": course[7],
                        "user_id": course[8],
                    }
                    for course in courses
                ]
                print(course_list)
                return course_list
            else:
                logging.warning(f"No courses found for user_id.")
                return []

        except Error as e:
            logging.error(f"Error retrieving courses for user to show. {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection:
                db_connection.close()

    def admin_filters(self, course_name=None, start_date=None, end_date=None, state=None):
        filters = []
        values = []

        if course_name:
            filters.append("course_name LIKE %s")
            values.append(f"%{course_name}%")
        if start_date:
            filters.append("start_date = %s")
            values.append(start_date)
        if end_date:
            filters.append("end_date = %s")
            values.append(end_date)
        if state:
            filters.append("state = %s")
            values.append(state)

        sql = f"SELECT course_id, course_name, course_details, duration, start_date, end_date, available_seats, state, user_id FROM course WHERE {" AND ".join(filters)};"
        print(sql)
        print(values)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database.")
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, values)
            courses = db_cursor.fetchall()
            print(courses)

            if courses:
                logging.info(f"Courses retrieved successfully for user.")
                course_list = [
                    {
                        "course_id": course[0],
                        "course_name": course[1],
                        "course_details": course[2],
                        "duration": course[3],
                        "start_date": course[4].strftime("%d-%m-%y") if course[4] else None,
                        "end_date": course[5].strftime("%d-%m-%y") if course[5] else None,
                        "available_seats": course[6],
                        "state": course[7],
                        "user_id": course[8],
                    }
                    for course in courses
                ]
                print(course_list)
                return course_list
            else:
                logging.warning(f"No courses found for user_id.")
                return []

        except Error as e:
            logging.error(f"Error retrieving courses for user to show. {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection:
                db_connection.close()

    def filter_courses(self, user_id, course_name=None, start_date=None, end_date=None, state=None):
        filters = ["user_id = %s"]
        values = [user_id]

        if course_name:
            filters.append("course_name LIKE %s")
            values.append(f"%{course_name}%")
        if start_date:
            filters.append("start_date = %s")
            values.append(start_date)
        if end_date:
            filters.append("end_date = %s")
            values.append(end_date)
        if state:
            filters.append("state = %s")
            values.append(state)

        sql = f"SELECT course_id, course_name, course_details, duration, start_date, end_date, available_seats, state, user_id FROM course WHERE {" AND ".join(filters)};"
        print(sql)
        print(values)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database.")
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, values)
            courses = db_cursor.fetchall()
            print(courses)

            if courses:
                logging.info(f"Courses retrieved successfully for user_id {user_id}")
                course_list = [
                    {
                        "course_id": course[0],
                        "course_name": course[1],
                        "course_details": course[2],
                        "duration": course[3],
                        "start_date": course[4].strftime("%d-%m-%y") if course[4] else None,
                        "end_date": course[5].strftime("%d-%m-%y") if course[5] else None,
                        "available_seats": course[6],
                        "state": course[7],
                        "user_id": course[8],
                    }
                    for course in courses
                ]
                print(course_list)
                return course_list
            else:
                logging.warning(f"No courses found for user_id {user_id}")
                return []

        except Error as e:
            logging.error(f"Error retrieving courses for user_id {user_id}: {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection:
                db_connection.close()

    def exists(self, course_name, teacher_id):
        sql = "SELECT 1 FROM course WHERE course_name = %s AND user_id = %s"
        val = (course_name, teacher_id,)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                return False

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            result = db_cursor.fetchone()

            if result:
                return True
            else:
                return False

        except Error as e:
            logging.error(f"Failed to check if course exists: {e}")
            return False
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def create(self, course_name, course_details, duration, start_date, end_date, available_seats, state, user_id):
        sql = "INSERT INTO course (course_name, course_details, duration, start_date, end_date, available_seats, state, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (course_name, course_details, duration, start_date, end_date, available_seats, state, user_id)

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

            course_id = db_cursor.lastrowid
            print(f"User record inserted with userId: {course_id}")
            return {"course_id": course_id, "course_name": course_name, "state":state}

        except Error as e:
            if e.errno == 1062:
                logging.warning(f"Duplicate course entry detected: {e}")
                raise DuplicateCourseException("A course with this name already exists.")
            else:
                logging.error(f"Failed to insert course: {e}")
                raise e

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def get_course(self, course_id):
        sql = "SELECT * FROM course WHERE course_id = %s"
        val = (course_id,)
        print(course_id)

        course = None
        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            course = db_cursor.fetchone()


            if course:
                logging.info(f"Course found: {course}")
                return course
            else:
                logging.warning(f"No course found with course_id: {course_id}")
                raise CourseNotFoundException("Course not found.")
        except CourseNotFoundException as e:
            logging.error(f"Course retrieval error for course_id {course_id}: {e}")
            raise e
        except Error as e:
            logging.error(f"Failed to retrieve course {course_id}: {e}")
            return None
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
            return course

    def get_student_courses(self):
        sql = "SELECT course_id, course_name, course_details, duration, start_date, end_date, available_seats, state, user_id FROM course WHERE state IN ('OPEN', 'ACTIVE');"
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
            courses = db_cursor.fetchall()
            print(courses)

            if courses:
                logging.info("Courses with state 'open' or 'active' retrieved successfully.")
                course_list = [
                    {
                        "course_id": course[0],
                        "course_name": course[1],
                        "course_details": course[2],
                        "duration": course[3],
                        "start_date": course[4].strftime("%d-%m-%y") if course[4] else None,
                        "end_date": course[5].strftime("%d-%m-%y") if course[5] else None,
                        "available_seats": course[6],
                        "state": course[7],
                    }
                    for course in courses
                ]
                return course_list
            else:
                logging.warning("No courses found in the database.")
                return []

        except Error as e:
            logging.error(f"Error retrieving courses: {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def get_teacher_courses(self, user_id):
        sql = "SELECT course_id, course_name, course_details, duration, start_date, end_date, available_seats, state FROM course WHERE user_id = %s;"
        val = (user_id,)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Failed to connect to the database.")
                return None

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            courses = db_cursor.fetchall()

            if courses:
                logging.info(f"Courses found for user_id {user_id}: {courses}")
                course_list = [
                    {
                        "course_id": course[0],
                        "course_name": course[1],
                        "course_details": course[2],
                        "duration": course[3],
                        "start_date": course[4].strftime("%d-%m-%y") if course[3] else None,
                        "end_date": course[5].strftime("%d-%m-%y") if course[4] else None,
                        "available_seats": course[6],
                        "state": course[7],
                    }
                    for course in courses
                ]
                return course_list
            else:
                logging.warning(f"No courses found for user_id: {user_id}")
                return []

        except Error as e:
            logging.error(f"Error retrieving courses for user_id {user_id}: {e}")
            return None

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def update(self, course_id, course_name, course_details, duration, start_date, end_date, available_seats, state,user_id):
        sql = "UPDATE course SET course_name = %s, course_details = %s, duration = %s, start_date = %s, end_date = %s, available_seats = %s, state= %s WHERE course_id = %s AND user_id = %s"
        val = (course_name, course_details, duration, start_date, end_date, available_seats, state, course_id, user_id)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                logging.error("Database connection failed")
                print("Database connection failed")

            db_cursor = db_connection.cursor()
            print(f"Executing SQL: {sql}")
            print(f"SQL Parameters: {val}")
            db_cursor.execute(sql, val)
            db_connection.commit()
            print(f"Rows affected: {db_cursor.rowcount}")

            if db_cursor.rowcount == 0:
                print(f"DBUserCourse: No Course found for userId {course_id}; update may have failed.")
                logging.warning(f"No course found for userId {user_id}; update may have failed.")
                return False
            else:
                print(f"DBUserCourse: Course updated successfully for courseId: {course_id}")
                logging.info(f"Course updated successfully for courseId: {course_id}")
                return True

        except Error as e:
            print(e)
            print(f"DBUserCourse: Failed to update user Course for userId {course_id}: {e}")
            logging.error(f"Failed to update user Course for userId {course_id}: {e}")
            if db_connection:
                db_connection.rollback()
                print("DBUserCourse: Transaction rolled back due to error.")
                logging.info("Transaction rolled back due to error.")
            return False

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
                print("Database connection closed")

    def approve(self, course_id, course_name):
        sql = "UPDATE course SET state = %s WHERE course_id = %s AND course_name = %s AND state = %s"
        new_state = OPEN
        current_state = PENDING_FOR_APPROVAL
        val = (new_state, course_id, course_name, current_state)

        print(sql)
        print(val)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                raise Exception("Database connection failed")

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            db_connection.commit()

            if db_cursor.rowcount == 0:
                logging.warning(f"No course found with course_id: {course_id} in PENDING FOR APPROVAL state.")
                return False

            logging.info(f"Course with course_id {course_id} approved successfully, state set to OPEN.")
            return True

        except Error as e:
            logging.error(f"Failed to approve course: {e}")
            if db_connection:
                db_connection.rollback()
            raise e
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def change_status_to_active(self, course_id, course_name):
        sql = "UPDATE course SET state = %s WHERE course_id = %s AND course_name = %s AND state = %s"
        new_state = "ACTIVE"
        current_state = "OPEN"
        val = (new_state, course_id, course_name, current_state)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                raise Exception("Database connection failed")

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            db_connection.commit()

            if db_cursor.rowcount == 0:
                logging.warning(f"No course found with course_id: {course_id} in OPEN state.")
                return False

            logging.info(f"Course with course_id {course_id} status updated to ACTIVE.")
            return True

        except Error as e:
            logging.error(f"Failed to change course status to ACTIVE: {e}")
            if db_connection:
                db_connection.rollback()
            raise e
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def reject_course_in_db(self, course_id, course_name):
        sql = "UPDATE course SET state = %s WHERE course_id = %s AND course_name = %s AND state IN (%s, %s)"
        new_state = "REJECTED"
        current_states = ("OPEN", "ACTIVE")
        val = (new_state, course_id, course_name, *current_states)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                raise Exception("Database connection failed")

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            db_connection.commit()

            if db_cursor.rowcount == 0:
                logging.warning(f"No course found with course_id: {course_id} in OPEN or ACTIVE state.")
                return False

            logging.info(f"Course with course_id {course_id} status updated to REJECTED.")
            return True

        except Error as e:
            logging.error(f"Failed to change course status to REJECTED: {e}")
            if db_connection:
                db_connection.rollback()
            raise e
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def cancel_course_in_db(self, course_id, course_name):
        sql = "UPDATE course SET state = %s WHERE course_id = %s AND course_name = %s AND state IN (%s, %s)"
        new_state = "CANCELLED"
        current_states = ("OPEN", "ACTIVE")
        val = (new_state, course_id, course_name, *current_states)

        print(sql)
        print(val)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                raise Exception("Database connection failed")

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            db_connection.commit()

            if db_cursor.rowcount == 0:
                logging.warning(f"No course found with course_id: {course_id} in OPEN or ACTIVE state.")
                return False

            logging.info(f"Course with course_id {course_id} status updated to CANCELLED.")
            return True

        except Error as e:
            logging.error(f"Failed to cancel course {course_id}: {e}")
            if db_connection:
                db_connection.rollback()
            raise e
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()

    def complete_course_in_db(self, course_id, course_name):
        sql = "UPDATE course SET state = %s WHERE course_id = %s AND course_name = %s AND state IN (%s, %s)"
        new_state = "COMPLETED"
        current_states = ("OPEN", "ACTIVE")
        val = (new_state, course_id, course_name, *current_states)

        db_connection = None
        db_cursor = None

        try:
            db_connection = self.get_connection()
            if db_connection is None:
                raise Exception("Database connection failed")

            db_cursor = db_connection.cursor()
            db_cursor.execute(sql, val)
            db_connection.commit()

            if db_cursor.rowcount == 0:
                logging.warning(f"No course found with course_id: {course_id} in OPEN or ACTIVE state.")
                return False

            logging.info(f"Course with course_id {course_id} status updated to COMPLETED.")
            return True

        except Error as e:
            logging.error(f"Failed to change course status to COMPLETED: {e}")
            if db_connection:
                db_connection.rollback()
            raise e
        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection and db_connection.is_connected():
                db_connection.close()
