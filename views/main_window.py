import tkinter as tk
from views.customer_window import open_customer_window
from views.employee_window import open_employee_window
from database_handler import init_db

def launch_app():
    init_db()
    root = tk.Tk()
    root.title("Bank System")
    root.geometry("300x200")

    btn_customer = tk.Button(root, text="Customer Access", command=open_customer_window)
    btn_customer.pack(pady=20)

    btn_employee = tk.Button(root, text="Employee Access", command=open_employee_window)
    btn_employee.pack(pady=20)

    root.mainloop()
