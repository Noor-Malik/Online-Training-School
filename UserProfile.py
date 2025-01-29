import logging
from DBUserProfile import DBUserProfile
from OTExceptions import DuplicateProfileException, InvalidProfileDataException

class UserProfile:
    def __init__(self, user_id=None, name=None, age=None, address=None, phone_number=None, userprofileId=None):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.address = address
        self.phone_number = phone_number
        self.userprofileId = userprofileId

    def is_valid(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Checking profile data is valid for user_id: {self.user_id}")

        if not all([self.name, self.age, self.address, self.phone_number]):
            logger.error("Invalid profile data: Missing required fields")
            return False
        return True

    def save(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Saving profile data for user_id: {self.user_id}")
        print("Entering Save Profile")

        if not self.is_valid():
            raise InvalidProfileDataException("All profile fields (user_id, name, age, address, phone number) are required.")

        try:
            user_profile = DBUserProfile()
            profile_id = user_profile.insert_profile(self.user_id, self.name, self.age, self.address, self.phone_number)
            logger.info(f"Profile saved for user_id: {self.user_id}")
            return profile_id
        except DuplicateProfileException as e:
            logger.error(f"Duplicate profile: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Error saving profile: {str(e)}")
            raise e

    def updateProfile(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
        logger.info(f"Updating profile for user_id: {self.user_id}")
        print(f"UserProfile: Updating profile for user_id: {self.user_id}")

        if not self.is_valid():
            raise InvalidProfileDataException("All profile fields (user_id, name, age, address, phone number, userprofileId) are required.")

        try:
            db_user_profile = DBUserProfile()
            print("UserProfile: Calling DBUserProfile to update profile")
            profile_id = db_user_profile.update_profile(self.user_id, self.name, self.age, self.address, self.phone_number, self.userprofileId)

            if profile_id:
                print(f"UserProfile: Profile updated successfully for user_id: {self.user_id}")
                logger.info(f"Profile updated successfully for user_id: {self.user_id}")
            else:
                print(f"UserProfile: No profile found for user_id: {self.user_id}, update failed.")
                logger.warning(f"No profile found for user_id: {self.user_id}, update failed.")
            return profile_id

        except DuplicateProfileException as e:
            print(f"Duplicate profile detected: {e.message}")
            logger.error(f"Duplicate profile detected: {e.message}")
            raise e
        except Exception as e:
            print(f"Error updating profile for user_id {self.user_id}: {str(e)}")
            logger.error(f"Error updating profile for user_id {self.user_id}: {str(e)}")
            raise e


# Test: create_profile
# profile = UserProfile(177, "noor", 35, "lahore", "325654445")
# profile.save()

# # Test: update_profile
# profile = UserProfile(177, "noor", 37, "lahori", 567895675678, 11)
# profile.updateProfile()

