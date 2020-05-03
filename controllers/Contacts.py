from models import Contacts
from flask import Flask,jsonify
from datetime import datetime
import sys, os
#sys.path.insert(0, os.path.abspath('..'))
from config import app,db
import json
def save(request):
    feed = 'ok'
    #contact = Contacts(phone='0726183049',name='Asua bufu',app_id='23232',status='verify',delete_status='0',regdate=datetime.now())
    contact = Contacts(phone=request.values['phone'],names=request.values['name'],status='verify',delete_status='0',regdate=datetime.now())
    db.session.add(contact)
    db.session.commit()
    return feed

def get(request):
    arr = []
    count = 0
    data = Contacts.query.all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'phone':obj.phone,'name':obj.name,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)

def getById(id):
    arr = []
    count = 0
    data = Contacts.query.filter_by(id=id).all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'phone':obj.phone,'name':obj.name,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)
def update(request,id):
    feed = 'ok'
    contact = Contacts.query.get(id=id)
    contact.phone=request.values['phone']
    contact.name=request.values['name']
    db.session.commit()
    return feed

def delete(id):
    feed = 'ok'
    contact = Contacts.query.get(id=id)
    db.session.delete(contact)
    return feed