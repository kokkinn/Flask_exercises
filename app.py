from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        f"""Task {self.id}"""


# @app.route('/')
# def index():
#     return render_template("index.html")


@app.route('/', methods=["POST", "GET"])
def tasks():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        db.session.add(new_task)
        db.session.commit()
        return redirect('/tasks')

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("tasks_list.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/tasks')


@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    print("AAA")
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        print("POST")
        task.content = request.form["content"]
        print(task.content)
        db.session.commit()
        return redirect('/tasks')

    else:
        return render_template("update.html", task=task)


if __name__ == '__main__':
    app.run(debug=True)
