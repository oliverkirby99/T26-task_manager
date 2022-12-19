# =====importing libraries===========
# Import datetime. I found this from:
# https://www.w3schools.com/python/python_datetime.asp
import datetime

# Define the function that will create new users.
def reg_user():
    print("You have selected 'Register a new user'")

    new_username = input("Enter a new username: ").lower()  # Get the new username and convert to lowercase

    users_f = open("user.txt", "r")  # Open the user.txt file as read mode to check the file for duplicates
    for line in users_f:  # Check all users in user.txt
        user_check = line.split()  # Break the username and password into separate strings
        username_check = user_check[0].strip(",")  # Set the username to be checked (remove the ,)
        while new_username == username_check:  # If the user exists, it's a duplicate, please try again
            new_username = input("User already exists, please enter a new username: ").lower()
    users_f.close()
    new_password = input("Enter a password: ")  # Get the new password
    confirm_password = input("Please confirm your password: ")  # Get password confirmation

    while confirm_password != new_password:  # Check if new password matches password confirmation
        print("Passwords did not match.")
        confirm_password = input("Please confirm your password: ")  # Keep asking to enter password until they match

    if new_password == confirm_password:  # Append the username and password to a new line on user.txt
        users_f = open("user.txt", "a")  # Open the user.txt file as read mode to check the file for duplicates
        users_f.write(f"\n{new_username}, {new_password}")
        users_f.close()  # close user.txt
        print("Account created!")


def add_task():
    print("You have selected 'Create new task'")

    assignee = input("Which user do you want to assign this task to? ").lower()
    new_task_title = input("Task summary: ")
    new_task_detail = input("Enter the task detail: ")
    new_task_due = input("When is this task due (use: 01 Jan 2000)? ")
    complete = "No"

    # Get the current date and set the date, month and year into 3 variables
    current_date = datetime.datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year

    # Convert the month into short_date (-1 to match the index)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    short_month = months[month - 1]

    current_date = str(f"{day} {short_month} {year}")  # Current date

    # === User Check ===
    users = open("user.txt", "r")  # Open user.txt as read-only
    user_verified = False  # Set a bool to verify if the user exists

    while not user_verified:
        users.seek(0, 0)  # Reset the current location in user.txt
        for user in users:  # Check all users in user.txt
            user_check = user.split()  # Break the username and password into separate strings
            username_check = user_check[0].strip(",")  # Set the username to be checked (remove the ,)
            if assignee == username_check:  # If the user exists, verify and move on
                users.close()  # close the user.txt file
                user_verified = True
                break
            else:
                continue
        if assignee != username_check:  # If the user does not exist, re-confirm the user and loop again
            print("User not found, please try again")
            assignee = input("Which user do you want to assign this task to? ").lower()

    # === Show Preview of Task ===
    # Preview - Print everything that will be added to the file, if confirmed by user
    print("############################################################")
    print(f"Task:\t\t\t{new_task_title}")
    print(f"Assigned to:\t\t{assignee}")
    print(f"Date assigned:\t\t{current_date}")
    print(f"Due Date:\t\t{new_task_due}")
    print(f"Task Complete?:\t\tNo")
    print(f"Task description:\t{new_task_detail}")
    print("############################################################")

    # === Confirm Task ===
    confirm = input("Do you want to add this task (y/n)? ").lower()
    if confirm == "n":
        print("Task Cancelled")
    elif confirm == "y":  # Add the task and all details to the file
        task_file = open("tasks.txt", "a")
        task_file.write(f"\n{assignee}, {new_task_title}, {new_task_detail}, {new_task_due}, {current_date}, No")
        task_file.close()  # Close the file
    else:
        # Keep asking y or n until it is entered.
        while confirm != "y" and confirm != "n":
            confirm = input("Invalid input, do you want to add this task (y/n)? ").lower()
        if confirm == "n":
            print("Task Cancelled")
        elif confirm == "y":  # Add the task and all details to the file
            task_file = open("tasks.txt", "a")
            task_file.write(
                f"\n{assignee}, {new_task_title}, {new_task_detail}, {new_task_due}, {current_date}, No")
            task_file.close()  # Close the file


