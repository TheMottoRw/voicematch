from models import Suspects
from flask import Flask,jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
from ms_api import ProcessVoices,Profiles
from controllers import Operations
import sys, os
#sys.path.insert(0, os.path.abspath('..'))
from config import app,db

import json

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
audioFile = ''
audioAttach = ''
file = ''
def save(request):
    feed = 'ok'
    # audioFile = request.files['voices']
    #suspect = Suspects(institution='RIB Rwanda',notification_phone='0726183049',notification_email='notify@rib.rw',names='Kabaka Jay',voices='sound1,sound2',status='pending')
    upload_file(request)
    
    filename = secure_filename(request.files['voices'].filename)
    audioFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audioAttach =  open(audioFile,'rb')

    suspect = Suspects(institution=request.values['institution'],notification_phone=request.values['phone'],notification_email=request.values['email'],names=request.values['names'],profile_id='',voices=audioFile,status='pending',delete_status='0',last_trace_date=datetime.now(),regdate=datetime.now())
    db.session.add(suspect)
    db.session.commit()
    #generate suspect profile identification ID
    profileObj = Profiles.Profile()
    profileId = profileObj.create()
    #After getting profile ID assign suspect ID
    lastInsertid = suspect.id
    #suspectObj = Suspects.query.get(id=lastInsertid)
    suspect.profile_id = profileId
    db.session.commit()
    #enroll with his/her voices
    enrollmentOperationLink = profileObj.enroll(profileId, audioAttach)
    if(enrollmentOperationLink != 'error'):#returned operation linkn header
        opStatus = Operations.save({'suspect':lastInsertid,'message_id':0,'sender':0,'opcode':enrollmentOperationLink,'description':'Enrollment'})
        #get operation status
        Operations.getEnrollmentOperationStatus()
        #save operation check after certain amount of time
    #End API endpoints calling
    return feed

def tracePendingSuspect(sender,message_id,audio_file):
    arr = []
    count = 0
    data = Suspects.query.filter_by(status='Enrolled')
    while(count < data.count()):
        trace(data[count].id,data[count].profile_id,sender,message_id,audio_file)
        count +=1


def trace(suspectId,profileId,sender,message_id,audio_file):
    voiceObj = ProcessVoices.ProcessVoice()
    audioFile = open(audio_file,'rb')
    identificationLink = voiceObj.identify(profileId, audioFile)
    opStatus = Operations.save({'suspect':suspectId,'message_id':message_id,'sender':sender,'opcode':identificationLink,'description':'Identification'})
    #get operation status,
    Operations.getIdentificationOperationStatus()



def get(request):
    arr = []
    count = 0
    #save(request)
    data = Suspects.query.all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'institution':obj.institution,'notif_phone':obj.notification_phone,'notif_email':obj.notification_email,'names':obj.names,'voices':obj.voices,'status':obj.status,'last_trace_date':obj.last_trace_date,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)

def getById(id):
    arr = []
    count = 0
    data = Suspects.query.filter_by(id=id).all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'institution':obj.institution,'notif_phone':obj.notification_phone,'notif_email':obj.notification_email,'names':obj.names,'voices':obj.voices,'status':obj.status,'last_trace_date':obj.last_trace_date,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)


def delete(id):
    feed = 'ok'
    suspect = Suspects.query.get(id=id)
    suspect.delete_status = '1'
    db.session.commit()
    return feed

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(request):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'voices' not in request.files:
            return 'Parameter file missing in request'
        file = request.files['voices']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No file selected'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            audioFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("File path joined "+os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'ok'