import logging
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, session, send_from_directory, abort
from flask_session import Session
from flask_cors import CORS
from OTExceptions import (DuplicateRecordException, InvalidCredentialsException, DuplicateProfileException,InvalidProfileDataException, PermissionDeniedException, DuplicateCourseException,CourseNotFoundException, PasswordMismatchException, DuplicateEnrollmentException,InvalidCourseStateException, DuplicateAssignmentException)
from User import User
from UserProfile import UserProfile
from Course import Course
from CourseEntrollment import CourseEnrollment
from TeacherAssignments import TeacherAssignments
from StudentHomework import StudentHomework

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'BAD_SECRET_KEY'
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session_data"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
Session(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx']
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.post("/register")
def register_user():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
    logger.info('Entering Register User')

    if not request.is_json:
        logger.info('Exiting registerUser - request is not JSON')
        return jsonify({"error": "Request must be JSON"}), 400

    jsonstring = request.get_json()
    email = jsonstring.get("email")
    password = jsonstring.get("password")
    userType = jsonstring.get("userType")
    securityQuestion = jsonstring.get("securityQuestion")
    passwordHint = jsonstring.get("passwordHint")

    logger.debug("Email: %s", email)
    logger.debug("Password: %s", password)
    logger.debug("UserType: %s", userType)
    logger.debug("securityQuestion: %s", securityQuestion)
    logger.debug("passwordHint: %s", passwordHint)

    try:
        user = User(email, password, userType, securityQuestion, passwordHint)
        userId = user.register()

        if userId:
            session['userId'] = userId
            logger.info(f"User registered successfully with userId: {userId}")
            return jsonify({"message": "User registered successfully"}), 201
        else:
            return jsonify({"error": "Failed to register user"}), 500

    except DuplicateRecordException as e:
        logger.error(f"Duplicate user registration attempt: {e.message}")
        return jsonify({"error": e.message}), 409

    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        return jsonify({"error": "System error"}), 500

@app.route('/user_login', methods=['POST'])
def user_login():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info('Entering User Login')

    if not request.is_json:
        return jsonify({"error": "Request payload must be in JSON format"}), 400

    json_data = request.get_json()
    email = json_data.get("email")
    password = json_data.get("password")
    userType = json_data.get("userType")

    logger.debug("Email: %s", email)
    logger.debug("Password: %s", password)
    logger.debug("UserType: %s", userType)

    if not email or not password:
        message = {"message": "Email and password are required"}
        logger.error(message)
        return jsonify(message), 400

    try:
        user = User(email=email, password=password, userType=userType)
        db_user_record = user.login()

        session['userId'] = db_user_record[3]
        session['email'] = email
        session['userType'] = userType
        session.modified = True

        logger.info(f"User logged in successfully with userId: {session['userId']}")
        return jsonify({f"message": "User logged in successfully", "userType": user.userType}), 200

    except InvalidCredentialsException:
        logger.error("Invalid email or password")
        return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@appdit .route('/verify', methods=['POST'])
def verify_user_hint():
    print("Session before setting in /verify:", dict(session))
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)

    jsonstring = request.get_json()
    email = jsonstring.get("email")
    userType = jsonstring.get("userType")
    securityQuestion = jsonstring.get("securityQuestion")
    passwordHint = jsonstring.get("passwordHint")

    logger.debug("Email: %s", email)
    logger.debug("UserType: %s", userType)
    logger.debug("securityQuestion: %s", securityQuestion)
    logger.debug("passwordHint: %s", passwordHint)

    if not email:
        logger.error("Email not provided")
        return jsonify({"message": "Email is required"}), 401

    if not userType:
        logger.error("Type not provided")
        return jsonify({"message": "User type is required"}), 402

    if not securityQuestion:
        logger.error("securityQuestion not provided")
        return jsonify({"message": "Security question is required"}), 403

    if not passwordHint:
        logger.error("Hint not provided")
        return jsonify({"message": "Hint is required"}), 404

    try:
        user = User(email=email, userType=userType, securityQuestion=securityQuestion, passwordHint=passwordHint)
        db_user_data = user.verify_hint()

        logger.info("user hint verified")
        session['email'] = email
        session['type'] = userType
        session['user_verified'] = "TRUE"
        print(session['email'])
        print(session['type'])
        print(session['user_verified'])
        print(session)
        return jsonify({"message": "user verified successfully!"}), 200

    except PasswordMismatchException as e:
        logger.error(f"Failed to verify user hint: {str(e)}")
        return jsonify({"message": "Failed to verify user hint"}), 500

