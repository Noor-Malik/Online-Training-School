import logging
from flask import session
from select import error
from DBTeacherAssignments import DBTeacherAssignments
from OTExceptions import DuplicateAssignmentException


class TeacherAssignments:
    def __init__(self, file_id=None, course_id=None, teacher_id=None, assignment_name=None, file_type=None, file_path=None,uploaded_at=None, status=None):
        self.file_id = file_id
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.assignment_name = assignment_name
        self.file_type = file_type
        self.file_path = file_path
        self.uploaded_at = uploaded_at
        self.status = status

    def create_assignment(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Entering get_course for course_id")
        print("Entered create_course method")
        print(session)

        try:
            print("Attempting to create course in database")
            db_teacher_assignments = DBTeacherAssignments()
            assignment = db_teacher_assignments.create(self.course_id, self.teacher_id, self.assignment_name, self.file_type, self.file_path,self.uploaded_at, self.status)
            logger.info(f"Assignment saved for user_id: {self.teacher_id}")
            return assignment

        except DuplicateAssignmentException as e:
            logger.warning(f"Duplicate course error: {str(e)}")
            print("Duplicate course error:", str(e))
            raise e

        except Exception as e:
            logger.error(f"An unexpected error occurred during course creation for '{self.assignment_name}': {e}")
            print(f"Error occurred during course creation: {e}")
            raise e

    def get_homework(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info("Fetching all homework from the database.")
        print("Entering get all homework")

        try:
            db_assignment = DBTeacherAssignments()
            homework = db_assignment.get_homework()

            if homework is not None:
                logger.info("Successfully retrieved all homework.")
                return homework
            else:
                logger.warning("No homework found in the database.")
                return []

        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving all homework: {e}")
            print(f"Error occurred while retrieving all homework: {e}")
            raise e

    def get_course_homework(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Fetching courses for user_id: {self.course_id}")

        try:
            db_assignment = DBTeacherAssignments()
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

    def get_student_homework(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Fetching courses for user_id: {self.course_id}")

        try:
            db_assignment = DBTeacherAssignments()
            work = db_assignment.get_student_homework(self.course_id)

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

    def assign_work(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info("Entering assign_work method")
        print("Entering to assign work")

        if not self.file_id:
            raise error("file ID is required to assign homework.")

        try:
            db_assignment = DBTeacherAssignments()
            assign = db_assignment.assign_work(self.file_id)

            if assign:
                logger.info(f"Homework '{self.assignment_name}' assigned and set to Active.")
            else:
                logger.error(f"Homework failed: homework '{self.assignment_name}' already exists.")
            return assign

        except error as e:
            print(f"Course homework already exists: {e.message}")
            logger.error(f"record already exists detected: {e.message}")
            raise e