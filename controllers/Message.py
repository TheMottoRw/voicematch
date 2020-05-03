from models import Messages
from flask import Flask,jsonify
from datetime import datetime
import sys, os
#sys.path.insert(0, os.path.abspath('..'))
from config import app,db
from ms_api import ProcessVoices
from controllers import Suspects

import json

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def save(request):
    feed = 'ok'
    audioFile = os.path.join(app.config['UPLOAD_FOLDER'], request.files['voices'].filename)
    Suspects.upload_file(request)
    #message = Messages(sender='1',voice='audio file',caption='greeting from bufu',receiver='2',status='pending')
    message = Messages(sender=request.values['sender'],voice=audioFile,caption=request.values['caption'],receiver=request.values['receiver'],status='pending',delete_status='0',read_date=datetime.now(),regdate=datetime.now())
    db.session.add(message)
    db.session.commit()
    #verify voices if it match any suspect
    Suspects.tracePendingSuspect(request.values['sender'],message.id,audioFile)
    #get operation status set delay of 1min to verifly operation status
    return feed

def get(request):
    arr = []
    count = 0
    data = Messages.query.all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'sender':obj.sender,'voice':obj.voice,'caption':obj.caption,'receiver':obj.receiver,'read_date':obj.read_date,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)

def getById(id):
    arr = []
    count = 0
    data = Messages.query.filter_by(id=id).all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'sender':obj.sender,'voice':obj.voice,'caption':obj.caption,'receiver':obj.receiver,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)

def delete(id):
    feed = 'ok'
    contact = Contacts.query.get(receiver=Contacts.query.get(id))
    db.session.commit()
    return feed


def deleteForReceiver(id):
    feed = 'ok'
    contact = Messages.query.get(receiver=Contacts.query.get(id))
    contact.receiver_delete_status = '2'
    db.session.commit()
    return feed