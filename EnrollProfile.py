from SpeakerCreation import verification_service as vs
import sys
import speech_recognition as sr

def enroll_profile(subscription_key, profile_id, file_path):
    helper = vs(subscription_key)

    enrollment_response = helper.enroll_profile(profile_id, file_path)

    print('Enrollments Completed = {0}'.format(enrollment_response.get_enrollments_count()))
    print('Remaining Enrollments = {0}'.format(enrollment_response.get_remaining_enrollments()))
    print('Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status()))
    print('Enrollment Phrase = {0}'.format(enrollment_response.get_enrollment_phrase()))

if __name__ == "__main__":
    subscription_key = "53feafe087b54819a3bfe1a76d112077"
    profile_id = "13b95c66-76d6-4dd7-b599-d46b2636974b"
    enroll_profile(subscription_key,profile_id,"audio.wav")
