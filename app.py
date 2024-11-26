from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# create app
app = Flask(__name__)

#create configuration for db, /// after sqlite means its relative path, //// means absolute path
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///taskmaster.db'

# initialize db
db =SQLAlchemy()
db.init_app(app)

# create the data model for tasks
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # create representation for the db object 
    def __repr__(self):
        return '(task %r)' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content=request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return 'error while adding task',500
        return redirect('/')
    else:
        tasks=Todo.query.order_by('date_created').all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'delete failed for the task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        new_content = request.form['content']
        task.content = new_content
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was error updating the task'
    else:
        return render_template('update.html', task=task)
if __name__ == '__main__':
    app.run(debug=True, port=5003)
    # db.create_all()