@app.route('/reset', methods=['POST'])
def reset_password():
    print("Session data at reset start:", dict(session))
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)

    jsonstring = request.get_json()
    if not jsonstring:
        return jsonify({"message": "Invalid JSON request"}), 400

    try:
        email = session['email']
        userType = session['type']
        user_verified = session['user_verified']
        print(user_verified)
    except KeyError as e:
        logger.error(f"Session key error: {e}")
        return jsonify({"message": "Session data is missing or expired"}), 400

    newPassword = jsonstring.get("newPassword")
    logger.debug("Password: %s", newPassword)
    if not newPassword:
        return jsonify({"message": "Password is required"}), 400

    try:
        user = User(email=email, userType=userType)
        user.changePassword(newPassword)
        logger.info("User password changed successfully")
        return jsonify({"message": "Password changed successfully!"}), 200
    except PermissionDeniedException as e:
        logger.error("Exception occurred in resetPassword", exc_info=True)
        return jsonify({"message": "Failed to change user password"}), 500

@app.post('/create_profile')
def create_profile():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info('Entering Create Profile')
    print("Entering create password")

    if 'userId' not in session:
        logger.warning("Unauthorized profile creation attempt. Session: %s", session)
        return jsonify({"error": "User must be logged in to create a profile"}), 400

    user_id = session['userId']
    logger.debug(f"Retrieved userId from session: {user_id}")

    if not request.is_json:
        logger.error("Invalid payload format.")
        return jsonify({"error": "Request payload must be in JSON format"}), 401

    json_data = request.get_json()
    name = json_data.get("name")
    age = json_data.get("age")
    address = json_data.get("address")
    phone = json_data.get("phone")

    if not all([name, age, address, phone]):
        logger.error("Missing required profile fields.")
        return jsonify({"error": "All profile fields (name, age, address, phone) are required"}), 400

    try:
        user_profile = UserProfile(user_id=user_id, name=name, age=age, address=address, phone_number=phone)
        db_profile_result = user_profile.save()

        userprofileId = db_profile_result.get("userprofileId")
        if not userprofileId:
            logger.error("Failed to retrieve userprofileId after profile creation")
            return jsonify({"error": "Failed to create profile"}), 500

        session["userprofileId"] = userprofileId
        logger.info(f"Profile created for userId: {user_id} with profileId: {userprofileId}")
        return jsonify({"message": "Profile created successfully"}), 200

    except DuplicateProfileException as e:
        logger.error(f"Duplicate profile creation attempt for userId {user_id}: {e}")
        return jsonify({"error": "Profile already exists"}), 409

    except InvalidProfileDataException as e:
        logger.exception(f"Unexpected error during profile creation. {e}")
        return jsonify({"error": "Failed to create profile"}), 500

@app.post("/updateProfile")
def update_profile():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering updateProfile route")
    print("user entering to update profile")

    if 'userId' not in session and 'userprofileId' not in session:
        logger.warning("Missing userId or userprofileId in session.", session)
        return jsonify({"error": "User must be logged in with a valid profile to update"}), 401

    user_id = session['userId']
    user_profile_id = session['userprofileId']

    if not request.is_json:
        logger.warning("Invalid request format: not JSON")
        return jsonify({"error": "Request must be in JSON format"}), 402

    json_data = request.get_json()
    name = json_data.get("name")
    age = json_data.get("age")
    address = json_data.get("address")
    phone = json_data.get("phoneNumber")

    if not all([name, age, address, phone]):
        logger.error("Missing required profile fields.")
        return jsonify({"error": "All profile fields (name, age, address, phone) are required"}), 400

    try:
        print("Trying to update profile")
        profile = UserProfile(user_id=user_id, name=name, age=age, address=address, phone_number=phone, userprofileId=user_profile_id)
        update_result = profile.updateProfile()

        if update_result:
            logger.info(f"Profile updated successfully for userId: {user_id}")
            return jsonify({"message": "User profile updated successfully"}), 200
        else:
            logger.warning(f"No profile found to update for userId: {user_id}")
            return jsonify({"error": "Profile not found to update"}), 404

    except Exception as e:
        logger.error(f"Error updating profile for userId {user_id}: {str(e)}")
        return jsonify({"error": "Failed to update profile"}), 500

