from flask_sqlalchemy import SQLAlchemy
from config import app,db
from datetime import datetime
#migration and management
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://super:super@localhost/voicematch'

#migration commands
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Contacts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    phone = db.Column(db.String(15), nullable = False)
    name = db.Column(db.String(50), nullable = False)
    app_id = db.Column(db.String(30), nullable = False)
    status = db.Column(db.String(15), nullable = False)
    delete_status = db.Column(db.String(15), nullable = False, default = '0')
    regdate = db.Column(db.DateTime, nullable = False, default = datetime.utcnow()) 

    def __repr__(self):
        return "Contact id "+str(self.id)

class Messages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sender = db.Column(db.Integer,nullable = False)
    voice = db.Column(db.Text, nullable = False)
    caption = db.Column(db.String(60), nullable = False)
    receiver = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(15), nullable = False)
    delete_status = db.Column(db.String(15), nullable = False, default = '0')
    receive_delete_status = db.Column(db.String(15), nullable = False, default = '0')
    read_date = db.Column(db.DateTime, default=datetime.utcnow())
    regdate = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())

    def __repr__(self):
        return "Message id "+str(self.id)

class Suspects(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    institution = db.Column(db.String(60), nullable = False)
    notification_phone = db.Column(db.String(15), nullable = False)
    notification_email = db.Column(db.String(60),nullable=False)
    names = db.Column(db.String(60), nullable = False)
    profile_id = db.Column(db.String(60), nullable = False)
    voices = db.Column(db.Text, nullable = False)
    status = db.Column(db.String(15), nullable = False)
    delete_status = db.Column(db.String(15), nullable = False, default = '0')
    last_message_id = db.Column(db.Integer)
    last_trace_date = db.Column(db.DateTime, default = datetime.now())
    regdate = db.Column(db.DateTime, nullable = False, default = datetime.now())

    def __repr__(self):
        return "Suspect id "+str(self.id)


class Codes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    codes = db.Column(db.String(60), nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    expiration = db.Column(db.DateTime,nullable=True)
    status = db.Column(db.String(15), nullable = False)
    delete_status = db.Column(db.String(5), nullable = False, default = '0')
    activation_date = db.Column(db.DateTime, nullable = True)
    regdate = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())

    def __repr__(self):
        return "Verification code id "+str(self.id)

class Operations(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    suspects_reference = db.Column(db.Integer)
    verification_message_id = db.Column(db.Integer)
    verification_message_sender = db.Column(db.Integer)
    opcodes = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(160), nullable = False)
    result = db.Column(db.String(500), nullable = False)
    status = db.Column(db.String(15), nullable = False)
    delete_status = db.Column(db.String(5), nullable = False, default = '0')
    activation_date = db.Column(db.DateTime, nullable = True)
    regdate = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())

    def __repr__(self):
        return "Operation id "+str(self.id)

if __name__ == '__main__':
    manager.run()