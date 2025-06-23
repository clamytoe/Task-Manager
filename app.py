from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ctm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

swagger = Swagger(app)


class Projects(db.Model):
    """Projects schema"""
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(20))
    active = db.Column(db.Boolean)

    def __init__(self, project, active):
        self.project_name = project
        self.active = active

    def __repr__(self):
        return '<Project {}>'.format(self.project_name)


class Tasks(db.Model):
    """Tasks schema"""
    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    task = db.Column(db.Text)
    status = db.Column(db.Boolean, default=False)

    def __init__(self, project_id, task, status=True):
        self.project_id = project_id
        self.task = task
        self.status = status

    def __repr__(self):
        return '<Task {}>'.format(self.task)


# initialize the database
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Home page of the app
    
    It loads the template page and passes on any current tasks and projects that exist.
    Also passes along the currently active tab. If the active tab was removed, selects
    the first project in the Projects database and sets that one as the active one.
    """
    active = None
    projects = Projects.query.all()
    tasks = Tasks.query.all()

    if len(projects) == 1:
        projects[0].active = True
        active = projects[0].project_id
        db.session.commit()

    if projects:
        for project in projects:
            if project.active:
                active = project.project_id
        if not active:
            projects[0].active = True
            active = projects[0].project_id
    else:
        projects = None

    if projects:
        return render_template('index.html', tasks=tasks, projects=projects, active=active)
    else:
        return render_template('index.html', tasks=tasks, active=active)


@app.route('/add', methods=['POST'])
def add_task():
    """Adds a new task
    
    Redirects to home page if no task was entered. Sets project to default of Tasks if
    none was entered. If the entered project does not exists, it is added to the database
    and sets the active tab.
    """
    found = False
    project_id = None
    task = request.form['task']
    project = request.form['project']
    
    if not task:
        return redirect('/')

    if not project:
        project = 'Tasks'

    projects = Projects.query.all()

    for proj in projects:
        if proj.project_name == project:
            found = True

    # add the project if not in database already
    if not found:
        add_project = Projects(project, True)
        db.session.add(add_project)
        db.session.commit()
        projects = Projects.query.all()

    # set the active tab
    for proj in projects:
        if proj.project_name == project:
            project_id = proj.project_id
            proj.active = True
        else:
            proj.active = False

    status = bool(int(request.form['status']))

    # add the new task
    new_task = Tasks(project_id, task, status)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')


@app.route('/close/<int:task_id>')
def close_task(task_id):
    """Changes the state of a task
    
    If the task is open, it closes it. If it's close, it opens it.
    Redirects to home page if the task does not exists.
    """
    task = Tasks.query.get(task_id)

    if not task:
        return redirect('/')

    if task.status:
        task.status = False
    else:
        task.status = True

    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Deletes task by its ID

    If the task does not exist, redirects to home page.
    """
    task = Tasks.query.get(task_id)

    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/clear/<delete_id>')
def clear_all(delete_id):
    """Dumps all tasks from the active tab and removes the project tab"""
    Tasks.query.filter(Tasks.project_id == delete_id).delete()
    Projects.query.filter(Projects.project_id == delete_id).delete()
    db.session.commit()

    return redirect('/')


@app.route('/remove/<lists_id>')
def remove_all(lists_id):
    """Dumps all tasks from the active tab"""
    Tasks.query.filter(Tasks.project_id == lists_id).delete()
    db.session.commit()

    return redirect('/')


@app.route('/project/<tab>')
def tab_nav(tab):
    """Switches between active tabs"""
    projects = Projects.query.all()

    for project in projects:
        if project.project_name == tab:
            project.active = True
        else:
            project.active = False

    db.session.commit()
    return redirect('/')


@app.route('/rename_project/<int:id>', methods=['POST'])
def rename_project(id):
    data = request.get_json()
    new_name = data.get('new_name', '').strip()
    if new_name:
        project = Projects.query.get_or_404(id)
        project.project_name = new_name
        db.session.commit()
        return '', 204
    return 'Invalid name', 400


