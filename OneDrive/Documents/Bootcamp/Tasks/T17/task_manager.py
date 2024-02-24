# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Login loop
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# Function to register user
def reg_user():
    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        with open("user.txt", "w") as out_file:
            user_data = [f"{k};{username_password[k]}" for k in username_password]
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do not match")

# Function to add a task
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    task_due_date = input("Due date of task (YYYY-MM-DD): ")
    due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = [";".join([t['username'], t['title'], t['description'], t['due_date'].strftime(DATETIME_STRING_FORMAT), t['assigned_date'].strftime(DATETIME_STRING_FORMAT), "Yes" if t['completed'] else "No"]) for t in task_list]
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all():
    for t in task_list:
        disp_str = "\n".join([f"\nTask: \t\t {t['title']}", f"Assigned to: \t {t['username']}", f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}", f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}", f"Task Description: \n {t['description']}"])
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine():
    user_tasks = [t for t in task_list if t['username'] == curr_user]
    if not user_tasks:
        print("No tasks assigned to you.")
        return

    for index, task in enumerate(user_tasks, start=1):
        print(f"{index}. Task: {task['title']} - Due: {task['due_date'].strftime(DATETIME_STRING_FORMAT)} - Completed: {'Yes' if task['completed'] else 'No'}")

    task_choice = int(input("Select a task number to edit or mark as complete, or -1 to return to the main menu: "))
    if task_choice == -1:
        return

    selected_task = user_tasks[task_choice - 1]  # Adjusting for zero-based index
    action = input("Would you like to (c)omplete or (e)dit the task? Enter 'c' or 'e': ").lower()

    if action == 'c':
        selected_task['completed'] = True
        print("Task marked as complete.")
    elif action == 'e' and not selected_task['completed']:
        new_username = input("Enter new username for the task (leave blank to keep current): ")
        new_due_date = input("Enter new due date for the task (YYYY-MM-DD, leave blank to keep current): ")
        if new_username:
            selected_task['username'] = new_username
        if new_due_date:
            selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
        print("Task updated.")
    else:
        print("Completed tasks cannot be edited.")

    # Save changes back to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = [";".join([t['username'], t['title'], t['description'], t['due_date'].strftime(DATETIME_STRING_FORMAT), t['assigned_date'].strftime(DATETIME_STRING_FORMAT), "Yes" if t['completed'] else "No"]) for t in task_list]
        task_file.write("\n".join(task_list_to_write))

# Function to generate reports
def generate_reports():
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.now())
    if total_tasks > 0:
        incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
    else:
        incomplete_percentage = 0 
    if total_tasks > 0:
        overdue_percentage = (overdue_tasks / total_tasks) * 100
    else:
        overdue_percentage = 0 

    with open("task_overview.txt", "w") as file:
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed_tasks}\n")
        file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        file.write(f"Overdue tasks: {overdue_tasks}\n")
        file.write(f"Percentage incomplete: {incomplete_percentage:.2f}%\n")
        file.write(f"Percentage overdue: {overdue_percentage:.2f}%\n")

    user_tasks = {user: 0 for user in username_password.keys()}
    for task in task_list:
        user_tasks[task['username']] += 1

    with open("user_overview.txt", "w") as file:
        file.write(f"Total users: {len(username_password)}\n")
        file.write(f"Total tasks: {total_tasks}\n")
        for user, tasks in user_tasks.items():
            completed = sum(1 for task in task_list if task['username'] == user and task['completed'])
            incomplete = tasks - completed
            overdue = sum(1 for task in task_list if task['username'] == user and not task['completed'] and task['due_date'] < datetime.now())
            file.write(f"\nUser: {user}\n")
            file.write(f"Tasks assigned: {tasks}\n")
            file.write(f"Completed tasks: {(completed / tasks) * 100:.2f}%\n")
            file.write(f"Incomplete tasks: {(incomplete / tasks) * 100:.2f}%\n")
            file.write(f"Overdue tasks: {(overdue / tasks) * 100:.2f}%\n")
    
    print("Reports Generated")

# Function to display statistics
def display_statistics():
    # Ensure required files exist or generate them
    if not os.path.exists("task_overview.txt") and not os.path.exists("user_overview.txt"):
        generate_reports()

    # Read and prepare task statistics
    with open("task_overview.txt", 'r') as file:
        task_stats = file.read()
    
    # Read and prepare user statistics
    with open("user_overview.txt", 'r') as file:
        user_stats = file.read()

    # Display the statistics
    print("\n====== Task Statistics ======")
    print(task_stats)
    print("\n====== User Statistics ======")
    print(user_stats)

# Main menu loop
# Prompt user for action and call appropriate function based on input
while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_reports()
    elif menu == 'ds':
        display_statistics()
    elif menu == 'e':
        print('Goodbye!!!')
        break
    else:
        print("Invalid option, please try again.")