def view_all():
    print("You have selected 'View All Tasks'\n")

    tasks_file = open("tasks.txt", "r")

    for task in tasks_file:  # Go through all tasks, break them up into individual elements and display them, 1 by 1
        full_task = task.split(",")
        print("############################################################")
        print(f"Task:\t\t\t{full_task[1]}")
        print(f"Assigned to:\t\t {full_task[0]}")
        print(f"Date Assigned:\t\t{full_task[4]}")
        print(f"Due Date:\t\t{full_task[3]}")
        print(f"Task Complete?:\t\t{full_task[5]}")
        print(f"Task Description:\t{full_task[2]}")
        print("############################################################\n")

    tasks_file.close()


def edit_task(edit_task_no, new_entry, position):

    with open("tasks.txt", "r") as tasks_file:  # Read the file
        all_tasks = tasks_file.readlines()  # Put all lines into a list

    this_task = all_tasks[edit_task_no - 1]  # this specific task is this_task
    this_task_split = this_task.split(",")  # Split this_task by ","

    # Check if task is complete. If "Yes", then the edit cannot be made
    if this_task_split[-1] == " Yes\n":
        print("############################################################")
        print("This task is complete and cannot be edited!")
        input("############################################################\n")
    else:
        # Check if it is the assignee being changed, don't add a " " before
        if position != 0:
            this_task_split[position] = f" {new_entry}"  # Replace task summary with new_task_title
        else:
            this_task_split[position] = f"{new_entry}"  # Replace task summary with new_task_title

        updated_task = this_task_split  # updated_task is a list of all the updated task components

        all_tasks[edit_task_no - 1] = ""  # Delete the current task info
        for section in updated_task:  # For all parts of the updated_task
            if section != updated_task[-1]:
                all_tasks[edit_task_no - 1] = all_tasks[edit_task_no - 1] + f"{section},"  # Add the section to the line with a ","
            else:
                all_tasks[edit_task_no - 1] = all_tasks[edit_task_no - 1] + f"{section}"  # Leave out the "," for the last item

        with open("tasks.txt", "w") as tasks_file:  # Write all the lines back to the file with the new line
            for line in all_tasks:
                tasks_file.write(line)
    tasks_file.close()


