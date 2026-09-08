from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import validates
from werkzeug.utils import secure_filename

from task_manager import db

VALID_PRIORITIES = {"Low", "Medium", "High"}


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
    project_name = db.Column(db.String(255), nullable=False)
    task = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(20), default="Medium")
    due_date = db.Column(Date, nullable=True)

    def __init__(self, project_name, task, *, status=True, priority="Medium", due_date=None):
        self.project_name = project_name
        self.task = task
        self.status = status
        self.priority = priority

        # Accept None or ISO string
        if isinstance(due_date, str):
            self.due_date = date.fromisoformat(due_date)
        else:
            self.due_date = due_date

    @property
    def is_overdue(self):
        if not self.due_date:
            return False
        return date.today() > self.due_date

    @property
    def due_date_display(self):
        if not self.due_date:
            return "Unassigned"
        return self.due_date.strftime("%d/%m")
