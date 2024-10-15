from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    if not os.path.exists('todo.db'):
        db.create_all()

@app.route('/')
def index():
    todo_items = TodoItem.query.all()
    total_tasks = len(todo_items)
    completed_tasks = sum(item.completed for item in todo_items)
    return render_template('index.html', todo_items=todo_items, completed_tasks=completed_tasks, total_tasks=total_tasks)

@app.route('/add', methods=['POST'])
def add_todo():
    new_item = TodoItem(content=request.form['content'])
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_todo(id):
    item_to_delete = TodoItem.query.get_or_404(id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_todo(id):
    item = TodoItem.query.get_or_404(id)
    item.completed = not item.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit_todo(id):
    item = TodoItem.query.get_or_404(id)
    new_content = request.json.get('content')
    item.content = new_content
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
