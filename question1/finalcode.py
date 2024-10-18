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
