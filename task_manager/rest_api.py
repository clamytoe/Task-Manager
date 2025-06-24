from flask import Blueprint, jsonify, request

from .models import Projects, Tasks, db

rest_api_routes = Blueprint("routes", __name__)


@rest_api_routes.route("/api/projects", methods=["GET"])
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
    return (
        jsonify(
            [
                {"id": p.project_id, "name": p.project_name, "active": p.active}
                for p in projects
            ]
        ),
        200,
    )


@rest_api_routes.route("/api/projects/<int:id>", methods=["GET"])
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
        return jsonify({"error": "Project not found"}), 404
    return (
        jsonify(
            {
                "id": project.project_id,
                "name": project.project_name,
                "active": project.active,
            }
        ),
        200,
    )


@rest_api_routes.route("/api/tasks", methods=["GET"])
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
    return (
        jsonify(
            [
                {
                    "id": t.task_id,
                    "project_id": t.project_id,
                    "task": t.task,
                    "status": t.status,
                }
                for t in tasks
            ]
        ),
        200,
    )


@rest_api_routes.route("/api/tasks/<int:id>", methods=["GET"])
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
        return jsonify({"error": "Task not found"}), 404
    return (
        jsonify(
            {
                "id": task.task_id,
                "project_id": task.project_id,
                "task": task.task,
                "status": task.status,
            }
        ),
        200,
    )


@rest_api_routes.route("/api/projects", methods=["POST"])
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
    if not data or "name" not in data:
        return jsonify({"error": "Project name is required"}), 400
    project = Projects(data["name"], data.get("active", False))
    db.session.add(project)
    db.session.commit()
    return jsonify({"message": "Project created", "id": project.project_id}), 201


@rest_api_routes.route("/api/tasks", methods=["POST"])
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
    if not data or "task" not in data or "project_id" not in data:
        return jsonify({"error": "Missing task or project_id"}), 400
    task = Tasks(data["project_id"], data["task"], data.get("status", True))
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created", "id": task.task_id}), 201


@rest_api_routes.route("/api/projects/<int:id>", methods=["PUT"])
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
        return jsonify({"error": "Project not found"}), 404
    project.project_name = data.get("name", project.project_name)
    project.active = data.get("active", project.active)
    db.session.commit()
    return jsonify({"message": "Project updated"}), 200


@rest_api_routes.route("/api/tasks/<int:id>", methods=["PUT"])
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
        return jsonify({"error": "Task not found"}), 404
    task.task = data.get("task", task.task)
    task.status = data.get("status", task.status)
    db.session.commit()
    return jsonify({"message": "Task updated"}), 200


@rest_api_routes.route("/api/projects/<int:id>", methods=["DELETE"])
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
        return jsonify({"error": "Project not found"}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"}), 200


@rest_api_routes.route("/api/tasks/<int:id>", methods=["DELETE"])
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
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200


@rest_api_routes.route("/api/delete_all", methods=["DELETE"])
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
        return jsonify({"message": "All projects and tasks deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"error": "Failed to delete all records", "details": str(e)}),
            500,
        )
