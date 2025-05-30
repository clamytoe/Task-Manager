#Video
  link: 

##Steps:
  1. The changes are located in the REST_feature branch of this repository. Use: git checkout REST_feature
  2. Activate the installed libraries on the Dependencies_Environment folder using: cd/Dependencies_Environment/Scripts, then enter activate.
  3. Enter cd.. twice, then run app.py
  4. The website is hosted at http://localhost:5000

###New features:
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

####Testing. Ensure you are in REST_feature branch and app.py is already running:
  GET METHODS: Simply enter this on your web browser.
    1. http://localhost:5000/api/projects                --->              Displays all projects in JSON format.
    2. http://localhost:5000/api/projects/<id>           --->              Displays a single project using its ID.
    3. http://localhost:5000/api/tasks                   --->              Displays all tasks in JSON formate.
    4. http://localhost:5000/api/tasks/<id>              --->              Displays a single task using its ID.


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


-Original README below-

# Task-Manager
A no frills task manager that's really intuitive and simple to use that I created for a PyBites code challenge.

## Index
* [UI](#ui)
  * [New Project](#new-project)
  * [New Task](#new-task)
  * [Task Status](#task-status)
  * [Controls](#controls)
  * [Project Tabs](#project-tabs)
  * [Remove Project](#remove-project)
  * [Remove All Tasks](#remove-all-tasks)
  * [Status Toggle](#status-toggle)
  * [Remove Task](#remove-task)
* [Installation](#installation)

#### UI

##### New Project
![New Project](img/project.png)

Enter the project name that you want to store your tasks
under.

##### New Task
![New Task](img/task.png)

Describe the task that you need to accomplish.

##### Task Status
![Task Status](img/status.png)

The task can be entered as open or close.

##### Controls
![Controls](img/controls.png)

Clicking on the **Add** button will add the new task and create
a new project if it does not already exist.

Clicking on the **Reset** button will reset the fields.

##### Project tabs
![Project Tabs](img/tabs.png)

Any projects that are created will be displayed here in the
tab area. Clickin on the tab switches you to that project.

##### Remove Project
![Remove Project](img/remove_project.png)

Clicking on this will remove the currently active project
along with all of it's corresponding tasks.

##### Remove all tasks
![Remove Tasks](img/remove_all_tasks.png)

Clicking this will remove all tasks from the active project,
but leave the project active.

##### Status toggle
![Status Toggle](img/status_toggle.png)

Clicking this will toggle the tasks from open to close.

##### Remove task
![Remove Task](img/remove_task.png)

Clicking this will remove that tasks from the project.

## Installation
First of all you have to prepare your environment. Select
a location where you want to store the files. I will use 
Projects as my example. I'm also on a linux machine, but
you should be able to figure it out for any other platform.

    mkdir Projects
    cd Projects
    git clone https://github.com/clamytoe/Task-Manager.git
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py

Then simply open up a browser, Chrome/Chromium recommended,
to [localhost:5000](http://localhost:5000/) and play around
with it :).


