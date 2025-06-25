from sqlalchemy.orm import validates
from werkzeug.utils import secure_filename

from task_manager import db


class Projects(db.Model):
    """Projects schema"""

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(20))
    active = db.Column(db.Boolean)
    url_slug = db.Column(db.String, unique=True)

    def __init__(self, project_name, active):
        self.project_name = project_name
        self.active = active

    @validates("project_name")
    def _generate_slug(self, _, name):
        self.url_slug = secure_filename(name.lower())
        return name

    def __repr__(self):
        return "<Project {}>".format(self.project_name)


class Tasks(db.Model):
    """Tasks schema"""

    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    task = db.Column(db.Text)
    status = db.Column(db.Boolean, default=False)

    def __init__(self, project_id, task, status=True):
        self.project_id = project_id
        self.task = task
        self.status = status

    def __repr__(self):
        return f"<Task {self.task}>"
