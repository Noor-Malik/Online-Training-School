import logging
from DBUser import DBUser
from OTExceptions import DuplicateRecordException, InvalidCredentialsException

class User:
    def __init__(self, email=None, password=None, userType=None, securityQuestion=None, passwordHint=None):
        self.email = email
        self.password = password
        self.userType = userType
        self.securityQuestion = securityQuestion
        self.passwordHint = passwordHint

    def login(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info('Entering user login')

        try:
            db_User = DBUser()
            db_user_record = db_User.select_login(self.email, self.password, self.userType)
            if db_user_record:
                logger.info(f"User {self.email} logged in successfully.")
                print(db_user_record)
                print(db_user_record[3])
                return db_user_record
            else:
                logger.warning(f"Login failed for {self.email}. Incorrect credentials.")
                raise InvalidCredentialsException(1002, "Invalid login credentials.")
        except InvalidCredentialsException as e:
            logger.error(f"Login error for {self.email}: {e}")
            raise e
        except Exception as e:
            logger.error(f"An unexpected error occurred during login for {self.email}: {e}")
            raise e

    def register(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info('Entering user registration')

        try:
            db_User = DBUser()
            userId = db_User.create(self.email, self.password, self.userType, self.securityQuestion, self.passwordHint)

            if userId:
                logger.info(f"User {self.email} registered successfully with userId: {userId}")
                return userId
            else:
                logger.error("Failed to register user due to database issue")
                raise Exception("User registration failed")

        except DuplicateRecordException as e:
            logger.error(f"Registration error for {self.email}: {e}")
            raise e

    def verify_hint(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info('Entering verify hint')

        try:
            db_User = DBUser()
            print("Email", self.email)
            print("User type", self.userType)
            print("Security Question", self.securityQuestion)
            print("User Hint", self.passwordHint)

            db_user_data = db_User.select_hint(self.email, self.userType, self.securityQuestion, self.passwordHint)
            if db_user_data:
                logger.info(f"User {self.email} hint verified successfully.")
                return db_user_data
            else:
                logger.warning(f"verify failed for {self.email}. Incorrect user hint.")
                raise InvalidCredentialsException(1002, "Invalid user hint.")
        except InvalidCredentialsException as e:
            logger.error(f"Error for hint verification {self.email}: {e}")
            raise e
        except Exception as e:
            logger.error(f"An unexpected error occurred during verification for user hint {self.email}: {e}")
            raise e

    def changePassword(self, newPassword):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info('Entering password change')
        print("Entering change password")

        try:
            db_User = DBUser()
            user_pass = db_User.updatePassword(self.email, self.userType, newPassword)

            if self.password == newPassword:
                raise ValueError("New password cannot be the same as the old password.")

            if user_pass:
                logger.info(f"User {self.email} password changed successfully.")
                return user_pass
            else:
                logger.warning(f"verify failed for {self.email}. Incorrect user hint.")
                raise InvalidCredentialsException(1002, "Invalid user hint.")

        except ValueError as ve:
            logger.warning(f"Password change error for {self.email}: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"An unexpected error occurred during password change for {self.email}: {e}")
            raise e

    def get_userId(self):
        pass