@app.route('/rename_task_desc/<int:id>', methods=['POST'])
def rename_task_desc(id):
    data = request.get_json()
    new_desc = data.get('new_desc', '').strip()
    if new_desc:
        task = Tasks.query.get_or_404(id)
        task.task = new_desc
        db.session.commit()
        return '', 204
    return 'Invalid description', 400


# new features below."

@app.route('/api/projects', methods=['GET'])
def api_get_projects():
    """
    Get all projects
    ---
    tags: [Projects]
    responses:
      200:
        description: List of all projects
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              name:
                type: string
              active:
                type: boolean
    """
    projects = Projects.query.all()
    return jsonify([
        {'id': p.project_id, 'name': p.project_name, 'active': p.active}
        for p in projects
    ]), 200

@app.route('/api/projects/<int:id>', methods=['GET'])
def api_get_project(id):
    """
    Get project by ID
    ---
    tags: [Projects]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Project found
      404:
        description: Project not found
    """
    project = Projects.query.get(id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify({'id': project.project_id, 'name': project.project_name, 'active': project.active}), 200

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """
    Get all tasks
    ---
    tags: [Tasks]
    responses:
      200:
        description: List of all tasks
    """
    tasks = Tasks.query.all()
    return jsonify([
        {'id': t.task_id, 'project_id': t.project_id, 'task': t.task, 'status': t.status}
        for t in tasks
    ]), 200

@app.route('/api/tasks/<int:id>', methods=['GET'])
def api_get_task(id):
    """
    Get task by ID
    ---
    tags: [Tasks]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Task found
      404:
        description: Task not found
    """
    task = Tasks.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'id': task.task_id, 'project_id': task.project_id, 'task': task.task, 'status': task.status}), 200

@app.route('/api/projects', methods=['POST'])
def api_create_project():
    """
    Create a new project
    ---
    tags: [Projects]
    parameters:
      - in: body
        name: project
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            active:
              type: boolean
    responses:
      201:
        description: Project created
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Project name is required'}), 400
    project = Projects(data['name'], data.get('active', False))
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Project created', 'id': project.project_id}), 201

@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    """
    Create a new task
    ---
    tags: [Tasks]
    parameters:
      - in: body
        name: task
        required: true
        schema:
          type: object
          properties:
            project_id:
              type: integer
            task:
              type: string
            status:
              type: boolean
    responses:
      201:
        description: Task created
    """
    data = request.get_json()
    if not data or 'task' not in data or 'project_id' not in data:
        return jsonify({'error': 'Missing task or project_id'}), 400
    task = Tasks(data['project_id'], data['task'], data.get('status', True))
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created', 'id': task.task_id}), 201

@app.route('/api/projects/<int:id>', methods=['PUT'])
def api_update_project(id):
    """
    Update a project
    ---
    tags: [Projects]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: project
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            active:
              type: boolean
    responses:
      200:
        description: Project updated
    """
    data = request.get_json()
    project = Projects.query.get(id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    project.project_name = data.get('name', project.project_name)
    project.active = data.get('active', project.active)
    db.session.commit()
    return jsonify({'message': 'Project updated'}), 200

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def api_update_task(id):
    """
    Update a task
    ---
    tags: [Tasks]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: task
        required: true
        schema:
          type: object
          properties:
            task:
              type: string
            status:
              type: boolean
    responses:
      200:
        description: Task updated
    """
    data = request.get_json()
    task = Tasks.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    task.task = data.get('task', task.task)
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'message': 'Task updated'}), 200

@app.route('/api/projects/<int:id>', methods=['DELETE'])
def api_delete_project(id):
    """
    Delete a project
    ---
    tags: [Projects]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Project deleted
      404:
        description: Project not found
    """
    project = Projects.query.get(id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'}), 200

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def api_delete_task(id):
    """
    Delete a task
    ---
    tags: [Tasks]
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Task deleted
      404:
        description: Task not found
    """
    task = Tasks.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200

@app.route('/api/delete_all', methods=['DELETE'])
def api_delete_all():
    """
    Delete all tasks and projects
    ---
    tags: [Admin]
    responses:
      200:
        description: All records deleted
      500:
        description: Deletion failed
    """
    try:
        Tasks.query.delete()
        Projects.query.delete()
        db.session.commit()
        return jsonify({'message': 'All projects and tasks deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete all records', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
