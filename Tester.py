from OTExceptions import CourseNotFoundException
from User import User
from Course import Course, PermissionDeniedException, DuplicateCourseException, REQUEST_FOR_APPROVAL
from CourseEntrollment import  CourseEnrollment, EnrollmentException

def main():
    # testUserRegister()
    # testUserLogin()
    # testUserVerifyHint()
    # testUserChangePassword()
    # testCreateCourse()
    # testUpdateCourse()
    # testApproveCourse()
    # testChangeCourseStatusToActive()
    # testRejectCourse()
    # testCancelCourse()
    # testCompletedCourse()
    # testViewCourse()
    # testEnrollStudent()
    # testCancelEnrollmentRequest()
    # testGetCourse()
    testGet_course_status()


def testUserRegister():
    try:
        email = "sunn.doe@example.com"
        password = "password123"
        userType = "S"
        passwordHint = "1343"
        print("Registering user...")
        user = User(email,userType, password, passwordHint)
        user.register()
    except Exception as e:
        print(f"Error: {e}")

def testUserLogin():
    try:
        email = "sunn.doe@example.com"
        userType = "S"
        password = "password123"
        print("Attempting login...")
        user = User(email, password, userType)
        if user.login():
            print(f"{email} logged in successfully")
    except Exception as e:
        print(f"Error: {e}")

def testUserVerifyHint():
    try:
        email = "sunn.doe@example.com"
        userType = "S"
        passwordHint = "1343"
        print("Attempting verify hint...")
        user = User(email, userType, None, passwordHint)
        if user.verify_hint():
            print(f"{email} user hint verified successfully")
    except Exception as e:
        print(f"Error: {e}")

def testUserChangePassword():
    try:
        email = "john.doe@example.com"
        userType = "S"
        password = "password123"
        newPassword = "ABy8CD"
        print("Attempting to change password...")
        user = User(email, password, userType)
        if user.changePassword(newPassword):
            print(f"{email} logged in successfully")
    except Exception as e:
        print(f"Error: {e}")

def testCreateCourse():
    print("Testing course creation...")
    try:
        # Define test course details
        course_name = "Python Advanced"
        course_details = "An introductory course on Python"
        duration = "6 weeks"
        start_date = "2023-01-10"
        end_date = "2023-02-20"
        available_seats = 30
        course_state = "REQUEST_FOR_APPROVAL"
        user_id = 2
        user_type = "teacher"

        # Create Course instance
        course = Course(course_name=course_name,course_details=course_details,duration=duration,start_date=start_date,end_date=end_date,available_seats=available_seats,state=course_state,user_id=user_id,user_type=user_type)
        course_id = course.create_course()
        print(f"Course created successfully with course ID: {course_id}")

    except PermissionDeniedException as e:
        print(f"Permission denied: {e}")
    except DuplicateCourseException as e:
        print(f"Course already exists: {e}")
    except Exception as e:
        print(f"Error creating course: {e}")

def testUpdateCourse():
    print("Testing course update...")
    try:
        course_id = 18
        course_name = "Advanced Coding"
        course_details = "Advance Python and algorithms"
        duration = "9 weeks"
        start_date = "2024-02-01"
        end_date = "2024-03-29"
        available_seats = 25
        state = REQUEST_FOR_APPROVAL
        user_id = 2
        user_type = "teacher"

        # Create course instance
        course = Course(course_id=course_id, course_name=course_name, course_details=course_details,duration=duration, start_date=start_date, end_date=end_date, available_seats=available_seats,state=state, user_id=user_id, user_type=user_type)
        success = course.update_course()

        # Output result based on success
        if success:
            print(f"Course updated successfully for course ID: {course_id}")
        else:
            print(f"Course update failed for course ID: {course_id}")

    except PermissionDeniedException as e:
        print(f"Permission denied: {e}")
    except CourseNotFoundException as e:
        print(f"Course not found: {e}")
    except Exception as e:
        print(f"Error updating course: {e}")

def testApproveCourse():
    print("Testing course approval...")
    try:
        course_id = 23
        course_name = "Advanced Coding Program"
        state = "REQUEST_FOR_APPROVAL"
        user_id = 1
        user_type = "ADMIN"

        # Create course instance with the given test data
        course = Course(course_id=course_id, course_name=course_name, state=state, user_id=user_id, user_type=user_type)
        course.approve_course(course_id)
        print(f"Course approved successfully for course ID: {course_id}")

    except PermissionDeniedException as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Error approving course: {e}")

