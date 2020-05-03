from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
#sqlite_configs app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)



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

@app.route("/greet/<string:name>")
def greet(name):
    return "Hello, " + name

@app.route("/load/<int:id>")
def getById(id):
    return "Data with id "+str(id)

@app.route("/method",methods = ['GET', 'POST'])
def onlyMethod():
    return "Only specific methods"
    
@app.route("/render")
def renderPage():
    return render_template('home.html')
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