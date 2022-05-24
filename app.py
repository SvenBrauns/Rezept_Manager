from flask import Flask, redirect, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

""" class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    ingredient = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id """

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name= db.Column(db.String(200), nullable=False)
    cook_time = db.Column(db.String(200), nullable=False)
    ingredients = db.relationship('Ingredients', backref='recipe', lazy=True)

    """ def __repr__(self):
        return '<Recipe %r>' % self.id """

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    name= db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Float, primary_key=False)
    unit = db.Column(db.String(200), nullable=False)

    """ def __repr__(self) -> str:
        return '<Ingredients %r>' % self.id """   

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_ingredient = request.form['ingredient']
        task_name = request.form['name']
        new_task = Todo(content=task_content, ingredient=task_ingredient, name=task_name)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        task_content = request.form['content']
        task_ingredient = request.form['ingredient']
        task_name = request.form['name']
        new_task = Todo(content=task_content, ingredient=task_ingredient, name=task_name)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/test')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('test.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.ingredient = request.form['ingredient']
        task.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)