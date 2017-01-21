import json
import time
import logging
from contextlib import closing
import http.client
import urllib.parse
import sys

class CreateProfielResponse:
    PROFILE_ID = 'verificationProfileId'
    
    def __init__(self, response):
        self.profile_id = response.get(self.PROFILE_ID, None)

    def get_profile_id(self):
        return self.profile_id

class verification_service:
    STATUS_OK = 200
    BASE_URI = 'westus.api.cognitive.microsoft.com'
    VERIFICATION_PROFILES_URI = '/spid/v1.0/verificationProfiles'
    VERIFICATION_URI = '/spid/v1.0/verify'
    SUBSCRIPTION_KEY_HEADER = 'Ocp-Apim-Subscription-Key'
    CONTENT_TYPE_HEADER = 'Content-Type'
    JSON_CONTENT_HEADER_VALUE = 'application/json'
    STREAM_CONTENT_HEADER_VALUE = 'application/octet-stream' 
    
    def __init__(self,subscription_key):
        self._subscription_key = subscription_key
    
    
    def create_profile(self,locale):
        try:
            body = json.dumps({'locale': '{0}'.format(locale)})
            res, message = self.send_request(
                'POST',
                self.BASE_URI,
                self.VERIFICATION_PROFILES_URI,
                self.JSON_CONTENT_HEADER_VALUE,
                body)
            if res.status == self.STATUS_OK:
                return CreateProfielResponse(json.loads(message))
            else:
                reason = res.reason if not message else message
                raise Exception('Error creating profile: ' + reason)
        except:
            logging.error('Error creating profile.')
            raise
            
            
    def send_request(self, method, base_url, request_url, content_type_value, body=None):
        try:
            headers = {self.CONTENT_TYPE_HEADER: content_type_value,
                       self.SUBSCRIPTION_KEY_HEADER: self._subscription_key}

            with closing(http.client.HTTPSConnection(base_url)) as conn:
                conn.request(method, request_url, body, headers)
                res = conn.getresponse()
                message = res.read().decode('utf-8')
                return res, message
        except:
            logging.error('Error sending the request.')
            raise
    def enroll_profile(self, profile_id, file_path):
        """Enrolls a profile using an audio file and returns a
        dictionary of the enrollment response.
        Arguments:
        profile_id -- the profile ID string of the user to enroll
        file_path -- the file path string of the audio file to use
        """
        try:
            # Prepare the request
            request_url = '{0}/{1}/enroll'.format(
                self._VERIFICATION_PROFILES_URI,
                urllib.parse.quote(profile_id))


            # Prepare the body of the message
            with open(file_path, 'rb') as body:
                # Send the request
                res, message = self._send_request(
                    'POST',
                    self._BASE_URI,
                    request_url,
                    self._STREAM_CONTENT_HEADER_VALUE,
                    body)
            if res.status == self._STATUS_OK:
                # Parse the response body
                return EnrollmentResponse.EnrollmentResponse(json.loads(message))
            else:
                reason = res.reason if not message else message
                raise Exception('Error enrolling profile: ' + reason)
        except:
            logging.error('Error enrolling profile.')
            raise

        

def create_profile(subscription_key,locale):
    helper = verification_service(subscription_key)
    creation_response = helper.create_profile(locale)
    print('Profile ID = {0}'.format(creation_response.get_profile_id()))

subscription_key = "53feafe087b54819a3bfe1a76d112077"
create_profile(subscription_key,'en-us')
