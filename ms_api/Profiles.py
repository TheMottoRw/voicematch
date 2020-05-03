import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
class Profile:
    key = ''
    
    def __init__(self):
        self.key = '4e00a40f10bc4d588c17823ec3f50d70'
    
    def enroll(self,profileId,file):
        headers = {
        # Request headers
        'Content-Type': 'multipart/form-data',
        'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            #'shortAudio': '{boolean}',
            'shortAudio': True,
        })

        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/spid/v1.0/identificationProfiles/"+profileId+"/enroll?%s" % params, file, headers)
            response = conn.getresponse()
            data = response.read()
            print("Enrollement response ",data)
            print(str(response.status)+"- "+response.headers['Operation-Location'])
            if(response.status == 202):
                return response.headers['Operation-Location']
            else:#error occurred return error
                return 'error'
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def create(self):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.key,
            "Accept-Language": "en-US"            
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % params, "{locale:'en-US'}", headers)
            response = conn.getresponse()
            data = json.loads(response.read())
            profId = data['identificationProfileId']
            #data = response.read()
            print(data)
            return profId
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def get(self):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('https://voicematch.cognitiveservices.azure.com')
            conn.request("GET", "/spid/v1.0/identificationProfiles?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def getById(self,profileId):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
            }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('https://voicematch.cognitiveservices.azure.com')
            conn.request("GET", "/spid/v1.0/identificationProfiles/"+profileId+"?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def delete(self,profileId):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
            }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('https://voicematch.cognitiveservices.azure.com')
            conn.request("DELETE", "/spid/v1.0/identificationProfiles/"+profileId+"?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def reset(self,profileId):

        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('https://voicematch.cognitiveservices.azure.com')
            conn.request("POST", "/spid/v1.0/identificationProfiles/"+profileId+"/reset?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))