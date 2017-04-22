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


