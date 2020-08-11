from flask import Flask, render_template , abort , request , jsonify , redirect , url_for
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:InnovativeThinkers@database-2.c7bwl5u5cyjg.ap-south-1.rds.amazonaws.com:5432/todo_app'
db = SQLAlchemy(app)
migrate = Migrate(app , db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean() , nullable=False , default=False)
  list_id = db.Column(db.Integer , db.ForeignKey('todolists.id') , nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model):
  __tablename__ = 'todolists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String() , nullable=False)
  todos = db.relationship('Todo' , backref='list' , lazy=True)

# db.create_all()

@app.route('/todos/delete-task' , methods=['POST'])
def delete_task_todo():
  error = False
  body = {}
  try:
    todo_id = request.get_json()['id']
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
    body['id'] = todo_id
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)
    


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    print("hi!!!!!!!!!!!!'")
    data = request.get_json()
    print(data)
    description = data['description']
    list_name = data['name']
    list_id = 0
    list = TodoList.query.all()
    for item in list:
      if item.name==list_name:
        list_id = item.id
    todo = Todo(description=description , list_id=list_id)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
  return render_template('index.html',
  lists = TodoList.query.all() ,
  active_list = TodoList.query.get(list_id),
  todos = Todo.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/')
def index():
  return redirect(url_for('get_list_todos' , list_id=1))

@app.route('/todos/create-list' , methods=['POST'])
def create_list():
  error=False
  body={}
  try:
    name = request.get_json()['name']
    todolist = TodoList(name=name)
    db.session.add(todolist)
    db.session.commit()
    body['name']=todolist.name
  except:
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

if __name__ == '__main__':
    app.run()