def view_mine():
    print("You have selected 'View Your Tasks'\n")

    tasks_file = open("tasks.txt", "r")  # Read the tasks file
    tasks_printed = 0  # Count how many tasks are assigned to the user

    task_no = 0  # Create value to count how many tasks are displayed
    # Create dictionary to store task as a value with the task_no as the key
    task_no_dic = {
    }

    for task in tasks_file:
        full_task = task.split(",")

        task_no += 1  # increment the task_no for each task displayed
        task_no_dic[task_no] = task  # assign the task to the task_no to the dictionary

        if full_task[0] == username_input:
            print("############################################################")
            print(f"Task No.{task_no}:")
            print(f"Task:\t\t\t{full_task[1]}")
            print(f"Assigned to:\t\t {full_task[0]}")
            print(f"Date Assigned:\t\t{full_task[4]}")
            print(f"Due Date:\t\t{full_task[3]}")
            print(f"Task Complete?:\t\t{full_task[5]}")
            print(f"Task Description:\t{full_task[2]}")
            print("############################################################\n")
            tasks_printed += 1
    tasks_file.close()


    if tasks_printed > 0:  # If there are some tasks:

        edit_task_no = 0
        while edit_task_no == 0:  # User can't edit task 0
            edit_task_no = int((input("Choose a Task.No to edit (-1 to cancel): ")))

        if edit_task_no == -1:  # -1 to exit
            pass

        else:  # Any other number selected, edit that task No.
            task_choice = input("Enter 'E' to edit the task or 'M' to mark it as complete: ").lower()
        if edit_task_no != -1:
            while task_choice != 'e' and task_choice != 'm':  # Enter "e" or "m"
                print("Invalid entry, please try again.")
                task_choice = input("Enter 'E' to edit the task or 'M' to mark it as complete: ").lower()

            #=== EDIT THE TASK===
            if task_choice == 'e':
                                
                edit_menu = input('''########################################
Select one of the following Options below:
task - Change the task summary
who - Change who the task is assigned to
when - Change when the task is due
desc - Update the task desription
e - Exit
########################################
: ''').lower()

                if edit_menu == "task":
                    new_task_title = input("Enter new task summary: ")  # Get new task summary input
                    position = 1
                    edit_task(edit_task_no, new_task_title, position)  # Call function to edit the entry  
                elif edit_menu == "who":
                    new_task_assignee = input("Enter new task assignee: ")  # Get new assignee input
                    position = 0
                    edit_task(edit_task_no, new_task_assignee, position)  # Call function to edit the entry
                elif edit_menu == "when":
                    new_task_date = input("Enter new task due date: ")  # Get new task due date input
                    position = 3
                    edit_task(edit_task_no, new_task_date, position)  # Call function to edit the entry
                elif edit_menu == "desc":
                    new_task_desc = input("Enter new task description: ")  # Get new task description input
                    position = 2
                    edit_task(edit_task_no, new_task_desc, position)  # Call function to edit the entry
                elif edit_menu == "e":
                    pass
                else:
                    print("Invalid entry.")

            #=== MARK THE TASK AS COMPLETE===
            elif task_choice == 'm':
                task_confirm = input("Are you sure you want to mark this task as complete (y/n)? ")  # Mark Complete?

                while task_confirm != 'y' and task_confirm != 'n':
                    print("Invalid entry, please try again.")
                    task_confirm = input("Are you sure you want to mark this task as complete (y/n)? ")  # Confirm y/n

                if task_confirm == 'y':  # YES, CONFIRM!
                    with open("tasks.txt", "r") as tasks_file:  # Read the file
                        all_tasks = tasks_file.readlines()  # Put all lines into a list
                    
                    this_task = all_tasks[edit_task_no - 1]  # this specific task is this_task
                    this_task_split = this_task.split(",")  # Split this_task by ","

                    if this_task_split[-1] == " Yes\n":
                        print("############################################################")
                        print("This task is already marked as complete.")
                        input("############################################################\n")
                    else:
                        print("############################################################")
                        print("This task has been marked as complete!")
                        input("############################################################\n")

                    this_task_split[-1] = " Yes"  # Replace No with Yes
                    
                    updated_task = this_task_split  # updated_task is a list of all the updated task components

                    all_tasks[edit_task_no - 1] = ""  # Delete the current task info
                    for section in updated_task:  # For all parts of the updated_task
                        if section != updated_task[-1]:
                            all_tasks[edit_task_no - 1] = all_tasks[edit_task_no - 1] + f"{section},"  # Add the section to the line with a ","
                        else:
                            all_tasks[edit_task_no - 1] = all_tasks[edit_task_no - 1] + f"{section}\n"  # Leave out the "," for the last item

                    with open("tasks.txt", "w") as tasks_file:  # Write all the lines back to the file with the new line
                        for line in all_tasks:
                            tasks_file.write(line)
                    

                elif task_confirm == 'n':  # Cancel requests
                    pass


    # User has no tasks.
    if tasks_printed == 0:
        input("You have no tasks assigned to you.\nPress enter to continue: ")


def view_statistics():
    task_list = open("tasks.txt", "r")  # Open tasks.txt file as read-only
    user_list = open("user.txt", "r")  # Open user.txt file as read-only
    task_overview_file = open("task_overview.txt", "r")  # Open task_overview.txt file as read-only
    user_overview_file = open("user_overview.txt", "r")   # Open user_overview.txt file as read-only

    task_overview = task_overview_file.readlines()
    user_overview = user_overview_file.readlines()

    total_tasks = 0
    total_users = 0

    for tasks in task_list:  # Count how many tasks there are
        total_tasks += 1
    for users in user_list:  # Count how many users there are
        total_users += 1
    print("############################################################")
    print(f"There are a total of {total_tasks} tasks.")
    print(f"There are a total of {total_users} users.\n")
    print("--- task overview ---\n")
    for line in task_overview:
        print(line)
    print("--- user overview ---\n")
    for line in user_overview:
        print(line)
    print("############################################################\n")

    input("Press enter to continue...")

    task_list.close()  # Close tasks.txt
    user_list.close()  # Close user.txt
    task_overview_file.close()  # Close task_overview.txt
    user_overview_file.close()  # Close user_overview.txt


