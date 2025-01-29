from Course import Course
from DBCourse import DBCourse
from OTExceptions import CourseNotFoundException

#DB Course Testers

#get_course test
# dbCousre = DBCourse()
# course_record = dbCousre.get_course(18)
# print(course_record)

# dbCousre = DBCourse()
# course_record = dbCousre.get_courses_by_state(178,"OPEN")
# print(course_record)

# dbCousre = DBCourse()
# course_record = dbCousre.get_all_courses()
# print(course_record)

# dbCousre = DBCourse()
# course_record = dbCousre.get_teacher_courses(178)
# print(course_record)

#create_course test
# dbCousre = DBCourse()
# course_record = dbCousre.create("Programmiz", "test details3", "3 weeks", "2024,11,30", "2025,3,30", 10, "REQUEST_FOR_APPROVAL",2)
# print(course_record)

#update_course test
# dbCousre = DBCourse()
# course_record = dbCousre.update("test3", "test details3", "3 weeks", "2024,11,30", "2025,3,30", 10, 18,"OPEN",174)
# print(course_record)

#approve_course test
# dbCousre = DBCourse()
# course_record = dbCousre.approve(20)
# print(course_record)

# Test: exists
# dbCousre = DBCourse()
# course_exists = dbCousre.exists("test_course", 2)
# print(f"Course exists: {course_exists}")

# Test: change_status_to_active
# dbCousre = DBCourse()
# active_result = dbCousre.change_status_to_active(24)
# print(f"Change to ACTIVE result: {active_result}")

# Test: reject_course_in_db
# dbCousre = DBCourse()
# reject_result = dbCousre.reject_course_in_db(28)
# print(f"Reject course result: {reject_result}")

# Test: cancel_course_in_db
# dbCousre = DBCourse()
# cancel_result = dbCousre.cancel_course_in_db(28)
# print(f"Cancel course result: {cancel_result}")

# Test: complete_course_in_db
# dbCousre = DBCourse()
# complete_result = dbCousre.complete_course_in_db(28)
# print(f"Complete course result: {complete_result}")

# Test: select_course
# dbCousre = DBCourse()
# selected_course = dbCousre.select_course(28)
# print(f"Selected course details: {selected_course}")


# Course Testers

# cousre = Course(user_id=178)
# course_record = cousre.get_teacher_courses()
# print(course_record)

#update_course test
# course  = Course("test course2", "test details2", "3 weeks", "2024,11,30", "2025,3,30", 10, 18,2)
# course.update_course()

# Test: is_valid
# course = Course("Test Course", "Some details", "4 weeks", "2024-12-01", "2025-01-01", 15)
# is_valid = course.is_valid()
# print(f"Course is valid: {is_valid}")

# Test: create_course
# course = Course("Test Course", "Some details", "4 weeks", "2024-12-01", "2025-01-01", 15, 2)
# course.create_course()

# Test: get_course_detail
# course = Course(course_id=18)
# course_details = course.get_course_detail()
# print(f"Course details: {course_details}")

# Test: update_course
# course = Course(course_name="Updated Test Course",course_details="Updated details",duration="6 weeks",start_date="2024-11-01",end_date="2025-02-01",available_seats=20,course_id=18,user_id=2)
# course.update_course()
# print("Course updated successfully.")

# Test: approve_course
# course = Course(course_id=28, user_id=1)
# course.user_type = "ADMIN"
# approval_result = course.approve_course(28)
# print(f"Approval result: {approval_result}")

# Test: change_status_to_active
# course = Course(course_id=23, user_id=2)
# course.user_type = "TEACHER"
# active_result = course.change_status_to_active(23)
# print(f"Change to ACTIVE result: {active_result}")

# # Test: reject_course
# course = Course(course_id=24, user_id=2)
# course.user_type = "ADMIN"
# reject_result = course.reject_course(24)
# print(f"Reject course result: {reject_result}")

# Test: cancel_course
# course = Course(course_id=28, user_id=1)
# course.user_type = "ADMIN"
# cancel_result = course.cancel_course(24)
# print(f"Cancel course result: {cancel_result}")

# Test: complete_course
# course = Course(course_id=28, user_id=1)
# course.user_type = "ADMIN"
# complete_result = course.complete_course(24)
# print(f"Complete course result: {complete_result}")

# cousre = Course()
# course_record = cousre.get_all_courses()
# print(course_record)