from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Todo
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@bp.route('/todo/create', methods=['POST'])
def create_todo():
    title = request.form.get('title')
    description = request.form.get('description')
    
    if not title:
        flash('Title is required!')
        return redirect(url_for('main.index'))
    
    todo = Todo(title=title, description=description)
    db.session.add(todo)
    db.session.commit()
    
    return redirect(url_for('main.index'))

@bp.route('/todo/<int:id>/toggle', methods=['POST'])
def toggle_todo(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/todo/<int:id>/delete', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/todo/<int:id>/edit', methods=['POST'])
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    title = request.form.get('title')
    description = request.form.get('description')
    
    if not title:
        flash('Title is required!')
        return redirect(url_for('main.index'))
    
    todo.title = title
    todo.description = description
    db.session.commit()
    
    return redirect(url_for('main.index'))