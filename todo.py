from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/lesia/Desktop/ToDoApp/todo.db'
db = SQLAlchemy(app)

# home page
@app.route("/")
def index():
    todos = Table.query.all()
    return render_template("index.html", todos = todos)

# add 
@app.route("/add", methods=["POST"])
def addToDo():
    title = request.form.get("title")
    content = request.form.get("content")

    table = Table(title=title, content=content, complete=False)

    db.session.add(table)
    db.session.commit()
    return redirect(url_for("index"))

# delete
@app.route("/delete/<string:id>")
def deleteToDo(id):
    todo = Table.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

# complete status
@app.route("/update/<string:id>", methods = ["GET"])
def completeToDo(id):
    todo = Table.query.filter_by(id=id).first()
    if(todo.complete == False):
        todo.complete = True
    else:
        todo.complete = False
    
    db.session.commit()
    return redirect(url_for("index"))

# database
class Table(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    app.run(debug=True)