@app.get('/get_teacher_courses')
def get_teacher_courses():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_teacher_courses")

    if 'userId' not in session:
        logger.warning("Unauthorized course retrieval attempt. Session: %s", session)
        return jsonify({"error": "User must be logged in to view courses"}), 403

    user_id = session['userId']
    logger.info(f"Fetching courses for user_id {user_id}")

    try:
        course = Course(user_id=user_id)
        courses = course.get_teacher_courses()

        logger.info(f"Courses fetched: {courses}")
        if not courses:
            logger.info(f"No courses found for user_id {user_id}")
            return jsonify({"courses": []}), 200

        logger.info(f"Successfully retrieved {len(courses)} courses for user_id {user_id}")
        return jsonify({"courses": courses}), 200

    except Exception as e:
        logger.error(f"Error fetching courses for user_id {user_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve courses"}), 500

@app.get('/get_all_courses')
def get_all_courses():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_all_courses route")
    print("Entering get all courses.")

    print(session)

    try:
        course = Course()
        courses = course.get_all_courses()

        if not courses:
            logger.info("No courses found in the database.")
            return jsonify({"courses": []}), 200

        logger.info(f"Successfully retrieved {len(courses)} courses.")
        return jsonify({"courses": courses}), 200

    except Exception as e:
        logger.error(f"Error fetching all courses: {str(e)}")
        return jsonify({"error": "Failed to retrieve courses"}), 500

@app.get('/get_student_courses')
def get_student_courses():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_student_courses route")
    print("Entering get student courses.")
    print(session)

    try:
        course = Course()
        courses = course.get_student_courses()

        if not courses:
            logger.info("No courses found in the database.")
            return jsonify({"courses": []}), 200

        logger.info(f"Successfully retrieved {len(courses)} courses.")
        return jsonify({"courses": courses}), 200

    except Exception as e:
        logger.error(f"Error fetching all courses: {str(e)}")
        return jsonify({"error": "Failed to retrieve courses"}), 500

@app.post('/create_course')
def create_course():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info('Entering Create Course')
    print("Entering create course")

    print(session)

    if 'userId' not in session and session.get('userType') != 'teacher':
        logger.warning('Unauthorized attempt to create course')
        return jsonify({"error": "Only teachers can create courses"}), 403

    if not request.is_json:
        logger.warning('Invalid request format: not JSON')
        return jsonify({"error": "Request must be in JSON format"}), 400

    json_data = request.get_json()
    course_name = json_data.get("course_name")
    course_details = json_data.get("course_details")
    duration = json_data.get("duration")
    start_date = json_data.get("start_date")
    end_date = json_data.get("end_date")
    available_seats = json_data.get("available_seats")
    state = json_data.get("state", "REQUEST_FOR_APPROVAL")

    logger.debug("Course Name: %s", course_name)
    logger.debug("Course Details: %s", course_details)
    logger.debug("Duration: %s", duration)
    logger.debug("Start Date: %s", start_date)
    logger.debug("End Date: %s", end_date)
    logger.debug("Available Seats: %s", available_seats)
    logger.debug("State: %s", state)

    print(json_data)

    try:
        course = Course(course_name=course_name, course_details=course_details, duration=duration,start_date=start_date, end_date=end_date, available_seats=available_seats, state= state, user_id=session['userId'])
        course_data = course.create_course()

        course_id = course_data.get("course_id")
        course_name = course_data.get("course_name")

        if not course_id and course_name:
            logger.error("Failed to retrieve userprofileId after profile creation")
            return jsonify({"error": "Failed to create profile"}), 500

        session["course_id"] = course_id
        session["course_name"] = course_name
        session.modified = True

        logger.info(f"Course created for userId: with course_id and course_name: {course_id}, {course_id}")
        return jsonify({"message": "Course created successfully"}), 200

    except DuplicateCourseException as e:
        logger.error(f"Duplicate course creation attempt: {e.message}")
        return jsonify({"error": e.message}), 409

    except Exception as e:
        logger.error(f"Unexpected error during course creation: {str(e)}")
        return jsonify({"error": "Failed to create course"}), 500

