from flask import Blueprint, redirect, render_template, request

from .models import Projects, Tasks, db

routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
    """Home page of the app

    It loads the template page and passes on any current tasks and projects
    that exist. Also passes along the currently active tab. If the active tab
    was removed, selects the first project in the Projects database and sets
    that one as the active one.
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
        return render_template(
            "index.html", tasks=tasks, projects=projects, active=active
        )
    else:
        return render_template("index.html", tasks=tasks, active=active)


@routes.route("/add", methods=["POST"])
def add_task():
    """Adds a new task

    Redirects to home page if no task was entered. Sets project to default of
    Tasks if none was entered. If the entered project does not exists, it is
    added to the database and sets the active tab.
    """
    found = False
    project_id = None
    task = request.form["task"]
    project = request.form["project"]

    if not task:
        return redirect("/")

    if not project:
        project = "Tasks"

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

    status = bool(int(request.form["status"]))

    # add the new task
    new_task = Tasks(project_id, task, status)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")


@routes.route("/close/<int:task_id>")
def close_task(task_id):
    """Changes the state of a task

    If the task is open, it closes it. If it's close, it opens it.
    Redirects to home page if the task does not exists.
    """
    task = db.session.get(Tasks, task_id)

    if not task:
        return redirect("/")

    if task.status:
        task.status = False
    else:
        task.status = True

    db.session.commit()
    return redirect("/")


@routes.route("/delete/<int:task_id>")
def delete_task(task_id):
    """Deletes task by its ID

    If the task does not exist, redirects to home page.
    """
    task = db.session.get(Tasks, task_id)

    if not task:
        return redirect("/")

    db.session.delete(task)
    db.session.commit()
    return redirect("/")


@routes.route("/clear/<delete_id>")
def clear_all(delete_id):
    """Dumps all tasks from the active tab and removes the project tab"""
    Tasks.query.filter(Tasks.project_id == delete_id).delete()
    Projects.query.filter(Projects.project_id == delete_id).delete()
    db.session.commit()

    return redirect("/")


@routes.route("/remove/<lists_id>")
def remove_all(lists_id):
    """Dumps all tasks from the active tab"""
    Tasks.query.filter(Tasks.project_id == lists_id).delete()
    db.session.commit()

    return redirect("/")


@routes.route("/project/<tab>")
def tab_nav(tab):
    """Switches between active tabs"""
    projects = Projects.query.all()

    for project in projects:
        if project.project_name == tab:
            project.active = True
        else:
            project.active = False

    db.session.commit()
    return redirect("/")


@routes.route("/rename_project/<int:id>", methods=["POST"])
def rename_project(id):
    data = request.get_json()
    new_name = data.get("new_name", "").strip()
    if new_name:
        project = db.session.get(Projects, id)
        if not project:
            return "Project not found", 404
        project.project_name = new_name
        db.session.commit()
        return "", 204
    return "Invalid name", 400


@routes.route("/rename_task_desc/<int:id>", methods=["POST"])
def rename_task_desc(id):
    data = request.get_json()
    new_desc = data.get("new_desc", "").strip()
    if new_desc:
        task = db.session.get(Tasks, id)
        if not task:
            return "Task not found", 404
        task.task = new_desc
        db.session.commit()
        return "", 204
    return "Invalid description", 400