def testChangeCourseStatusToActive():
    print("Testing course status change to OPEN...")
    try:
        course_id = 23
        course_name = "Advanced Coding"
        initial_state = "ACTIVE"  # Set initial state to ACTIVE for testing
        user_id = 1
        user_type = "ADMIN"  # Can be "ADMIN" or "TEACHER"

        # Create course instance with the given test data
        course = Course(course_id=course_id, course_name=course_name, state=initial_state, user_id=user_id, user_type=user_type)

        # Call change_status_to_open to attempt to change the status to OPEN
        course.change_status_to_active(user_id)
        print(f"Course status updated to ACTIVE for course ID: {course_id}")

    except PermissionDeniedException as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Error changing course status: {e}")

def testRejectCourse():
    print("Testing course rejection...")
    try:
        course_id = 23
        course_name = "Advanced Python Programming"
        initial_state = "OPEN"  # Set initial state to OPEN or ACTIVE for testing
        user_id = 1
        user_type = "ADMIN"

        # Create course instance with the given test data
        course = Course(course_id=course_id, course_name=course_name, state=initial_state, user_id=user_id, user_type=user_type)

        # Attempt to reject the course
        course.reject_course(course_id)
        print(f"Course ID: {course_id} rejected successfully.")

    except PermissionDeniedException as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Error rejecting course: {e}")

def testCancelCourse():
    print("Testing course cancellation...")
    try:
        course_id = 20
        course_name = "Advanced Python Programming"
        initial_state = "OPEN"  # Set initial state to OPEN or ACTIVE for testing
        user_id = 1
        user_type = "ADMIN"

        # Create course instance with the given test data
        course = Course(course_id=course_id, course_name=course_name, state=initial_state, user_id=user_id, user_type=user_type)

        # Attempt to cancel the course
        course.cancel_course(course_id)
        print(f"Course ID: {course_id} cancelled successfully.")

    except PermissionDeniedException as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Error cancelling course: {e}")

def testCompletedCourse():
    print("Testing course completion...")
    try:
        course_id = 18
        course_name = "Advanced Python Programming"
        initial_state = "OPEN"  # Set initial state to OPEN or ACTIVE for testing
        user_id = 1
        user_type = "ADMIN"

        # Create course instance with the given test data
        course = Course(course_id=course_id, course_name=course_name, state=initial_state, user_id=user_id, user_type=user_type)

        # Attempt to complete the course
        course.complete_course(course_id)
        print(f"Course ID: {course_id} completed successfully.")

    except PermissionDeniedException as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Error completing course: {e}")

def testViewCourse():
    print("Testing view_course...")
    try:
        course_id = 23

        # Create CourseEnrollment instance
        course_enrollment = CourseEnrollment()

        # Attempt to view the course details
        course_details = course_enrollment.view_course(course_id)
        if course_details:
            print(f"Course details for course ID {course_id} retrieved successfully.")
        else:
            print(f"Course ID {course_id} not found.")

    except CourseNotFoundException as e:
        print(f"Course not found: {e}")
    except Exception as e:
        print(f"Error viewing course: {e}")

def testEnrollStudent():
    print("Testing enroll_student...")
    try:
        course_id = 23
        student_id = 185

        # Create CourseEnrollment instance with test data
        course_enrollment = CourseEnrollment(course_id=course_id, student_id=student_id)

        # Attempt to enroll the student in the course
        enrollment_result = course_enrollment.enroll_student()
        if enrollment_result:
            print(f"Student ID: {student_id} successfully enrolled in course ID: {course_id}.")
        else:
            print(f"Enrollment request for student ID: {student_id} in course ID: {course_id} failed.")

    except PermissionDeniedException as e:
        print(f"Permission denied: {e}")
    except EnrollmentException as e:
        print(f"Enrollment error: {e}")
    except Exception as e:
        print(f"Unexpected error during enrollment: {e}")

def testCancelEnrollmentRequest():
    print("Testing cancel_enrollment_request...")
    try:
        course_id = 23
        student_id = 185

        # Create CourseEnrollment instance with test data
        course_enrollment = CourseEnrollment(course_id=course_id, student_id=student_id)

        # Attempt to cancel the enrollment request
        cancellation_result = course_enrollment.cancel_enrollment_request()
        if cancellation_result:
            print(f"Enrollment request for student ID: {student_id} in course ID: {course_id} canceled successfully.")
        else:
            print(f"No enrollment request to cancel for student ID: {student_id} in course ID: {course_id}.")

    except EnrollmentException as e:
        print(f"Cancellation error: {e}")
    except Exception as e:
        print(f"Unexpected error during cancellation: {e}")

def testGetCourse():
    print("Testing get_course...")

    try:
        course_id = 18

        course = Course(course_id=course_id)
        course_details = course.get_course_detail()
        if course_details:
            print(f"Course details for {course_id} retrieved successfully.")
        else:
            print(f"{course_id} not found.")

    except CourseNotFoundException as e:
        print(f"Course not found: {e}")
    except Exception as e:
        print(f"Error viewing course: {e}")

if __name__ == "__main__":
    main()
