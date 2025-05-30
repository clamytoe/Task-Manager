import unittest
import json
from app import app, db, Projects, Tasks  

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_project(self, name="TestProject", active=False):
        project = Projects(name, active)
        with app.app_context():
            db.session.add(project)
            db.session.commit()
            return project.project_id

    def create_task(self, project_id, task="Test Task", status=True):
        task_obj = Tasks(project_id, task, status)
        with app.app_context():
            db.session.add(task_obj)
            db.session.commit()
            return task_obj.task_id

    def test_get_projects_empty(self):
        response = self.app.get('/api/projects')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_projects(self):
        pid = self.create_project("Project1", True)
        response = self.app.get('/api/projects')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], pid)
        self.assertEqual(data[0]['name'], "Project1")
        self.assertTrue(data[0]['active'])

    def test_get_project_valid(self):
        pid = self.create_project("Project1", True)
        response = self.app.get(f'/api/projects/{pid}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], pid)
        self.assertEqual(data['name'], "Project1")

    def test_get_project_invalid(self):
        response = self.app.get('/api/projects/9999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_tasks_empty(self):
        response = self.app.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_tasks(self):
        pid = self.create_project("Project1", True)
        tid = self.create_task(pid, "Task1", True)
        response = self.app.get('/api/tasks')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], tid)
        self.assertEqual(data[0]['task'], "Task1")

    def test_get_task_valid(self):
        pid = self.create_project("Project1", True)
        tid = self.create_task(pid, "Task1", True)
        response = self.app.get(f'/api/tasks/{tid}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], tid)
        self.assertEqual(data['task'], "Task1")

    def test_get_task_invalid(self):
        response = self.app.get('/api/tasks/9999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_project_success(self):
        response = self.app.post('/api/projects', json={"name": "NewProj", "active": True})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['message'], 'Project created')

    def test_create_project_fail(self):
        response = self.app.post('/api/projects', json={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_task_success(self):
        pid = self.create_project("P", True)
        response = self.app.post('/api/tasks', json={"project_id": pid, "task": "New Task", "status": False})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['message'], 'Task created')

    def test_create_task_fail(self):
        response = self.app.post('/api/tasks', json={"task": "No project"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_project_success(self):
        pid = self.create_project("OldName", False)
        response = self.app.put(f'/api/projects/{pid}', json={"name": "UpdatedName", "active": True})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Project updated')
        with app.app_context():
            p = Projects.query.get(pid)
            self.assertEqual(p.project_name, "UpdatedName")
            self.assertTrue(p.active)

    def test_update_project_fail(self):
        response = self.app.put('/api/projects/9999', json={"name": "Name"})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_task_success(self):
        pid = self.create_project("P", True)
        tid = self.create_task(pid, "OldTask", True)
        response = self.app.put(f'/api/tasks/{tid}', json={"task": "NewTask", "status": False})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Task updated')
        with app.app_context():
            t = Tasks.query.get(tid)
            self.assertEqual(t.task, "NewTask")
            self.assertFalse(t.status)

    def test_update_task_fail(self):
        response = self.app.put('/api/tasks/9999', json={"task": "Name"})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_delete_project_success(self):
        pid = self.create_project("ToDelete", True)
        response = self.app.delete(f'/api/projects/{pid}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Project deleted')
        with app.app_context():
            self.assertIsNone(Projects.query.get(pid))

    def test_delete_project_fail(self):
        response = self.app.delete('/api/projects/9999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_delete_task_success(self):
        pid = self.create_project("P", True)
        tid = self.create_task(pid, "TaskToDelete", True)
        response = self.app.delete(f'/api/tasks/{tid}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Task deleted')
        with app.app_context():
            self.assertIsNone(Tasks.query.get(tid))

    def test_delete_task_fail(self):
        response = self.app.delete('/api/tasks/9999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_delete_all_success(self):
        pid = self.create_project("P", True)
        tid = self.create_task(pid, "Task", True)
        response = self.app.delete('/api/delete_all')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'All projects and tasks deleted')
        with app.app_context():
            self.assertEqual(Projects.query.count(), 0)
            self.assertEqual(Tasks.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
