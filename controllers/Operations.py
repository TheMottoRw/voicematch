from models import Operations,Suspects
from flask import Flask,jsonify
from datetime import datetime,timedelta
import sys, os
from ms_api import ProcessVoices
#sys.path.insert(0, os.path.abspath('..'))
from config import app,db
import json,random
def save(obj):
    feed = 'ok'
    #code = Operations(suspects_reference='2',opcodes='XDF8-DF-XVD',description='Match suspect',status='verify',activation_date=datetime.now(),regdate=datetime.now())
    code = Operations(suspects_reference=obj['suspect'],verification_message_id=obj['message_id'],verification_message_sender=obj['sender'],opcodes=obj['opcode'],description=obj['description'],result='',status='pending',delete_status='0',activation_date=datetime.now(),regdate=datetime.now())
    db.session.add(code)
    db.session.commit()
    return feed

def get(request):
    arr = []
    count = 0
    #save(request)
    data = Operations.query.all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'suspect':obj.suspects_reference,'opcodes':obj.opcodes,'description':obj.description,'status':obj.status,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)

def getById(id):
    arr = []
    count = 0
    data = Operations.query.filter_by(id=id).all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'suspect':obj.suspects_reference,'opcodes':obj.opcodes,'description':obj.description,'status':obj.status,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)


def getEnrollmentOperationStatus():
    arr = []
    count = 0
    voicesObj = ProcessVoices.ProcessVoice()
    data = Operations.query.filter_by(description='Enrollment',status='pending')
    while(count<data.count()):
        opId = getOperationIdFromUrl(data[count].opcodes)
        result = voicesObj.getOperations(opId)

        opObj = Operations.query.get_or_404(data[count].id)
        suspectObj = Suspects.query.get(data[count].suspects_reference)
        opObj.result = str(result)
        if("processingResult" in result):
            if(result['processingResult'] == None):#it still being processed
                opObj.status = result['status']
            else:#has been processed
                opObj.status = result['processingResult']['enrollmentStatus']
                suspectObj.status = result['processingResult']['enrollmentStatus']

        else:
            opObj.status = result['status']
        count += 1
        
        db.session.commit()

def getIdentificationOperationStatus():
    count = 0
    data = Operations.query.filter_by(description='Identification',status='pending')
    voiceObj = ProcessVoices.ProcessVoice()
    while(count<data.count()):
        opId = getOperationIdFromUrl(data[count].opcodes)
        result = voiceObj.getOperations(opId)
        if("error" not in result):
            print("Obj ops "+str(data[count]))
            suspectObj = Suspects.query.get(data[count].suspects_reference)
            opObj = Operations.query.get(data[count].id)
            opObj.result = str(result)
            if(result['processingResult'] != None):#processing completed
                if(result['processingResult']['identifiedProfileId'] == suspectObj.profile_id):
                    opObj.status = 'matches'
                    #notify status to notification email and phone
                    #sendSms(suspectObj.notification_phone,"Suspect traced")
                    #sendEmail(suspectObj.notification_email,"Suspect traced","we notice you that we've found suspect for more info")
                else:
                    opObj.status = 'not match'
            else:#still being processed
                opObj.status = result['status']
                
            db.session.commit()
        count += 1

def getOperationIdFromUrl(url):
    opUrlArr = url.split("/")
    return opUrlArr[-1]

def sendSms(phone,sms):
    url = 'http://egtecs.com:8787/api/v2/sendSms/?number=' + \
        phone+'&message='+sms
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8',
               'User-Agent': 'Mozilla/5.1', 'Authorization': Optional.base64_encode("0784634118:Roger@@2709")}
    r = requests.get(url, headers=headers)
    print(r)
    return r


def sendEmail(to, subject, message):
    feed = 'ok'
    # subject = subject # The subject line

    msg = MIMEMultipart()
    msg['Message-Id'] = str(random.random()*100000)
    msg['From'] = 'no-reply@imenye.rw'
    msg['FromName'] = 'Imenye Team'
    msg['To'] = to
    msg['Subject'] = "Imenye - remind you about your "+subject
    msg['Reply-To'] = "info@imenye.rw"
    msg['Host'] = "smtp.imenye.rw"
    msg['SMTPAuth'] = 'true'
    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'html'))
    textMessage = msg.as_string()  # convert object in text
    
    server = smtplib.SMTP('smtp.imenye.rw', 587)
    server.connect("smtp.imenye.rw", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # Next, log in to the server
    server.login("no-reply@imenye.rw", "Imenye@App")
    # Send the mail
    try:
        response=server.sendmail(msg['From'], msg['To'], textMessage)
        print(str(response))
    except:
        feed = 'fail'
    server.quit()
    return feed