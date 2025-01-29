import logging
from flask import session
from DBCourse import DBCourse
from OTExceptions import PermissionDeniedException, DuplicateCourseException, CourseNotFoundException, InvalidCourseDataException, InvalidCourseStateException

PENDING_FOR_APPROVAL = "PENDING FOR APPROVAL"
OPEN = "OPEN"
ACTIVE = "ACTIVE"
COMPLETED = "COMPLETED"
CANCELLED = "CANCELLED"
REJECTED = "REJECTED"
ADMIN = "ADMIN"
TEACHER = "TEACHER"
STUDENT = "STUDENT"

class Course:
    def __init__(self, course_id=None, course_name=None, course_details=None, duration=None, start_date=None, end_date=None,available_seats=None, user_id=None, state=None, user_type=None):
        self.course_id = course_id
        self.course_name = course_name
        self.course_details = course_details
        self.duration = duration
        self.start_date = start_date
        self.end_date = end_date
        self.available_seats = available_seats
        self.user_id = user_id
        self.state = state
        self.user_type = user_type

    def is_valid(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Checking user data is valid for user_id: {self.user_id}")

        if not all([self.course_name, self.course_details, self.duration, self.start_date, self.end_date, self.available_seats]):
            logger.error("Invalid profile data: Missing required fields")
            return False
        return True

    def get_course_detail(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Entering get_course for course_id")
        print("Getting course detail")

        try:
            course_get = DBCourse()
            course = course_get.get_course(self.course_id)

            if course:
                logger.info(f"Course details retrieved successfully for course_id: {self.course_id}")
                return course
            else:
                logger.warning(f"Course with course_id: {self.course_id} not found.")
                raise CourseNotFoundException("Course not found.")

        except CourseNotFoundException as e:
            logger.error(f"Course retrieval error for course_id: {self.course_id}: {e}")
            print(f"Course retrieval error: {e}")
            raise e

        except Exception as e:
            logger.error(f"Unexpected error while retrieving course_id: {self.course_id}: {e}")
            print(f"Unexpected error: {e}")
            raise e

    def get_teacher_courses(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Fetching courses for user_id: {self.user_id}")

        try:
            db_course = DBCourse()
            courses = db_course.get_teacher_courses(self.user_id)

            if courses is not None:
                logger.info(f"Successfully retrieved courses for user_id: {self.user_id}")
                return courses
            else:
                logger.warning(f"No courses found for user_id: {self.user_id}")
                return []

        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving courses for user_id {self.user_id}: {e}")
            print(f"Error occurred while retrieving courses: {e}")
            raise e

    def get_all_courses(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info("Fetching all courses from the database.")
        print("Entering get all courses")

        try:
            db_course = DBCourse()
            courses = db_course.get_all_courses()

            if courses is not None:
                logger.info("Successfully retrieved all courses.")
                return courses
            else:
                logger.warning("No courses found in the database.")
                return []

        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving all courses: {e}")
            print(f"Error occurred while retrieving all courses: {e}")
            raise e

    def get_student_courses(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info("Fetching all courses with state 'open' or 'active' from the database.")
        print("Entering get student courses")

        try:
            db_course = DBCourse()
            courses = db_course.get_student_courses()

            if courses is not None:
                logger.info("Successfully retrieved all courses.")
                return courses
            else:
                logger.warning("No courses found in the database.")
                return []

        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving all courses: {e}")
            print(f"Error occurred while retrieving all courses: {e}")
            raise e

    def create_course(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Entering get_course for course_id")
        print("Entered create_course method")
        print(session)
        if not self.is_valid():
            raise InvalidCourseDataException("All course fields (course_name, course_details, duration, start_date, end_date, available_seats, state, user_id) are required.")

        try:
            print("Attempting to create course in database")
            db_course = DBCourse()
            course = db_course.create(self.course_name, self.course_details, self.duration, self.start_date, self.end_date, self.available_seats, self.state, self.user_id)
            logger.info(f"Course saved for user_id: {self.user_id}")
            return course

        except DuplicateCourseException as e:
            logger.warning(f"Duplicate course error: {str(e)}")
            print("Duplicate course error:", str(e))
            raise e

        except Exception as e:
            logger.error(f"An unexpected error occurred during course creation for '{self.course_name}': {e}")
            print(f"Error occurred during course creation: {e}")
            raise e

    def update_course(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Entering update_course for course_id: {self.course_id}")
        print(f"Entered update_course method for course_id: {self.course_id}")

        if not self.course_id:
            print("Course ID is missing!")
            raise InvalidCourseDataException("Course ID is required to update a course.")

        if not self.state == PENDING_FOR_APPROVAL:
            print("Course state is not valid to update course!")
            raise InvalidCourseStateException("Course state is not valid to update course.")

        try:
            print("Attempting to update course in database")
            db_course = DBCourse()
            db_course.update(self.course_id, self.course_name, self.course_details, self.duration,self.start_date, self.end_date, self.available_seats, self.state, self.user_id)
            logger.info(f"Course updated successfully for course_id: {self.course_id}")
            print(f"Course updated successfully for course_id: {self.course_id}")

        except CourseNotFoundException as e:
            logger.warning(f"Course not found: {str(e)}")
            print(f"Course not found: {str(e)}")
            raise e

        except Exception as e:
            logger.error(f"An error occurred while updating course (course_id: {self.course_id}): {e}")
            print(f"Error occurred during course update: {e}")
            raise e

    def get_courses_by_state(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
        logger.info(f"Fetching courses with state '{self.state}' for user_id {self.user_id}")
        print("Entering in get course state")

        try:
            db_course = DBCourse()
            courses = db_course.get_courses_by_state(self.user_id, self.state)

            if courses is not None:
                logger.info(f"Successfully retrieved courses with state '{self.state}' for user_id {self.user_id}")
                return courses
            else:
                logger.warning(f"No courses found with state '{self.state}' for user_id {self.user_id}")
                return []

        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving courses with state '{self.state}': {e}")
            raise e

    def filtered_courses(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
        logger.info(f"Fetching courses with state '{self.state}' for user_id {self.user_id}")
        print("Entering in get filter state")

        try:
            db_course = DBCourse()
            courses = db_course.filtered_courses(self.course_name, self.start_date, self.end_date, self.state)

            if courses is not None:
                logger.info(f"Successfully retrieved courses with state '{self.state}' for user_id {self.user_id}")
                return courses
            else:
                logger.warning(f"No courses found with state '{self.state}' for user_id {self.user_id}")
                return []

        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving courses with state '{self.state}': {e}")
            raise e

    def admin_filters(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
        logger.info(f"Fetching courses with state '{self.state}' for user_id {self.user_id}")
        print("Entering in get filter state")

        try:
            db_course = DBCourse()
            courses = db_course.admin_filters(self.course_name, self.start_date, self.end_date, self.state)

            if courses is not None:
                logger.info(f"Successfully retrieved courses with state '{self.state}' for user_id {self.user_id}")
                return courses
            else:
                logger.warning(f"No courses found with state '{self.state}' for user_id {self.user_id}")
                return []

        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving courses with state '{self.state}': {e}")
            raise e

    def filter_courses(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
        logger.info(f"Fetching courses with state '{self.state}' for user_id {self.user_id}")
        print("Entering in get filter state")

        try:
            db_course = DBCourse()
            courses = db_course.filter_courses(self.user_id, self.course_name, self.start_date, self.end_date, self.state)

            if courses is not None:
                logger.info(f"Successfully retrieved courses with state '{self.state}' for user_id {self.user_id}")
                return courses
            else:
                logger.warning(f"No courses found with state '{self.state}' for user_id {self.user_id}")
                return []

        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving courses with state '{self.state}': {e}")
            raise e

    def approve_course(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info("Entering approve_course method")
        print("Entering to approve course")

        if not self.course_id:
            raise InvalidCourseDataException("Course ID is required to update a course.")

        try:
            db_course = DBCourse()
            approved = db_course.approve(self.course_id, self.course_name)

            if approved:
                logger.info(f"Course '{self.course_name}' approved and set to OPEN.")
            else:
                logger.error(f"Approval failed: Course '{self.course_name}' is not in PENDING_FOR_APPROVAL state.")
            return approved

        except PermissionDeniedException as e:
            print(f"Course is not in PENDING_FOR_APPROVAL status: {e.message}")
            logger.error(f"Undefined state detected: {e.message}")
            raise e

    def change_status_to_active(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"User entering in change status")
        print("Entering to change status.")

        if not self.course_id:
            raise InvalidCourseDataException("Course ID is required to update a course.")

        try:
            db_course = DBCourse()
            current_status = db_course.get_status(self.course_id)

            if current_status != 'OPEN':
                logger.error(f"Cannot change course_id {self.course_id} to ACTIVE. Current status: {current_status}")
                raise Exception("Course must be in OPEN state to transition to ACTIVE.")

            db_course = DBCourse()
            db_course.change_status_to_active(self.course_id, self.course_name)

        except Exception as e:
            logger.error(f"Error while changing status to ACTIVE for course_id {self.course_id}: {e}")
            raise e

    def reject_course(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info("Entering reject_course method")

        if not self.course_id:
            raise InvalidCourseDataException("Course ID is required to update a course.")

        db_course = DBCourse()
        current_status = db_course.get_status(self.course_id)

        if current_status != 'OPEN' and  current_status !='ACTIVE':
            logger.error(f"Course ID {self.course_id} is not in OPEN or ACTIVE state; cannot reject.")
            raise Exception("Course must be in OPEN or ACTIVE state to be rejected.")

        rejected = db_course.reject_course_in_db(self.course_id, self.course_name)
        if rejected:
            logger.info(f"Course '{self.course_name}' status changed to REJECTED.")
        else:
            logger.error(f"Failed to update course '{self.course_name}' to REJECTED.")

    def cancel_course(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info("Entering cancel_course method")

        if not self.course_id:
            raise InvalidCourseDataException("Course ID is required to update a course.")

        db_course = DBCourse()
        current_status = db_course.get_status(self.course_id)

        if current_status != 'OPEN' and  current_status !='ACTIVE':
            logger.error(f"Course ID {self.course_id} is not in OPEN or ACTIVE state; cannot be cancelled.")
            raise Exception("Course must be in OPEN or ACTIVE state to be cancelled.")

        db_course = DBCourse()
        cancelled = db_course.cancel_course_in_db(self.course_id, self.course_name)

        if cancelled:
            logger.info(f"Course '{self.course_name}' status updated to CANCELLED.")
        else:
            logger.error(f"Cancelled course '{self.course_name}': ")

    def complete_course(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info("Entering complete_course method")

        if not self.course_id:
            raise InvalidCourseDataException("Course ID is required to update a course.")

        db_course = DBCourse()
        current_status = db_course.get_status(self.course_id)

        if current_status != 'OPEN' and  current_status !='ACTIVE':
            logger.error(f"Course ID {self.course_id} is not in OPEN or ACTIVE state; cannot complete.")
            raise Exception("Course must be in OPEN or ACTIVE state to be completed.")

        completed = db_course.complete_course_in_db(self.course_id, self.course_name)
        if completed:
            logger.info(f"Course '{self.course_name}' status changed to COMPLETED.")
        else:
            logger.error(f"Failed to update course '{self.course_name}' to COMPLETED.")




