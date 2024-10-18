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
