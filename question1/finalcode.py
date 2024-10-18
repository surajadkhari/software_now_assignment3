import tkinter as tk
from tkinter import simpledialog, messagebox
import csv
from datetime import datetime

# Base class for handling employee management
class BaseAttendance:
    def __init__(self, file_path):
        self.file_path = file_path
        self.shift_flag = []
        self.shift_start_time = []
    
    def read_employees_from_csv(self):
        """Read employees from a CSV file and initialize flags."""
        employees = []
        try:
            with open(self.file_path, mode='r') as file:
                csv_reader = csv.DictReader(file, delimiter='|')
                for row in csv_reader:
                    employees.append((row['NAME'], row['EMPLOYEEID']))
                    self.shift_flag.append(False)
                    self.shift_start_time.append(None)
        except FileNotFoundError:
            messagebox.showerror("Error", "Employee list file not found!")
        return employees

    def write_employee_to_csv(self, name, emp_id):
        """Add a new employee to the CSV file and create a new attendance CSV."""
        try:
            with open(self.file_path, mode='a', newline='') as file:
                csv_writer = csv.writer(file, delimiter='|')
                csv_writer.writerow([name, emp_id])
            
            # Create a new CSV file for this employee's attendance log
            file_path = f"E:/Software_Now/Assignment3/attendance_logSheet/{name}.csv"
            self.create_employee_csv(file_path)
            messagebox.showinfo("Success", f"Employee {name} added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee: {str(e)}")
    
    def remove_employee_from_csv(self, emp_id):
        """Remove an employee from the CSV file."""
        updated_employees = []
        try:
            with open(self.file_path, mode='r') as file:
                csv_reader = csv.DictReader(file, delimiter='|')
                for row in csv_reader:
                    if row['EMPLOYEEID'] != emp_id:
                        updated_employees.append((row['NAME'], row['EMPLOYEEID']))

            with open(self.file_path, mode='w', newline='') as file:
                csv_writer = csv.writer(file, delimiter='|')
                csv_writer.writerow(['NAME', 'EMPLOYEEID'])
                csv_writer.writerows(updated_employees)
            messagebox.showinfo("Success", f"Employee with ID {emp_id} removed successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "Employee list file not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove employee: {str(e)}")

    def create_employee_csv(self, file_path):
        """Creates a new CSV file for the employee's attendance log with appropriate headers."""
        try:
            with open(file_path, mode='w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['Date', 'Start Time', 'End Time', 'Duration'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create CSV file: {str(e)}")
class AdminAttendance(BaseAttendance):
    def __init__(self, file_path):
        super().__init__(file_path)

    def reset_to_initial_screen(self):
        employees = self.read_employees_from_csv()
        
        for widget in root.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(root, bg="lightgray", height=50)
        header_frame.pack(fill="x")
        header_label = tk.Label(header_frame, text="CDU Attendance System", bg="lightgray", font=("Arial", 14, "bold"))
        header_label.pack(pady=10)

        employee_frame = tk.Frame(root)
        employee_frame.pack(pady=20)

        for i, (name, emp_id) in enumerate(employees):
            employee_button = tk.Button(employee_frame, text=f"{name} (ID: {emp_id})", relief="solid", width=30, height=2)
            employee_button.pack(pady=5)
            employee_button.bind("<Button-1>", lambda e, emp_name=name, emp_id=emp_id, idx=i: self.on_employee_click(emp_name, emp_id, idx))

        admin_button = tk.Button(root, text="(+/-)", width=10, command=self.admin_login)
        admin_button.pack(side="bottom", pady=10)

    def on_employee_click(self, employee_name, correct_emp_id, index):
        entered_emp_id = simpledialog.askstring("Employee ID Validation", f"Enter Employee ID for {employee_name}:")
        if entered_emp_id == correct_emp_id:
            show_employee_screen(employee_name, index)
        else:
            messagebox.showerror("Error", "Incorrect Employee ID!")
            self.reset_to_initial_screen()

    def admin_login(self):
        admin_username = simpledialog.askstring("Admin Login", "Enter Admin Username:")
        admin_password = simpledialog.askstring("Admin Login", "Enter Admin Password:", show='*')
        try:
            with open("credentials.txt", "r") as file:
                credentials = file.readlines()
                stored_username = credentials[0].strip()
                stored_password = credentials[1].strip()

                if admin_username == stored_username and admin_password == stored_password:
                    self.show_admin_screen()
                else:
                    messagebox.showerror("Login Failed", "Invalid credentials, please try again.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Credentials file not found!")
    def show_admin_screen(self):
        for widget in root.winfo_children():
            widget.destroy()

        add_employee_button = tk.Button(root, text="Add Employee", width=20, bg="lightgreen", command=self.add_employee)
        add_employee_button.place(x=50, y=100)

        remove_employee_button = tk.Button(root, text="Remove Employee", width=20, bg="red", command=self.remove_employee)
        remove_employee_button.place(x=200, y=100)

        back_button = tk.Button(root, text="Back", bg="lightblue", width=10, command=self.reset_to_initial_screen)
        back_button.place(x=20, y=250)

    def add_employee(self):
        employee_name = simpledialog.askstring("Add Employee", "Enter Employee Name:")
        employee_id = simpledialog.askstring("Add Employee", "Enter Employee ID:")
        if employee_name and employee_id:
            self.write_employee_to_csv(employee_name, employee_id)
            self.reset_to_initial_screen()
        else:
            messagebox.showwarning("Input Error", "Both Name and Employee ID are required.")

    def remove_employee(self):
        employee_id = simpledialog.askstring("Remove Employee", "Enter Employee ID to Remove:")
        if employee_id:
            self.remove_employee_from_csv(employee_id)
            self.reset_to_initial_screen()
        else:
            messagebox.showwarning("Input Error", "Employee ID is required.")


# Function to display the employee's screen dynamically after validation
def show_employee_screen(employee, index):
    """Display the screen based on whether the employee's shift has started or not."""
    for widget in root.winfo_children():
        widget.destroy()

    if attendance_system.shift_flag[index]:
        end_shift_screen(employee, index)
    else:
        start_shift_screen(employee, index)


# Function to display the "Start Shift" screen
def start_shift_screen(employee, index):
    """Displays the screen for starting the shift."""
    employee_label = tk.Label(root, text=f"{employee}", relief="solid", width=30)
    employee_label.pack(pady=20)

    date_label = tk.Label(root, text=datetime.now().strftime("%d/%m/%y"), width=15)
    date_label.place(x=100, y=120)

    start_shift_button = tk.Button(root, text="Start Shift", bg="lightgreen", width=15, command=lambda: start_shift(index))
    start_shift_button.place(x=200, y=120)


# Function to start the shift
def start_shift(index):
    """Handles the start of an employee's shift."""
    attendance_system.shift_flag[index] = True
    attendance_system.shift_start_time[index] = datetime.now()
    attendance_system.reset_to_initial_screen()


# Function to display the "End Shift" screen
def end_shift_screen(employee, index):
    """Displays the screen for ending the shift and calculating duration."""
    now = datetime.now()
    duration = now - attendance_system.shift_start_time[index]
    intial_time = attendance_system.shift_start_time[index]
    now_time_str = now.strftime("%H:%M")
    date_str = now.strftime("%Y/%m/%d")
    total_minutes = int(duration.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    duration_str = f"{hours:02}:{minutes:02}"

    file_path = f"E:/Software_Now/Assignment3/attendance_logSheet/{employee}.csv"

    employee_label = tk.Label(root, text=f"{employee}", relief="solid", width=30)
    employee_label.pack(pady=20)

    date_label = tk.Label(root, text=intial_time.strftime("%d/%m/%y"),  width=15)
    date_label.place(x=90, y=100)

    start_time_label = tk.Label(root, text=f"Start Time: {intial_time.strftime('%H:%M')}", relief="solid", width=15)
    start_time_label.place(x=50, y=200)

    current_time_label = tk.Label(root, text=f"Time Now: {now.strftime('%H:%M')}", relief="solid", width=15)
    current_time_label.place(x=150, y=200)

    duration_label = tk.Label(root, text=f"Duration: {duration_str}", relief="solid", width=15)
    duration_label.place(x=250, y=200)

    end_shift_button = tk.Button(root, text="End Shift", bg="lightgreen", width=15,
                                 command=lambda: end_shift(index, file_path, date_str, intial_time.strftime('%H:%M'),
                                                           now_time_str, duration_str))
    end_shift_button.place(x=200, y=100)


# Function to handle ending the shift
def end_shift(index, file_path, date_str, intitial_time_str, now_time_str, duration_str):
    """Handles the end of an employee's shift."""
    attendance_system.shift_flag[index] = False
    attendance_system.reset_to_initial_screen()

    new_row = {
        "Date": date_str,
        "Start Time": intitial_time_str,
        "End Time": now_time_str,
        "Duration": duration_str
    }

    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Start Time", "End Time", "Duration"])
        writer.writerow(new_row)


# Tkinter root setup
root = tk.Tk()
root.title("Employee Attendance System")
root.geometry("400x300")

# Initialize the attendance system (Admin for this example)
attendance_system = AdminAttendance(r"E:/Software_Now/Assignment3/employeelist.txt")
attendance_system.reset_to_initial_screen()

root.mainloop()