@app.post('/update_course')
def update_course():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info('Entering Update Course')
    print("Entering update course route")

    if 'userId' not in session or session.get('userType') != 'teacher':
        logger.warning('Unauthorized attempt to update course')
        print("Unauthorized user attempting to update course")
        return jsonify({"error": "Only teachers can update courses"}), 403

    if not request.is_json:
        logger.warning('Invalid request format: not JSON')
        print("Request is not in JSON format")
        return jsonify({"error": "Request must be in JSON format"}), 400

    user_id = session.get('userId')
    print(f"Session user_id: {user_id}")

    json_data = request.get_json()
    print(f"Received JSON data: {json_data}")

    course_id = json_data.get("course_id")
    course_name = json_data.get("course_name")
    course_details = json_data.get("course_details")
    duration = json_data.get("duration")
    start_date = json_data.get("start_date")
    end_date = json_data.get("end_date")
    available_seats = json_data.get("available_seats")
    state = json_data.get("state")

    print(f"Parsed input: course_name={course_name}, start_date={start_date}, state={state}")

    try:
        course = Course(course_id=course_id, course_name=course_name, course_details=course_details,duration=duration, start_date=start_date, end_date=end_date,available_seats=available_seats, state=state, user_id=user_id)
        update_status = course.update_course()

        logger.info(f"Course updated successfully for course_id: {course_id}")
        print(f"Course updated successfully for course_id: {course_id}")
        return jsonify({"message": "Course updated successfully."}), 200

    except InvalidCourseStateException as e:
        logger.error(f"Error updating course with state: {state} - {str(e)}")
        print(f"Error occurred: {e}")
        return jsonify({"message": "Failed to update the course. Invalid course state."}), 409

    except Exception as e:
        logger.error(f"Error updating course with course_id: {course_id} - {str(e)}")
        print(f"Error occurred: {e}")
        return jsonify({"message": "Failed to update the course."}), 500

@app.post('/get_courses_by_state')
def get_courses_by_state():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_courses_by_state route")
    print("Entering get courses by state")

    print(session)

    if 'userId' not in session:
        logger.warning("Unauthorized course retrieval attempt. Session: %s", session)
        return jsonify({"error": "User must be logged in to view courses"}), 403

    if not request.is_json:
        logger.warning("Invalid request format: not JSON")
        return jsonify({"error": "Request must be in JSON format"}), 402

    user_id = session['userId']
    json_data = request.get_json()
    state = json_data.get("state")

    logger.info(f"Fetching courses with state '{state}' for user_id {user_id}")

    try:
        course = Course(user_id=user_id, state=state)
        courses = course.get_courses_by_state()

        if not courses:
            logger.info(f"No courses found for state '{state}' and user_id {user_id}")
            return jsonify({"courses": []}), 200

        logger.info(f"Successfully retrieved {len(courses)} courses for state '{state}' and user_id {user_id}")
        return jsonify({"courses": courses}), 200

    except Exception as e:
        logger.error(f"Error fetching courses for state '{state}' and user_id {user_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve courses"}), 500

@app.post('/filtered_courses')
def filtered_courses():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_courses_by_state route")
    print("Entering get filter courses")

    print(session)

    if 'userId' not in session:
        logger.warning("Unauthorized course retrieval attempt. Session: %s", session)
        return jsonify({"error": "User must be logged in to view courses"}), 403

    if not request.is_json:
        logger.warning("Invalid request format: not JSON")
        return jsonify({"error": "Request must be in JSON format"}), 402

    user_id = session['userId']
    json_data = request.get_json()
    course_name = json_data.get("course_name")
    start_date = json_data.get("start_date")
    end_date = json_data.get("end_date")
    state = json_data.get("state")

    logger.info(f"Fetching courses with state '{course_name}','{start_date}', '{end_date}' and '{state}' for user_id {user_id}")

    try:
        course = Course(course_name=course_name, start_date=start_date, end_date=end_date, state=state)
        courses = course.filtered_courses()

        if not courses:
            logger.info(f"No courses found for state '{state}' and user_id {user_id}")
            return jsonify({"courses": []}), 200

        logger.info(f"Successfully retrieved {len(courses)} courses for state '{state}' and user_id {user_id}")
        return jsonify({"courses": courses}), 200

    except Exception as e:
        logger.error(f"Error fetching courses for state '{state}' and user_id {user_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve courses"}), 500

