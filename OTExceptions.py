class DuplicateRecordException(Exception):
    def __init__(self, errorno, message="Duplicate entry: user already exists"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsException(Exception):
    def __init__(self, errorno, message="Invalid credentials: Incorrect username or password"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class PasswordRetrievalException(Exception):
    def __init__(self, errorno, message="Password retrieval failed: User not found"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

# New exceptions for user profile management, login, and password change
class PasswordMismatchException(Exception):
    def __init__(self, errorno, message="Password change failed: Current password is incorrect"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class DuplicateEnrollmentException(Exception):
    def __init__(self, errorno, message="Duplicate entry: user already exists"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class WeakPasswordException(Exception):
    def __init__(self, errorno, message="Password change failed: New password is too weak"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class ProfileNotFoundException(Exception):
    def __init__(self, errorno, message="Profile not found"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class DuplicateProfileException(Exception):
    def __init__(self, errorno, message="Profile creation failed: Profile already exists"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class InvalidProfileDataException(Exception):
    def __init__(self, errorno, message="Profile update failed: Invalid data provided"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class PermissionDeniedException(Exception):
    def __init__(self, errorno):
        self.errorno = errorno
        self.message = "Permission denied: You do not have access to perform this action"
        super().__init__(self.message)

class InvalidCourseDataException(Exception):
    def __init__(self, errorno, message="Course update failed: Invalid data provided"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class InvalidAssignmentDataException(Exception):
    def __init__(self, errorno, message="Assignment update failed: Invalid data provided"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class InvalidCourseStateException(Exception):
    def __init__(self, errorno, message="Course update failed: State is not valid"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class DuplicateCourseException(Exception):
    def __init__(self, errorno, message="Duplicate entry: course already exists"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class DuplicateAssignmentException(Exception):
    def __init__(self, errorno, message="Duplicate entry: assignment already exists"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

class CourseNotFoundException(Exception):
    def __init__(self, errorno):
        self.errorno = errorno
        self.message = "Course not found: The specified course does not exist"
        super().__init__(self.message)

class EnrollmentException(Exception):
    def __init__(self, errorno, message="Enrollment failed: Unable to process enrollment request"):
        self.errorno = errorno
        self.message = message
        super().__init__(self.message)

# User management class
class UserManagementSystem:
    def __init__(self):
        self.users = {}  # Format: {username: {"password": "password", "profile": profile_data}}

    # User registration method
    def register_user(self, username, password):
        if username in self.users:
            raise DuplicateRecordException(1001)
        self.users[username] = {"password": password, "profile": None}
        print(f"User {username} registered successfully!")

    # User login method
    def login_user(self, username, password):
        if username not in self.users or self.users[username]["password"] != password:
            raise InvalidCredentialsException(1002)
        print(f"User {username} logged in successfully!")

    # Forget password method
    def forget_password(self, username):
        if username not in self.users:
            raise PasswordRetrievalException(1003)
        print(f"Password for {username} is: {self.users[username]['password']}")

    # Change password method
    def change_password(self, username, current_password, new_password):
        if username not in self.users or self.users[username]["password"] != current_password:
            raise PasswordMismatchException(1004)
        if len(new_password) < 8:  # Example of a simple password strength rule
            raise WeakPasswordException(1005)
        self.users[username]["password"] = new_password
        print(f"Password for {username} changed successfully!")

    # Create user profile method
    def create_profile(self, username, profile_data):
        if username not in self.users:
            raise ProfileNotFoundException(1006)
        if self.users[username]["profile"] is not None:
            raise DuplicateProfileException(1007)
        self.users[username]["profile"] = profile_data
        print(f"Profile for {username} created successfully!")

    # Update user profile method
    def update_profile(self, username, profile_data):
        if username not in self.users:
            raise ProfileNotFoundException(1006)
        if not isinstance(profile_data, dict):  # Example validation
            raise InvalidProfileDataException(1008)
        self.users[username]["profile"].update(profile_data)
        print(f"Profile for {username} updated successfully!")