def generate_reports():
    # Create 2 new text files
    task_overview_file = open("task_overview.txt", "w")
    user_overview_file = open("user_overview.txt", "w")

    #=== TASK OVERVIEW===
    # Read tasks.txt. Store each line in a list
    with open("tasks.txt", "r") as tasks_file:
        all_tasks = tasks_file.readlines()

    # Get the total amount of tasks in tasks.txt
    total_tasks = (len(all_tasks))  

     # Get the total amount of completed tasks
    total_completed_tasks = 0  # Set to 0
    total_incomplete_tasks = 0  # Set to 0
    incomplete_tasks = []  # List of incomplete tasks that we can check if they are overdue

    # Convert the task into a list.
    for line in all_tasks:
        line_split = line.split(",")
        if line_split[-1] == " Yes\n":   # If the last index in the list is "Yes", increase completed task.
            total_completed_tasks += 1
        else:
            total_incomplete_tasks += 1  # Task is incomplete. Add it to a list of incomplete tasks.
            incomplete_tasks.append(line)
    

    overdue_tasks = []  # List of incomplete tasks that have expired
    # Check for expired tasks that are incomplete
    for task in incomplete_tasks:
        task_split = task.split(",")  # Split the task by ","
        task_due_date = task_split[3]  # Get the due date
        task_due_date = datetime.datetime.strptime(task_due_date.strip(), "%d %b %Y").date()  #Convert Due date to yyyy-mm-dd
        current_date = datetime.date.today() # get todays date yyyy-mm-dd
        if current_date > task_due_date:  # Check if task_due_date is in the past
            overdue_tasks.append(task) # It has expired. Add to list
        else:
            pass # It is not expired
    
    # % of incomplete tasks
    percent_incomplete = round((total_incomplete_tasks / total_tasks) * 100, 2)
    # % of overdue tasks
    percent_overdue = round((len(overdue_tasks) / total_tasks) * 100, 2)

    # write all stats to the file
    task_overview_file.write(f"Total number of tasks: {total_tasks}\n")
    task_overview_file.write(f"Total number of completed tasks: {total_completed_tasks}\n")
    task_overview_file.write(f"Total number of incomplete tasks: {total_incomplete_tasks}\n")
    task_overview_file.write(f"Total number of overdue tasks: {len(overdue_tasks)}\n")
    task_overview_file.write(f"Percentage of tasks incomplete: {percent_incomplete}%\n")
    task_overview_file.write(f"Percentage of tasks overdue: {percent_overdue}%")

    task_overview_file.close()

    #=== USER OVERVIEW===    
    # Read users.txt. Store each line in a list
    with open("user.txt", "r") as users_file:
        all_users = users_file.readlines()

    # Get the total amount of users
    total_users = len(all_users)

    # TOTAL NUMBER OF TASKS IS STILL total_tasks

    
    for user in all_users:
        user_tasks = 0  # Total user tasks
        complete_user_tasks = 0  # Completed user tasks
        incomplete_user_tasks = 0  # Incomplete user tasks
        overdue_user_tasks = []  # Overdue user tasks
        user_split = user.split(",")
        selected_user = user_split[0]

        user_overview_file.write(f"### {selected_user} ###\n")

        # Get all tasks and split them up into lists
        with open("tasks.txt", "r") as tasks_file:
            all_tasks = tasks_file.readlines()
        for task in all_tasks:
            task_split = task.split(",")
            selected_task = task_split[0]

            # If the tasks is assigned to the user, +1 task
            if selected_user == selected_task:
                user_tasks += 1
                # If the task is complete, +1 compelted task
                if task_split[-1] == " Yes\n":
                    complete_user_tasks += 1
                # If the task is incomplete, +1 incomplete task
                if task_split[-1] == " No\n":
                    incomplete_user_tasks += 1
                # If the task is overdue
                task_due_date = task_split[3]  # Get the due date
                task_due_date = datetime.datetime.strptime(task_due_date.strip(), "%d %b %Y").date()  #Convert Due date to yyyy-mm-dd
                current_date = datetime.date.today() # get todays date yyyy-mm-dd
                # Check if task is incomplete and overdue
                if current_date > task_due_date and task_split[-1] == " No\n":  # Check if task_due_date is in the past
                    overdue_user_tasks.append(task) # It has expired. Add to list

        # No of tasks assigned to user
        user_overview_file.write((f"Total tasks assigned to {selected_user}: {user_tasks}\n"))
        # % of all tasks assigned to this user
        if user_tasks == 0:
            user_overview_file.write((f"There are no assigned tasks to {selected_user}.\n"))
        else:
            percent_assigned = round((user_tasks / total_tasks) * 100, 2)
            user_overview_file.write((f"Percent of tasks assigned to {selected_user}: {percent_assigned}%\n"))
        # % of assigned tasks that are completed for this user
        if complete_user_tasks == 0 or user_tasks == 0:
            user_overview_file.write((f"There are no complete tasks for {selected_user}.\n"))
        else:
            percent_user_complete = round((complete_user_tasks / user_tasks) * 100, 2)
            user_overview_file.write((f"Percent of complete tasks assigned to {selected_user}: {percent_user_complete}%\n"))
        # % of assigned tasks that are incomplete for this user
        if incomplete_user_tasks == 0 or user_tasks == 0:
             user_overview_file.write((f"There are no incomplete tasks assigned to {selected_user}.\n"))
        else:
            percent_user_incomplete = round((incomplete_user_tasks / user_tasks) * 100, 2)
            user_overview_file.write((f"Percent of incomplete tasks assigned to {selected_user}: {percent_user_incomplete}%\n"))
        # % of assigned tasks that are overdue for this user
        if len(overdue_user_tasks) == 0 or user_tasks == 0:
             user_overview_file.write((f"There are no overdue tasks for {selected_user}.\n"))
        else:
            percent_user_overdue = round((len(overdue_user_tasks) / user_tasks) * 100, 2)
            user_overview_file.write((f"Percent of overdue tasks assigned to {selected_user}: {percent_user_overdue}%\n"))
    user_overview_file.close()
        

    