@app.post('/admin_filters')
def admin_filters():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_courses_by_state route")
    print("Entering get filter courses")

    print(session)

    if 'userId' not in session:
        logger.warning("Unauthorized course retrieval attempt. Session: %s", session)
        return jsonify({"error": "User must be logged in to view courses"}), 403

    if not request.is_json:
        logger.warning("Invalid request format: not JSON")
        return jsonify({"error": "Request must be in JSON format"}), 402

    user_id = session['userId']
    json_data = request.get_json()
    course_name = json_data.get("course_name")
    start_date = json_data.get("start_date")
    end_date = json_data.get("end_date")
    state = json_data.get("state")

    logger.info(f"Fetching courses with state '{course_name}','{start_date}', '{end_date}' and '{state}' for user_id {user_id}")

    try:
        course = Course(course_name=course_name, start_date=start_date, end_date=end_date, state=state)
        courses = course.admin_filters()

        if not courses:
            logger.info(f"No courses found for state '{state}' and user_id {user_id}")
            return jsonify({"courses": []}), 200

        logger.info(f"Successfully retrieved {len(courses)} courses for state '{state}' and user_id {user_id}")
        return jsonify({"courses": courses}), 200

    except Exception as e:
        logger.error(f"Error fetching courses for state '{state}' and user_id {user_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve courses"}), 500

@app.post('/filter_courses')
def filter_courses():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_courses_by_state route")
    print("Entering get filter courses")

    print(session)

    if 'userId' not in session:
        logger.warning("Unauthorized course retrieval attempt. Session: %s", session)
        return jsonify({"error": "User must be logged in to view courses"}), 403

    if not request.is_json:
        logger.warning("Invalid request format: not JSON")
        return jsonify({"error": "Request must be in JSON format"}), 402

    user_id = session['userId']
    json_data = request.get_json()
    course_name = json_data.get("course_name")
    start_date = json_data.get("start_date")
    end_date = json_data.get("end_date")
    state = json_data.get("state")

    logger.info(f"Fetching courses with state '{course_name}','{start_date}', '{end_date}' and '{state}' for user_id {user_id}")

    try:
        course = Course(user_id=user_id, course_name=course_name, start_date=start_date, end_date=end_date, state=state)
        courses = course.filter_courses()

        if not courses:
            logger.info(f"No courses found for state '{state}' and user_id {user_id}")
            return jsonify({"courses": []}), 200

        logger.info(f"Successfully retrieved {len(courses)} courses for state '{state}' and user_id {user_id}")
        return jsonify({"courses": courses}), 200

    except Exception as e:
        logger.error(f"Error fetching courses for state '{state}' and user_id {user_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve courses"}), 500

