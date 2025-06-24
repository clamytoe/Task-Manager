# REST API

Video: https://drive.google.com/file/d/1xxiQkPa1zuDXlYim_cQv0lNoopiwtGFZ/view?usp=sharing

Swagger documentation: http://localhost:5000/apidocs/

Steps:
1. The changes are located in the REST_feature branch of this repository. Use: git checkout REST_feature
2. Activate the installed libraries on the Dependencies_Environment folder using: cd/Dependencies_Environment/Scripts, then enter activate.
3. Enter cd.. twice, then run app.py
 4. The website is hosted at http://localhost:5000

New features:
  Note: I did not delete any of the original's code in order to preserve the functionality of the website's buttons. These features added are mainly testable/executable using Postman.

  There were two general ways on how I have modified this flask app, and it was through ADDING and ENHANCING.
  -Adding: 
    
  1. Implemented the use of JSONIFY to transform captured data into JSON format for the api.
  2. Added GET method to retrieve all the tasks and projects in JSON format. It can also retrieve a singular task or project using its id.
  3. Added PUT method to rename tasks and projects as well as updating its Open/Closed status.
  4. Added a DELETE method to delete all tasks and projects AT ONCE.
  
  -ENHANCING:
1. Enhanced POST methods in adding projects and tasks, although, it is currently only executable using Postman. Meaning the UI buttons on the website are still not bounded to it, however, these methods are fully functional and correctly submits data to the api in JSON format.
2. Added a DELETE method to delete a single task or project using the api''s endpoint and its id to support RESTful implementation and improve the original's version which previously deleted a task/project using POST method.

Testing. Ensure you are in REST_feature branch and app.py is already running:
  GET METHODS: Simply enter this on your web browser.
1. http://localhost:5000/api/projects => Displays all projects in JSON format.
2. http://localhost:5000/api/projects/<id> => Displays a single project using its ID.
3. http://localhost:5000/api/tasks => Displays all tasks in JSON formate.
4. http://localhost:5000/api/tasks/<id> => Displays a single task using its ID.


POST, PUT, and DELETE METHODS: Executable mainly using postman.

POST: On postman, kindly select the method to POST. The data submitted will only appear on the website ONCE a project is created and at least ONE task is added for that said project/used the project's id. 

    1. Create a new project:
        Endpoint: http://localhost:5000/api/projects   
        Headers: Content-Type: application/json
        Body:
            {
              "name": "Name of project",
              "active": true
            }

    2. Add a task for a project. Project_id and task_id can be found by typing the endpoint of GET method no. 1. and GET method no.3 respectively:
        Endpoint: http://localhost:5000/api/tasks
        Headers: Content-Type: application/json
        Body:
          {
            "task": "Name of task",
            "project_id": project_id,
            "status": true
          }

  PUT: Testable using postman.
  
    1. Rename project name and update status
      Method: PUT
      Endpoint: http:localhost:5000/api/projects/project_id
      Headers: Content-Type: application/json
      Body:
        {
          "name": "New project name",
          "status": false
        }

    2. Rename task and update status
    Method: PUT
    Endpoint: http:localhost:5000/api/tasks/task_id
    Headers: Content-Type: application/json
    Body:
      {
        "task": "New task name",
        "status": false
      }

  DELETE: Testable using postman.
  
    1. Delete a single project.
    Method: DELETE
    Endpoint: http://localhost:5000/api/projects/project_id
    No headers or body needed

    2. Delete a single task.
    Method: DELETE
    Endpoint: http://localhost:5000/api/tasks/task_id
    No headers or body needed

    3. Delete all projects and tasks.
    Method: DELETE
    Endpoint: http://localhost:5000/api/delete_all
    No headers or body needed