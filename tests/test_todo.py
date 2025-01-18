from app.models import Todo
from app import db

def test_new_todo(app):
    """
    GIVEN a Todo model
    WHEN a new Todo is created
    THEN check the title, description, and completed fields are defined correctly
    """
    with app.app_context():
        todo = Todo(title='Test Todo', description='Test Description')
        db.session.add(todo)
        db.session.commit()

        assert todo.title == 'Test Todo'
        assert todo.description == 'Test Description'
        assert todo.completed is False
        assert todo.id is not None

def test_todo_creation(client):
    """
    GIVEN a Flask application
    WHEN the '/todo/create' page is posted to (POST)
    THEN check the response is valid and todo is created
    """
    response = client.post('/todo/create', data={
        'title': 'Test Todo',
        'description': 'Test Description'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    with client.application.app_context():
        todo = Todo.query.first()
        assert todo is not None
        assert todo.title == 'Test Todo'
        assert todo.description == 'Test Description'

def test_todo_toggle(client):
    """
    GIVEN a Flask application and an existing todo
    WHEN the todo's status is toggled
    THEN check the todo's completed status is changed
    """
    with client.application.app_context():
        # Create a test todo
        todo = Todo(title='Test Todo', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

        # Toggle the todo
        response = client.post(f'/todo/{todo_id}/toggle', follow_redirects=True)
        assert response.status_code == 200

        # Check if the todo is now completed
        todo = Todo.query.get(todo_id)
        assert todo.completed is True

        # Toggle again
        response = client.post(f'/todo/{todo_id}/toggle', follow_redirects=True)
        assert response.status_code == 200

        # Check if the todo is now uncompleted
        todo = Todo.query.get(todo_id)
        assert todo.completed is False

def test_todo_deletion(client):
    """
    GIVEN a Flask application and an existing todo
    WHEN the todo is deleted
    THEN check the todo no longer exists
    """
    with client.application.app_context():
        # Create a test todo
        todo = Todo(title='Test Todo', description='Test Description')
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

        # Delete the todo
        response = client.post(f'/todo/{todo_id}/delete', follow_redirects=True)
        assert response.status_code == 200

        # Check if the todo is deleted
        todo = Todo.query.get(todo_id)
        assert todo is None

def test_todo_edit(client):
    """
    GIVEN a Flask application and an existing todo
    WHEN the todo is edited
    THEN check the todo's details are updated
    """
    with client.application.app_context():
        # Create a test todo
        todo = Todo(title='Original Title', description='Original Description')
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

        # Edit the todo
        response = client.post(f'/todo/{todo_id}/edit', data={
            'title': 'Updated Title',
            'description': 'Updated Description'
        }, follow_redirects=True)
        assert response.status_code == 200

        # Check if the todo is updated
        todo = Todo.query.get(todo_id)
        assert todo.title == 'Updated Title'
        assert todo.description == 'Updated Description'
