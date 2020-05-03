import http.client, urllib.request, urllib.parse, urllib.error, base64

class Verification:
    
    def __init__(self):
        self.key = '4e00a40f10bc4d588c17823ec3f50d70'

    def create(self):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("POST", "/spid/v1.0/verificationProfiles?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def enroll(self):
        headers = {
            # Request headers
            'Content-Type': 'multipart/form-data',
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("POST", "/spid/v1.0/verificationProfiles/{verificationProfileId}/enroll?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


    def getPhrases(self):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("GET", "/spid/v1.0/verificationPhrases?locale={locale}&%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def get(self):#get all profiles
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("GET", "/spid/v1.0/verificationProfiles?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def getById(self):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("GET", "/spid/v1.0/verificationProfiles/{verificationProfileId}?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def delete(self):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("DELETE", "/spid/v1.0/verificationProfiles/{verificationProfileId}?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def reset(self):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("POST", "/spid/v1.0/verificationProfiles/{verificationProfileId}/reset?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