logged_in = False
# ====Login Section====
while not logged_in:
    username_input = input("Username: ")  # Get username input
    password_input = input("Password: ")  # Get password input
    users = open("user.txt", "r")  # Open the user.txt file as read-only

    for user in users:  # Check all usernames in user.txt
        user_check = user.split()  # Break the username and password into separate strings
        username_check = user_check[0].strip(",")  # Set the username to be checked (remove the ,)
        password_check = user_check[1]  # Set the password to be checked

        if username_input == username_check:  # if this is a valid username, check the password
            if password_input == password_check:  # if the password is also correct, trigger "logged_in"
                logged_in = True  # Logged in! continue to the next stage in the program
                users.close()  # Close the users file as it is no longer needed
                break
            else:
                print("Incorrect password! Please try again")
                break  # Go to the beginning of the while loop and ask for username and password again
        else:
            continue  # Go to the next statement

    if username_input != username_check:  # If after all usernames have been checked, finish the for loop
        print("Incorrect username. Please try again")
        continue  # Go back to the beginning of the while loop and ask for username and password again

# ====Menu Section====
while logged_in:
    if username_input == "admin":  # Check if user logged in is "admin". This shows an extra option (vs)
        menu = input('''Select one of the following Options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
gr - Generate reports (admin-only)
vs - View statistics (admin-only)
e - Exit
: ''').lower()

    else:  # any other user, normal menu. Typing "vs" will return an error.
        menu = input('''Select one of the following Options below:  
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
e - Exit
: ''').lower()

    if menu == 'r':
        if username_input != "admin":  # Only "admin" can add users
            print("Sorry, but users can only be registered by admins")
            input("Press enter to continue...")
            continue
        else:  # if it is an "admin", run the reg_user function
            reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    elif menu == 'gr' and username_input == "admin":  # Only the "admin" can run this menu option
        generate_reports()

    elif menu == 'vs' and username_input == "admin":  # Only the "admin" can run this menu option
        generate_reports()
        view_statistics()

    else:
        print("You have made a wrong choice, Please Try again")