@app.route('/approve_course', methods=['POST'])
def approve_course():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info(f'Entering Approve Course for course_id')
    print("Entering approve Course")

    print(session)

    if 'userId' not in session or session.get('userType') != 'admin':
        logger.warning(f'Unauthorized attempt to approve course for course_id')
        return jsonify({"error": "Only admins can approve courses"}), 403

    if not request.is_json:
        logger.warning('Invalid request format: not JSON')
        return jsonify({"error": "Request must be in JSON format"}), 400

    user_id = session['userId']
    user_type = session['userType']

    json_data = request.get_json()
    course_name = json_data.get("course_name")
    course_id = json_data.get("course_id")

    if not course_id or not course_name:
        logger.error("Missing course_name or course_id in request data")
        return jsonify({"error": "Missing course_name or course_id"}), 400

    try:
        course = Course(user_id=user_id, course_id=course_id, course_name=course_name, user_type=user_type)
        approval_status = course.approve_course()

        logger.info(f"Course approved successfully for: {course_id}")
        return jsonify({"message": f"Course approved successfully for: {course_id}"}), 200

    except Exception as e:
        logger.error(f"Error approving course: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/change_status', methods=['POST'])
def change_status_to_active():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info(f'Entering Approve Course for course_id')
    print("Entering change status Course")

    if 'userId' not in session or session.get('userType') != 'admin' and session.get('userType') != 'teacher':
        logger.warning(f'Unauthorized attempt to approve course for course_id')
        return jsonify({"error": "Only admins can approve courses"}), 403

    if not request.is_json:
        logger.warning('Invalid request format: not JSON')
        return jsonify({"error": "Request must be in JSON format"}), 400

    user_id = session['userId']
    user_type = session['userType']

    json_data = request.get_json()
    course_name = json_data.get("course_name")
    course_id = json_data.get("course_id")

    try:
        course = Course(user_id=user_id, course_id=course_id, course_name=course_name, user_type=user_type)
        approval_status = course.change_status_to_active()

        user_id = session['userId']
        course_id = session['course_id']

        logger.info(f"Course status changed successfully for course_id: {user_id}")
        print(f"Course state updated successfully for course:{course_id}")
        return jsonify({"message": "Course status changed successfully"}), 200

    except Exception as e:
        logger.error(f"Error changing status of course with course_id: {course_id}: {str(e)}")
        return jsonify({"error": "Failed to change status course"}), 500

@app.route('/reject_course', methods=['POST'])
def reject_course():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info(f'Entering Reject Course for course_id')
    print("Entering reject course")

    if 'userId' not in session or session.get('userType') != 'admin':
        logger.warning(f'Unauthorized attempt to reject course for course_id')
        return jsonify({"error": "Only admins can reject courses"}), 403

    user_id = session['userId']
    user_type = session['userType']

    json_data = request.get_json()
    course_name = json_data.get("course_name")
    course_id = json_data.get("course_id")

    try:
        course = Course(user_id=user_id, course_id=course_id, course_name=course_name, user_type=user_type)
        rejection_status = course.reject_course()

        logger.info(f"Course rejected successfully for course_id: {course_id}")
        print(f"Course state updated successfully for course:{course_id}")
        return jsonify({"message": "Course rejected successfully"}), 200

    except Exception as e:
        logger.error(f"Error rejecting course with course_id: {course_id}: {str(e)}")
        return jsonify({"error": "Failed to reject course"}), 500

@app.route('/cancel_course', methods=['POST'])
def cancel_course(course_id):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info(f'Entering Cancel Course for course_id: {course_id}')
    print("Entering cancel course")

    if 'userId' not in session or session.get('userType') != 'admin':
        logger.warning(f'Unauthorized attempt to cancel course for course_id: {course_id}')
        return jsonify({"error": "Only teachers can cancel courses"}), 403

    user_id = session['userId']
    user_type = session['userType']

    json_data = request.get_json()
    course_name = json_data.get("course_name")
    course_id = json_data.get("course_id")

    try:
        course = Course(user_id=user_id, course_id=course_id, course_name=course_name, user_type=user_type)
        cancellation_status = course.cancel_course()

        logger.info(f"Course canceled successfully for course_id: {course_id}")
        return jsonify({"message": "Course canceled successfully"}), 200

    except Exception as e:
        logger.error(f"Error canceling course with course_id: {course_id}: {str(e)}")
        return jsonify({"error": "Failed to cancel course"}), 500

@app.route('/complete_course', methods=['POST'])
def complete_course(course_id):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info(f'Entering Complete Course for course_id: {course_id}')
    print("Entering complete course")

    if 'userId' not in session or session.get('userType') != 'admin':
        logger.warning(f'Unauthorized attempt to complete course for course_id: {course_id}')
        return jsonify({"error": "Only teachers can mark courses as completed"}), 403

    user_id = session['userId']
    user_type = session['userType']

    json_data = request.get_json()
    course_name = json_data.get("course_name")
    course_id = json_data.get("course_id")

    try:
        course = Course(user_id=user_id, course_id=course_id, course_name=course_name, user_type=user_type)
        completion_status = course.complete_course()

        logger.info(f"Course marked as completed for course_id: {course_id}")
        print(f"Course state updated successfully for course:{course_id}")
        return jsonify({"message": "Course marked as completed successfully"}), 200

    except Exception as e:
        logger.error(f"Error marking course as completed for course_id: {course_id}: {str(e)}")
        return jsonify({"error": "Failed to mark course as completed"}), 500

@app.post('/enroll_student')
def enroll_student():
    logging.basicConfig(filename='enrollments.log', encoding='utf-8', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Entering Enroll Student endpoint.')
    print("Entering Enroll Student endpoint.")

    print(session)
    student_id = session["userId"]

    if not student_id not in session:
        message = {"message": "Course ID and student id is required for enrollment."}
        logger.error(message)
        return jsonify(message), 400

    if not request.is_json:
        logger.error("Invalid request: Payload is not in JSON format.")
        return jsonify({"error": "Request payload must be in JSON format"}), 401

    json_data = request.get_json()
    course_id = json_data.get("course_id")

    try:
        enrollment = CourseEnrollment(course_id= course_id, student_id = student_id)
        enrollment_result = enrollment.enroll_student()

        logger.info(f"Student {student_id} successfully enrolled in course {course_id}.")
        print(f"Enrollment successful for student {student_id}.")
        return jsonify({"message": f"Student {student_id} enrolled successfully in course {course_id}."}), 201

    except DuplicateEnrollmentException as e:
        logger.error(f"Duplicate enrollment creation attempt for userId {student_id}: {e}")
        return jsonify({"error": "Student already exists"}), 409

    except PermissionDeniedException as e:
        logger.error(f"Permission denied: {e}")
        return jsonify({"error": str(e)}), 403

    except CourseNotFoundException as e:
        logger.error(f"Unexpected error during enrollment: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@app.post('/cancel_enrollment')
def cancel_enrollment():
    logging.basicConfig(filename='enrollments.log', encoding='utf-8', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Entering Cancel Enrollment endpoint.')
    print("Entering Cancel Enrollment endpoint.")

    student_id = session["userId"]

    if not request.is_json:
        logger.error("Invalid request: Payload is not in JSON format.")
        return jsonify({"error": "Request payload must be in JSON format"}), 400

    json_data = request.get_json()
    course_id = json_data.get("course_id")

    if not course_id:
        message = {"message": "Course ID is required for cancellation."}
        logger.error(message)
        return jsonify(message), 400

    if not student_id:
        logger.warning("User is not logged in or user type is invalid.")
        return jsonify({"error": "Please log in to cancel an enrollment."}), 403

    try:
        enrollment = CourseEnrollment(course_id= course_id, student_id = student_id)
        cancel_result = enrollment.cancel_enrollment_request()

        logger.info(f"Enrollment request for student {student_id} in course {course_id} canceled successfully.")
        print(f"Cancellation successful for student {student_id}.")
        return jsonify({"message": f"Enrollment for student {student_id} in course {course_id} canceled successfully."}), 200

    except CourseNotFoundException as e:
        logger.error(f"Unexpected error during cancellation: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post('/create_assignment')
def create_assignment():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info('Entering Create Course Assignment')
    print("Entering create course assignment")

    print(session)

    if 'userId' not in session:
        logger.warning('Unauthorized attempt to create course')
        return jsonify({"error": "Only teachers can create courses"}), 403

    teacher_id = session["userId"]

    if 'file' not in request.files:
        logger.warning('No file part in the request')
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        logger.warning('Empty file name in upload request')
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        logger.warning(f"Invalid file type for file: {file.filename}")
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    logger.info(f"File uploaded successfully: {file_path}")

    json_data = request.form.to_dict()
    course_id = json_data.get("course_id")
    assignment_name = json_data.get("assignment_name")
    file_type = json_data.get("file_type")
    uploaded_at = json_data.get("uploaded_at")
    status = json_data.get("status")

    logger.info(f"File uploaded successfully: {file_path}")

    print("Uploaded At:", uploaded_at)

    logger.debug("Assignment Name: %s", assignment_name)
    logger.debug("File Type: %s", file_type)
    logger.debug("File Path: %s", file_path)
    logger.debug("Upload Date: %s", uploaded_at)
    logger.debug("Status: %s", status)
    print(json_data)

    try:
        assignments = TeacherAssignments(assignment_name= assignment_name, file_type=file_type, file_path=file_path,uploaded_at=uploaded_at, status=status ,course_id = course_id,teacher_id= teacher_id)
        course_data = assignments.create_assignment()

        file_id = course_data.get("file_id")
        file_type = course_data.get("file_type")
        file_path = course_data.get("file_path")

        if not file_id and file_type:
            logger.error("Failed to retrieve file_id after assignment creation")
            return jsonify({"error": "Failed to upload assignment"}), 500

        session["file_id"] = file_id
        session["file_type"] = file_type
        session["file_path"] = file_path
        session.modified = True

        logger.info(f"Course assignment created for userId: with course_id and course_name: {file_id}, {file_type}")
        return jsonify({"message": "Course homework created successfully"}), 200

    except DuplicateAssignmentException as e:
        logger.error(f"Duplicate assignment creation attempt: {e.message}")
        return jsonify({"error": e.message}), 409

    except Exception as e:
        logger.error(f"Unexpected error during assignment creation: {str(e)}")
        return jsonify({"error": "Failed to create course assignment"}), 500

@app.post('/get_course_homework')
def get_course_homework():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_teacher_homework")

    print(session)

    json_data = request.get_json()
    course_id = json_data.get("course_id")
    print(course_id)

    try:
        work = TeacherAssignments(course_id=course_id)
        works = work.get_course_homework()

        logger.info(f"Homework fetched: {works}")
        if not works:
            logger.info(f"No works found for course_id {course_id}")
            return jsonify({"works": []}), 200

        logger.info(f"Successfully retrieved {len(works)} works for course_id {course_id}")
        return jsonify({"works": works}), 200

    except Exception as e:
        logger.error(f"Error fetching works for course_id {course_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve works"}), 500

@app.post('/get_student_homework')
def get_student_homework():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_teacher_homework")
    print(session)

    json_data = request.get_json()
    course_id = json_data.get("course_id")
    print(course_id)

    try:
        work = TeacherAssignments(course_id=course_id)
        works = work.get_student_homework()

        logger.info(f"Homework fetched: {works}")
        if not works:
            logger.info(f"No works found for course_id {course_id}")
            return jsonify({"works": []}), 200

        logger.info(f"Successfully retrieved {len(works)} works for course_id {course_id}")
        return jsonify({"works": works}), 200

    except Exception as e:
        logger.error(f"Error fetching works for course_id {course_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve works"}), 500

@app.get('/get_homework')
def get_homework():
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Entering get_homework route")
    print("Entering get all homework.")

    print(session)

    try:
        work = TeacherAssignments()
        homework = work.get_homework()

        if not homework:
            logger.info("No homework found in the database.")
            return jsonify({"homework": []}), 200

        logger.info(f"Successfully retrieved {len(homework)} homework.")
        return jsonify({"homework": homework}), 200

    except Exception as e:
        logger.error(f"Error fetching all courses: {str(e)}")
        return jsonify({"error": "Failed to retrieve homework"}), 500

@app.route('/assign_work', methods=['POST'])
def assign_work():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info(f'Entering Assign work for course_id')
    print("Entering assign homework")

    print(session)
    if not request.is_json:
        logger.warning('Invalid request format: not JSON')
        return jsonify({"error": "Request must be in JSON format"}), 400

    json_data = request.get_json()
    assignment_name = json_data.get("assignment_name")
    file_id = json_data.get("file_id")

    if not file_id or not assignment_name:
        logger.error("Missing course_name or course_id in request data")
        return jsonify({"error": "Missing course_name or course_id"}), 400

    try:
        work = TeacherAssignments(file_id=file_id)
        homework = work.assign_work()

        logger.info(f"Homework assigned successfully for: {file_id}")
        return jsonify({"message": f"Homework assigned successfully for: {file_id}"}), 200

    except Exception as e:
        logger.error(f"Error assigning homework: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.post('/submit_homework')
def submit_homework():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logger.info('Entering submit homework')
    print("Entering submit homework")

    print(session)

    if 'userId' not in session:
        logger.warning('Unauthorized attempt to create course')
        return jsonify({"error": "Only teachers can create courses"}), 403

    student_id = session["userId"]

    file = request.files['file']
    if file.filename == '':
        logger.warning('Empty file name in upload request')
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        logger.warning(f"Invalid file type for file: {file.filename}")
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    logger.info(f"File submitted successfully: {file_path}")

    json_data = request.form.to_dict()
    file_id = json_data.get("file_id")
    course_id = json_data.get("course_id")
    homework_name = json_data.get("homework_name")
    file_type = json_data.get("file_type")
    submitted_at = json_data.get("submitted_at")
    status = json_data.get("status")

    print("Submitted At:", submitted_at)

    logger.debug("File ID: %s", file_id)
    logger.debug("Homework Name: %s", homework_name)
    logger.debug("File Type: %s", file_type)
    logger.debug("Submit Date: %s", submitted_at)
    logger.debug("Status: %s", status)
    print(json_data)

    try:
        assignments = StudentHomework( file_id= file_id, homework_name= homework_name, file_type=file_type, file_path=file_path,submitted_at=submitted_at, status=status ,course_id = course_id,student_id= student_id)
        work_data = assignments.submit_homework()

        homework_id = work_data.get("homework_id")
        file_type = work_data.get("file_type")
        file_path = work_data.get("file_path")

        if not file_id and file_type:
            logger.error("Failed to retrieve file_id after assignment creation")
            return jsonify({"error": "Failed to upload assignment"}), 500

        session["homework_id"] = homework_id
        session["file_type"] = file_type
        session["file_path"] = file_path
        session.modified = True

        logger.info(f"Course assignment created for userId: with course_id and course_name: {file_id}, {file_type}")
        return jsonify({"message": "Course homework created successfully"}), 200

    except DuplicateAssignmentException as e:
        logger.error(f"Duplicate homework submission attempt: {e.message}")
        return jsonify({"error": e.message}), 409

    except Exception as e:
        logger.error(f"Unexpected error during homework submission: {str(e)}")
        return jsonify({"error": "Failed to submit homework"}), 500

@app.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found")

