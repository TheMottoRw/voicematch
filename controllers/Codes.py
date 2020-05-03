from models import Codes
from flask import Flask,jsonify
from datetime import datetime,timedelta
import sys, os
#sys.path.insert(0, os.path.abspath('..'))
from config import app,db
import json,random
def save(request):
    feed = 'ok'
    #code = Codes(codes=getRandomKey(),phone='0726183049',expiration=getExpirationTime(),activation_date = datetime.now(),status='verify',delete_status='0',regdate=datetime.now())
    code = Codes(code=request.values['code'],phone=request.values['phone'],expiration=request.values['expire'],status='verify',delete_status='0',activation_date=datetime.now(),regdate=datetime.now())
    db.session.add(code)
    db.session.commit()
    return feed

def get(request):
    arr = []
    count = 0
    #save(request)
    data = Codes.query.all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'phone':obj.phone,'codes':obj.codes,'expiration':obj.expiration,'status':obj.status,'activated_on':obj.activation_date,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)

def getById(id):
    arr = []
    count = 0
    data = Codes.query.filter_by(id=id).all()
    #print(json.dumps([dict(r) for r in dict.items()]))
    while(count < len(data)):
        obj = data[count]
        arr.append({'id':obj.id,'phone':obj.phone,'codes':obj.codes,'expiration':obj.expiration,'status':obj.status,'activated_on':obj.activation_date,'regdate':obj.regdate})
        count += 1
    return jsonify(arr)
def activate(request):
    feed = 'fail'
    code = Codes.query.filter(codes=request.values['code'])
    if(code != None):
        feed = 'ok'
        code.status='activated'
        db.session.commit()
    return feed

def getRandomKey():
	key=random.randint(1000,99999)
	if(Codes.query.filter_by(codes=str(key),status='pending').count()!=0):
		getRandomKey()
	return key

def getExpirationTime():
    return datetime.now() + timedelta(hours = 8)