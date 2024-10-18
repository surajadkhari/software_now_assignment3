import tkinter as tk
from tkinter import simpledialog, messagebox
import csv
from datetime import datetime


def create_employee_csv(file_path):
    """
    Creates a CSV file with headers: Date, Start time, End Time, Duration.

    :param file_path: The path where the CSV will be created.
    """
    try:
        # Open the file in write mode
        with open(file_path, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            
            # Write the headers
            csv_writer.writerow(['Date', 'Start time', 'End Time', 'Duration'])
        
        print(f"CSV file created successfully: {file_path}")
    
    except Exception as e:
        print(f"Error creating CSV file: {str(e)}")

# Initialize the shift flag array (this will be dynamically updated based on the CSV file size)
shift_flag = []
shift_start_time = []  # To store start time for each employee

# Function to read employees from the CSV file
def read_employees_from_csv():
    employees = []  # List to store employee names and IDs
    try:
        with open(r"E:/Software_Now/Assignment3/employeelist.txt", mode='r') as file:
            csv_reader = csv.DictReader(file, delimiter='|')  # Use pipe as the delimiter
            for row in csv_reader:
                employees.append((row['NAME'], row['EMPLOYEEID']))  # Append tuple (NAME, EMPLOYEEID)
                shift_flag.append(False)  # Initialize shift flag for each employee
                shift_start_time.append(None)  # Initialize the start time for each employee
    except FileNotFoundError:
        messagebox.showerror("Error", "Employee list file not found!")
    return employees

# Function to write a new employee to the CSV file
def write_employee_to_csv(name, emp_id):
    try:
        with open(r"E:/Software_Now/Assignment3/employeelist.txt", mode='a', newline='') as file:
            csv_writer = csv.writer(file, delimiter='|')
            csv_writer.writerow([name, emp_id])  # Write new employee to CSV
        messagebox.showinfo("Success", f"Employee {name} added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add employee: {str(e)}")

# Function to remove an employee from the CSV file
def remove_employee_from_csv(emp_id):
    updated_employees = []
    try:
        # Read the current employees from the CSV
        with open(r"E:/Software_Now/Assignment3/employeelist.txt", mode='r') as file:
            csv_reader = csv.DictReader(file, delimiter='|')
            for row in csv_reader:
                if row['EMPLOYEEID'] != emp_id:  # Skip the employee to be removed
                    updated_employees.append((row['NAME'], row['EMPLOYEEID']))

        # Write the updated employee list back to the CSV
        with open(r"E:/Software_Now/Assignment3/employeelist.txt", mode='w', newline='') as file:
            csv_writer = csv.writer(file, delimiter='|')
            csv_writer.writerow(['NAME', 'EMPLOYEEID'])  # Write the headers back
            csv_writer.writerows(updated_employees)  # Write the remaining employees

        messagebox.showinfo("Success", f"Employee with ID {emp_id} removed successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", "Employee list file not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove employee: {str(e)}")

# Function to reset the screen to the initial state (employee selection screen)
def reset_to_initial_screen():
    employees = read_employees_from_csv()  # Read the employee list from CSV

    # Clear the current window of any existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Recreate the header frame and label
    header_frame = tk.Frame(root, bg="lightgray", height=50)  # Create a gray frame
    header_frame.pack(fill="x")  # Expand the frame horizontally to fit the window
    header_label = tk.Label(header_frame, text="Employee Attendance System", bg="lightgray", font=("Arial", 14, "bold"))
    header_label.pack(pady=10)  # Add the label to the header with padding

    # Recreate the employee selection frame
    employee_frame = tk.Frame(root)  # Create a frame for employee-related widgets
    employee_frame.pack(pady=20)  # Add padding around the employee buttons

    # Create labels for employees dynamically from the CSV file
    for i, (name, emp_id) in enumerate(employees):  # Loop through the list of employees
        # Create a button for each employee
        employee_button = tk.Button(employee_frame, text=f"{name} (ID: {emp_id})", relief="solid", width=30, height=2)
        # Position the employee buttons with padding between them
        employee_button.pack(pady=5)
        # Bind the button so that it responds to click events (opens the employee's screen)
        employee_button.bind("<Button-1>", lambda e, emp_name=name, emp_id=emp_id, idx=i: on_employee_click(emp_name, emp_id, idx))

    # Create a button for admin access at the bottom center
    admin_button = tk.Button(root, text="(+/-)", width=10, command=admin_login)
    admin_button.pack(side="bottom", pady=10)  # Position the button at the bottom with padding

# Function to display the employee's screen dynamically after validation
def show_employee_screen(employee, index):
    # Clear the current window of any existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Check if the employee's shift is ongoing
    if shift_flag[index]:
        # Display the "End Shift" screen
        end_shift_screen(employee, index)
    else:
        # Display the regular "Start Shift" screen
        start_shift_screen(employee, index)

# Function to display the "Start Shift" screen
def start_shift_screen(employee, index):
    # Create a label to display the selected employee's name
    employee_label = tk.Label(root, text=f"{employee}", relief="solid", width=30)
    employee_label.pack(pady=20)  # Add the label to the window with padding

    # Create a label to display the current date
    date_label = tk.Label(root, text=datetime.now().strftime("%d/%m/%y"), width=15)
    date_label.place(x=100, y=120)  # Position the date label at specific coordinates

    # Create a button labeled "Start Shift" to simulate starting an employee's shift
    start_shift_button = tk.Button(root, text="Start Shift", bg="lightgreen", width=15, command=lambda: start_shift(index))
    start_shift_button.place(x=200, y=120)  # Position the button below the date label

# Function to display the "End Shift" screen
def end_shift_screen(employee, index):
    now = datetime.now()  # Get the current time
    duration = now - shift_start_time[index]  # Calculate the duration of the shift
    intial_time=shift_start_time[index]
    now_time_str = now.strftime("%H:%M")
    date_str = now.strftime("%Y/%m/%d")
    total_minutes = int(duration.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

# Format as "HH:MM"
    duration_str = f"{hours:02}:{minutes:02}"
    intitial_time_str=now.strftime("%H:%M")

    file_path = f"E:/Software_Now/Assignment3/attendance_logSheet/{employee}.csv"

    # Create a label to display the selected employee's name
    employee_label = tk.Label(root, text=f"{employee}", relief="solid", width=30)
    employee_label.pack(pady=20)

    # Create a date label
    date_label = tk.Label(root, text=shift_start_time[index].strftime("%d/%m/%y"), relief="solid", width=15)
    date_label.place(x=50, y=100)

    # Create labels for Start Time, Time Now, and Duration
    start_time_label = tk.Label(root, text=f"Start Time: {shift_start_time[index].strftime('%H:%M')}", relief="solid", width=15)
    start_time_label.place(x=50, y=200)

    current_time_label = tk.Label(root, text=f"Time Now: {now.strftime('%H:%M')}", relief="solid", width=15)
    current_time_label.place(x=150, y=200)

    duration_label = tk.Label(root, text=f"Duration: {duration.seconds // 3600}:{(duration.seconds % 3600) // 60}", relief="solid", width=15)
    duration_label.place(x=250, y=200)

    # Create an "End Shift" button
    end_shift_button = tk.Button(root, text="End Shift", bg="lightgreen", width=15, command=lambda: end_shift(index,file_path,date_str,intitial_time_str,now_time_str,duration_str))
    end_shift_button.place(x=150, y=120)  # Position the button at specific coordinates

# Function to handle when the shift starts
def start_shift(index):
    shift_flag[index] = True  # Set the flag to True, indicating the shift has started
    shift_start_time[index] = datetime.now()  # Record the start time of the shift
    reset_to_initial_screen()  # Go back to the employee selection screen

# Function to handle when the shift ends
def end_shift(index,file_path,date_str,intitial_time_str,now_time_str,duration_str):
    shift_flag[index] = False  # Set the flag back to False, indicating the shift has ended
    reset_to_initial_screen()  # Go back to the employee selection screen
    new_row = {
    "Date": date_str,
    "Start Time": intitial_time_str,
    "End Time": now_time_str,
    "Duration": duration_str,}
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Start Time", "End Time", "Duration"])
        writer.writerow(new_row)  # Write the new row

# Function to handle click events for any employee
def on_employee_click(employee_name, correct_emp_id, index):
    # Prompt the user to enter the Employee ID for validation
    entered_emp_id = simpledialog.askstring("Employee ID Validation", f"Enter Employee ID for {employee_name}:")

    # Validate the entered ID against the correct Employee ID
    if entered_emp_id == correct_emp_id:
        # If the ID matches, proceed to the employee screen
        show_employee_screen(employee_name, index)
    else:
        # If the ID does not match, show an error and return to the initial screen
        messagebox.showerror("Error", "Incorrect Employee ID!")
        reset_to_initial_screen()

# Function to authenticate the admin by reading credentials from a file
def admin_login():
    # Prompt for admin credentials
    admin_username = simpledialog.askstring("Admin Login", "Enter Admin Username:")
    admin_password = simpledialog.askstring("Admin Login", "Enter Admin Password:", show='*')  # Mask the password

    # Read credentials from a text file and verify
    try:
        with open("credentials.txt", "r") as file:
            credentials = file.readlines()
            stored_username = credentials[0].strip()
            stored_password = credentials[1].strip()

            if admin_username == stored_username and admin_password == stored_password:
                show_admin_screen()  # If credentials are correct, show the admin options
            else:
                messagebox.showerror("Login Failed", "Invalid credentials, please try again.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Credentials file not found!")

# Function to show the admin screen with options to add/remove employees
def show_admin_screen():
    # Clear the current window of any existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create buttons for adding and removing employees
    add_employee_button = tk.Button(root, text="Add Employee", width=20, relief="solid", command=add_employee)
    add_employee_button.place(x=100, y=100)

    remove_employee_button = tk.Button(root, text="Remove Employee", width=20, relief="solid", command=remove_employee)
    remove_employee_button.place(x=250, y=100)

    # Back button to return to the main screen
    back_button = tk.Button(root, text="Back", bg="lightblue", width=10, command=reset_to_initial_screen)
    back_button.place(x=20, y=250)

# Function to add a new employee by prompting admin for details
def add_employee():
    employee_name = simpledialog.askstring("Add Employee", "Enter Employee Name:")
    employee_id = simpledialog.askstring("Add Employee", "Enter Employee ID:")
    file_path = f"E:/Software_Now/Assignment3/attendance_logSheet/{employee_name}.csv"
    create_employee_csv(file_path)

    if employee_name and employee_id:
        write_employee_to_csv(employee_name, employee_id)  # Write the new employee to the CSV
        reset_to_initial_screen()  # Refresh the screen to show the new employee
    else:
        messagebox.showwarning("Input Error", "Both Name and Employee ID are required.")

# Function to remove an employee by prompting admin for Employee ID
def remove_employee():
    employee_id = simpledialog.askstring("Remove Employee", "Enter Employee ID to Remove:")

    if employee_id:
        remove_employee_from_csv(employee_id)  # Remove the employee from the CSV
        reset_to_initial_screen()  # Refresh the screen to show the updated employee list
    else:
        messagebox.showwarning("Input Error", "Employee ID is required.")

# Create the main window
root = tk.Tk()  # Initialize the main window
root.title("Employee Attendance System")  # Set the window title
root.geometry("400x300")  # Set the window size to 400x300 pixels

# Initialize the screen with employee selection
reset_to_initial_screen()

# Run the application by entering the Tkinter event loop
root.mainloop()
