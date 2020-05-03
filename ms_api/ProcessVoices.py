import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
class ProcessVoice:
    key = ''
    
    def __init__(self):
        self.key = '4e00a40f10bc4d588c17823ec3f50d70'
    
    def getOperations(self,operationId):#returned in response header Operation-Location of identify 
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("GET", "/spid/v1.0/operations/"+operationId+"?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = json.loads(response.read())

            print("Ops status "+str(data))
            return data
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def identify(self,profileId,file):

        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            #'shortAudio': '{boolean}',
            'shortAudio': file,
        })

        try:
            conn = http.client.HTTPSConnection('voicematch.cognitiveservices.azure.com')
            conn.request("POST", "/spid/v1.0/identify?identificationProfileIds="+profileId+"&%s" % params, file, headers)
            response = conn.getresponse()
            #data = json.loads(response.read())
            print("Voice identify "+str(response.read()))
            if(response.status != 202):#error occurred return error
                return 'error'
            conn.close()
            return response.headers['Operation-Location']
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
