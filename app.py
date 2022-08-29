from crypt import methods
from flask import Flask, redirect, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from models.Todo import Todo
from markupsafe import escape


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
app.config["SECRET_KEY"] = "absj1kn1j2n32k3k23knjkan212kl"
db = SQLAlchemy(app)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        todo_item = request.form['item']
        newTodo = Todo(content = todo_item)

        try:
            db.session.add(newTodo)
            db.session.commit()
            return redirect('/')
        except:
            return "Couldn't create todo"
    else:
        todos = db.session.query(Todo).all()

        return render_template("todo.html", todos = todos)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.find_filter(id=id).first()
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that task'


