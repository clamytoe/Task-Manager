from task_manager import db


class Projects(db.Model):
    """Projects schema"""

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(20))
    active = db.Column(db.Boolean)

    def __init__(self, project, active):
        self.project_name = project
        self.active = active

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
