from flask import Flask , render_template, url_for, request
from flask.templating import render_template_string 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.datastructures import RequestCacheControl
from werkzeug.utils import redirect 
app = Flask(__name__)

#intializing database
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#create model

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return super().__repr__() 

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there was problem in adding your task "
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',  tasks = tasks)
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try :
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was problem in deleting'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):

    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
           db.session.commit()
           return redirect('/')
        except:
           return 'issue update'

    else:
        return render_template('update.html', task =task)
if __name__ == "__main__":
    app.run(debug=True)
