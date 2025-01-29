import logging
from flask import session
from select import error
from DBStudentHomework import DBStudentHomework
from OTExceptions import DuplicateAssignmentException

class StudentHomework:
    def __init__(self, file_type=None, homework_name=None, score=None, course_id=None, student_id=None, status=None, file_id=None, submitted_at=None, homework_id=None, file_path=None):
        self.file_type = file_type
        self.homework_name = homework_name
        self.score = score
        self.course_id = course_id
        self.student_id = student_id
        self.status = status
        self.file_id = file_id
        self.submitted_at = submitted_at
        self.homework_id = homework_id
        self.file_path = file_path

    def submit_homework(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Entering get_course for course_id")
        print("Entered create_course method")
        print(session)

        try:
            print("Attempting to create course in database")
            db_assignment = DBStudentHomework()
            assignment = db_assignment.submit_homework(self.course_id,self.file_id, self.student_id, self.homework_name, self.file_type, self.file_path,self.submitted_at, self.status)
            logger.info(f"Assignment saved for user_id: {self.student_id}")
            return assignment

        except DuplicateAssignmentException as e:
            logger.warning(f"Duplicate course error: {str(e)}")
            print("Duplicate course error:", str(e))
            raise e

        except Exception as e:
            logger.error(f"An unexpected error occurred during course creation for '{self.homework_name}': {e}")
            print(f"Error occurred during course creation: {e}")
            raise e

    def get_student_homework(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Fetching courses for user_id: {self.course_id}")

        try:
            db_assignment = DBStudentHomework()
            work = db_assignment.get_course_homework(self.course_id)

            if work is not None:
                logger.info(f"Successfully retrieved homework for course_id: {self.course_id}")
                return work
            else:
                logger.warning(f"No homework found for course_id: {self.course_id}")
                return []

        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving homework for course_id {self.course_id}: {e}")
            print(f"Error occurred while retrieving courses: {e}")
            raise e
