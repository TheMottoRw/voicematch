from flask import render_template,request,redirect
from config import app,db
from datetime import datetime
from controllers import Contacts,Message,Suspects,Codes,Operations


'''class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    regdate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow())
    
    def __init__(self,title,message):
        self.title = title
        self.message = message

    def __repr__(self):
        return "Post id "+str(self.id)
'''
contents = [
    {
        'title':'Good',
        'message':'Hello, how are you doing dear?'
    }
]

@app.route("/")
def hello():
    return "Hello Flask developer asua "+str(request.headers['Host'])

@app.route("/contacts", methods = ['GET', 'POST'])
def contacts():
    feed = ''
    if(request.method == 'POST'):
        feed = Contacts.save(request)
    else:
        feed = Contacts.get(request)
    return feed

@app.route("/contact/<int:id>",methods = ['GET','POST','PUT'])
def contact(id):
    feed = ''
    method = request.method
    if(method == 'POST'):
        feed = Contacts.update(request,id)
    else:
        if(method == 'PUT'):
            feed = Contacts.delete(id)
        else:
            feed = Contacts.getById(id)
    return feed

@app.route("/chats", methods = ['GET', 'POST'])
def chats():
    feed = ''
    if(request.method == 'POST'):
        feed = Message.save(request)
    else:
        feed = Message.get(request)
    return feed

@app.route("/chat/<int:id>",methods = ['GET','PUT'])
def chat(id):
    feed = ''
    method = request.method
    if(method == 'PUT'):
        feed = Message.delete(id)
    else:
        feed = Message.getById(id)
    return feed

@app.route("/suspects", methods = ['GET', 'POST'])
def suspects():
    feed = ''
    if(request.method == 'POST'):
        feed = Suspects.save(request)
    else:
        feed = Suspects.get(request)
    return feed

@app.route("/suspect/<int:id>",methods = ['GET','PUT'])
def suspect(id):
    feed = ''
    method = request.method
    if(method == 'PUT'):
        feed = Suspects.delete(id)
    else:
        feed = Suspects.getById(id)
    return feed

@app.route("/codes", methods = ['GET', 'POST'])
def codes():
    feed = ''
    if(request.method == 'POST'):
        feed = Codes.save(request)
    else:
        feed = Codes.get(request)
    return feed

@app.route("/code/<int:id>",methods = ['GET','PUT'])
def code(id):
    feed = ''
    method = request.method
    if(method == 'PUT'):
        feed = Codes.delete(id)
    else:
        feed = Codes.getById(id)
    return feed

@app.route("/operations", methods = ['GET', 'POST'])
def operations():
    feed = ''
    if(request.method == 'POST'):
        feed = Operations.save(request)
    else:
        feed = Operations.get(request)
    return feed

@app.route("/operation/<int:id>",methods = ['GET','PUT'])
def operation(id):
    feed = ''
    method = request.method
    if(method == 'PUT'):
        feed = Operations.delete(id)
    else:
        feed = Operations.getById(id)
    return feed


@app.route("/upload",methods = ['POST'])
def voiceUpload():
    feed = 'ok'
    feed = Suspects.upload_file(request)
    return feed

@app.route("/posts", methods = ['GET','POST'])
def posts():
    if(request.method == 'POST'):
        data = Posts(title=request.form['title'],message = request.form['message'])
        db.session.add(data)
        db.session.commit()
    contents = Posts.query.all()
    return render_template('posts.html',posts = contents)

@app.route("/posts/<int:id>", methods = ['GET','POST'])
def edit(id):
    inst = Posts.query.get_or_404(id)
    if(request.method == 'POST'):
        inst.title = request.form['title']
        inst.message = request.form['message']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("edit.html",post = inst)

@app.route("/posts/delete/<int:id>",methods = ['GET'])
def delete(id):
    data = Posts.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect("/posts")


if __name__ == "__main__":
    app.run(debug = True)
    #migrate manager command replaced app