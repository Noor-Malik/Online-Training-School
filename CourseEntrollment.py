import logging
from datetime import datetime
from DBCourseEnrollment import DBCourseEnrollment
from OTExceptions import PermissionDeniedException, EnrollmentException, CourseNotFoundException

REQUEST_FOR_APPROVAL = "REQUEST_FOR_APPROVAL"
OPEN = "OPEN"
ACTIVE = "ACTIVE"
COMPLETED = "COMPLETED"
CANCELLED = "CANCELLED"
REJECTED = "REJECTED"
ADMIN = "ADMIN"
TEACHER = "TEACHER"
STUDENT = "STUDENT"

class CourseEnrollment:
    def __init__(self, course_id=None, student_id=None, enrollment_date=None, status=None):
        self.course_id = course_id
        self.student_id = student_id
        self.enrollment_date = enrollment_date or datetime.now()
        self.status = status
        self.db = DBCourseEnrollment()
        print(f"Initialized CourseEnrollment for course_id: {course_id}, student_id: {student_id}")

    def view_course(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Entering view_course for course_id: {self.course_id}")
        print(f"Entering view_course for course_id: {self.course_id}")

        try:
            db_course = DBCourseEnrollment()
            course = db_course.select_course(self.course_id)
            if course:
                logger.info(f"Course details retrieved successfully for course_id: {self.course_id}")
                print(f"Course details: {course}")
                return course
            else:
                logger.warning(f"Course with course_id: {self.course_id} not found.")
                return course
        except CourseNotFoundException as e:
            logger.error(f"Course retrieval error for course_id: {self.course_id}: {e}")
            print(f"Course retrieval error: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error while retrieving course_id: {self.course_id}: {e}")
            print(f"Unexpected error: {e}")
            raise e

    def enroll_student(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info("Entering enroll_student method")
        print("Entering enroll_student method")

        try:
            db_enrollment = DBCourseEnrollment()
            course_status = db_enrollment.get_course_status(self.course_id)
            print(f"Course status for course_id {self.course_id}: {course_status}")

            if course_status != OPEN:
                logger.warning(f"Course {self.course_id} is not open for enrollment.")
                print(f"Course {self.course_id} is not open for enrollment.")
                raise PermissionDeniedException("Course is not open for enrollment.")

            # select if the student already enrolled
            enrollment_status = db_enrollment.enroll_student(self.course_id, self.student_id)

            if enrollment_status:
                logger.info(f"Student {self.student_id} successfully requested enrollment in course {self.course_id}.")
                print(f"Enrollment request for student {self.student_id} in course {self.course_id} successful.")
                return True
            else:
                logger.warning(f"Failed to request enrollment for course {self.course_id}.")
                print(f"Failed to request enrollment for course {self.course_id}.")
                return False

        except PermissionDeniedException as e:
            logger.error(f"Permission error during enrollment: {e}")
            print("Permission error during enrollment:", str(e))
            raise e
        except EnrollmentException as e:
            logger.error(f"Unexpected error during enrollment: {e}")
            print("Unexpected error during enrollment:", str(e))
            raise e

    def cancel_enrollment_request(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Entering cancel_enrollment_request for student_id: {self.student_id} and course_id: {self.course_id}")
        print(f"Entering cancel_enrollment_request for student_id: {self.student_id} and course_id: {self.course_id}")

        try:
            db_enrollment = DBCourseEnrollment()
            cancellation_result = db_enrollment.cancel_enrollment(self.course_id, self.student_id)

            if cancellation_result:
                logger.info(f"Enrollment request for student_id {self.student_id} in course_id {self.course_id} successfully canceled.")
                print(f"Enrollment request for student {self.student_id} in course {self.course_id} canceled successfully.")
                return True
            else:
                logger.warning(f"No enrollment request found to cancel for student_id {self.student_id} in course_id {self.course_id}.")
                print(f"No enrollment request to cancel for student {self.student_id} in course {self.course_id}.")
                return False

        except EnrollmentException as e:
            logger.error(f"Unexpected error during cancellation: {e}")
            print("Unexpected error during cancellation:", str(e))
            raise e



