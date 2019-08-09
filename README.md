# Final Project: Ez2Do (Task Management System)

This project utilized python's Django framework, JavaScript, AJAX and SQL in form of Django's orm.
This app is used to manage user tasks. 

# Requirements
https://cs50.harvard.edu/web/2019/summer/projects/final/#requirements

## Getting started 
This project is used to track and manage tasks.

## Features

Below are the features this app is loaded with:
* User can register and login to app. Once logged in, user needs to activate account from the activation link sent via email.
* User can reset password.
* User can create task, edit his own task, add comments on any task, closed his own task, assign task to other user.
* User can view his own task metrics - Task count by status.
* User can search for any task by title, description and status.

### Prerequisites

Get your environment setup. Make sure you install latest copy of python v 3.6 or higher. Run following command in your terminal to install all necessary packages.

```
pip3 install -r requirements.txt
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Milestones

* Custom User authentication and reCaptcha while signing up to avoid spam registrations.
* Add a new task.
* Edit user's own task. Super user can edit any task.
* View loggedin users open and closed task.
* User can close his own task and has to provide a resolution.
* Search for task by title, text and status. Sort search results.
* Comment on tasks, email notification is sent if user forgets and requests for a password change from the UI.
* Reports using chart.js.


## Tools and frameworks used to build

* [IntelliJ IDEA Ultimate](https://www.jetbrains.com/idea/) - The IDE used for development and code styling/formatting.
* [iTerm2](https://www.iterm2.com/) - Terminal.
* [Bootstrap v4.3.1](https://getbootstrap.com/) - Used this primarily for styling.
* [font-awesome v4.7](https://fontawesome.com/v4.7.0/) - Used to show icons.
* Python v3.7.3
* Django
* AJAX and JavaScript
* Django ORM for SQL
* SQLite3
* django_tables2 for displaying tables
* Django forms for displaying forms
* bootstrap4 python library for making bootstrap styled forms

## Some sample screenshots
##### Home
![Alt text](/../master/examples/home_page.png?raw=true "Home")
##### Login
![Alt text](/../master/examples/login.png?raw=true "Login")
##### Account activate email
![Alt text](/../master/examples/account_activate.png?raw=true "Account activate email")
##### Register
![Alt text](/../master/examples/register.png?raw=true "Login")
##### Dashboard
![Alt text](/../master/examples/dashboard.png?raw=true "Dashboard")
##### Task Details
![Alt text](/../master/examples/task_details.png?raw=true "Task Details")
##### Create Task
![Alt text](/../master/examples/createtask.png?raw=true "Create Task")
##### Edit Task
![Alt text](/../master/examples/edit_task.png?raw=true "Edit Task")
##### Search Results
![Alt text](/../master/examples/search_results.png?raw=true "Search Results")
##### Task Activity
![Alt text](/../master/examples/task_activity.png?raw=true "Task Activity")
##### Password Reset Email
![Alt text](/../master/examples/password_reset_email.png?raw=true "Password Reset Email")

### Project Files
1. views.py - controls what happens when a user visits a URL route (acts like app.py, or application.py, in a FLASK application)
2. settings.py -- I have added few things here. Updated INSTALLED_APPS to include 'bootstrap4','django_tables2' and added gmail settings to send EmailMessage.
3. models.py -  create the structure of tables to be used with the sqlite3 database - to create the SQL commands to reflect the changes to any tables within models.py, you create a "migration" file, which is stored in ~/task/migrations/, by running:
    ```
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```
4. static/img/favicon.ico- required favicon.ico for the website.
5. admin.py -- add models from ~/task/models.py to admin.py in order to track models using the built-in Django admin GUI.
6. urls.py - Used to define app routes like we do in flask, but this is all at one place.
7. task/templates/management
    * base.html - it is re-usable template used in different pages.
    * home.html - home page of the application, user can login or register from this page.
    * dashboard.html - Logged in user can view his tasks
    * search_results.html - Displays search results
    * change_password.html - Custom change password page
    * createtask.html - this has HTML content which serves as a popup modal content when user clicks Add Task from dashboard.
    * login.html - custom login page
    * register.html - registration page
    * task_detail.html - shows details of task
    * task_edit.html - shows task in edit mode
    * taskactivity.html - using chart.js, shows reports for Task by status
8. task/static
    * style.css - basic styling for the application, most of the styling is done by bootstrap framework
    * chart.js - JavaScript file which is responsible to render report.
    * main.js - JavaScript code which pulls content from createtask.html.
9. Miscellaneous pages used handling password changes - 
     - password_reset_complete.html 
     - password_reset_confirm.html 
     - password_reset_done.html 
     - password_reset_email.html
     - password_reset_form.html 
     - password_reset_subject.txt 
10. Miscellaneous python files - 
    - choices.py - used to store select list field values
    -  forms.py - defined all forms used in the application
    -  tables.py - defined search results table here
    -  token.py - generates token for account activation