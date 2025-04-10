import tkinter as tk
from tkinter import messagebox
from models.customer import Customer
from models.account import Account
from models.transaction import Transaction
from fpdf import FPDF
from datetime import datetime


def open_employee_window():
    win = tk.Toplevel()
    win.title("Employee Panel")
    win.geometry("400x500")

    def create_customer():
        form = tk.Toplevel(win)
        form.title("Create New Customer")
        entries = {}

        for label in ["ID", "First Name", "Last Name", "Age", "Password", "CNP"]:
            tk.Label(form, text=label).pack()
            entry = tk.Entry(form)
            entry.pack()
            entries[label] = entry

        def submit():
            id_ = entries["ID"].get()
            fn = entries["First Name"].get()
            ln = entries["Last Name"].get()
            age = int(entries["Age"].get())
            pw = int(entries["Password"].get())
            cnp = entries["CNP"].get()

            all_customers = Customer.get_all()
            if any(c.customer_id == id_ for c in all_customers):
                messagebox.showerror("Error", "Customer already exists.")
            else:
                Customer.create_custom(id_, fn, ln, age, pw, cnp)
                messagebox.showinfo("Success", "Customer created successfully.")
            form.destroy()

        tk.Button(form, text="Submit", command=submit).pack()

    def create_account():
        form = tk.Toplevel(win)
        form.title("Create New Account")
        entries = {}

        for label in ["Account ID", "Customer ID", "Account Number", "Initial Balance"]:
            tk.Label(form, text=label).pack()
            entry = tk.Entry(form)
            entry.pack()
            entries[label] = entry

        def submit():
            acc_id = entries["Account ID"].get()
            cust_id = entries["Customer ID"].get()
            acc_num = entries["Account Number"].get()
            balance = float(entries["Initial Balance"].get())

            all_accounts = Account.get_all()
            if any(a.account_id == acc_id for a in all_accounts):
                messagebox.showerror("Error", "Account already exists.")
            else:
                Account.create_custom(acc_id, cust_id, acc_num, balance)
                messagebox.showinfo("Success", "Account created successfully.")
            form.destroy()

        tk.Button(form, text="Submit", command=submit).pack()

    def show_customers():
        customers = Customer.get_all()
        msg = "\n".join([f"{c.customer_id} - {c.first_name} {c.last_name}" for c in customers])
        messagebox.showinfo("All Customers", msg or "No customers found.")

    def show_accounts():
        accounts = Account.get_all()
        msg = "\n".join([f"{a.account_id} - {a.account_number} | Balance: {a.balance}" for a in accounts])
        messagebox.showinfo("All Accounts", msg or "No accounts found.")

    def show_transactions():
        accounts = Account.get_all()
        all_trans = []
        for a in accounts:
            all_trans += Transaction.get_by_account(a.account_id)
        if not all_trans:
            messagebox.showinfo("Transactions", "No transactions available.")
        else:
            msg = "\n".join([f"{t.timestamp} – {t.type.upper()} – {t.amount:.2f} (Account: {t.account_id})" for t in all_trans])
            messagebox.showinfo("Transactions", msg)

    def delete_customer():
        form = tk.Toplevel(win)
        form.title("Delete Customer")

        tk.Label(form, text="Customer ID").pack()
        entry = tk.Entry(form)
        entry.pack()

        def delete():
            cust_id = entry.get()
            Customer.delete_by_id(cust_id)
            messagebox.showinfo("Deleted", f"Customer {cust_id} deleted (and associated data).")
            form.destroy()

        tk.Button(form, text="Delete", command=delete).pack()

    def delete_account():
        form = tk.Toplevel(win)
        form.title("Delete Account")

        tk.Label(form, text="Account ID").pack()
        entry = tk.Entry(form)
        entry.pack()

        def delete():
            acc_id = entry.get()
            Account.delete_by_id(acc_id)
            messagebox.showinfo("Deleted", f"Account {acc_id} deleted.")
            form.destroy()

        tk.Button(form, text="Delete", command=delete).pack()

    # def generate_pdf():
    #     form = tk.Toplevel(win)
    #     form.title("Export Statement")

    #     tk.Label(form, text="Account ID").pack()
    #     entry = tk.Entry(form)
    #     entry.pack()

    #     def export():
    #         account_id = entry.get()
    #         transactions = Transaction.get_by_account(account_id)
    #         pdf = FPDF()
    #         pdf.add_page()
    #         pdf.set_font("Arial", size=12)
    #         pdf.cell(200, 10, txt=f"Statement for Account {account_id}", ln=True)
    #         for t in transactions:
    #             pdf.cell(200, 10, txt=f"{t.timestamp} – {t.type} – {t.amount}", ln=True)
    #         pdf.output(f"statement_account_{account_id}.pdf")
    #         messagebox.showinfo("Success", f"Exported to statement_account_{account_id}.pdf")
    #         form.destroy()

    #     tk.Button(form, text="Export", command=export).pack()

    
    def generate_pdf():
        form = tk.Toplevel()
        form.title("Export Statement")

        tk.Label(form, text="Account ID").pack()
        entry = tk.Entry(form)
        entry.pack()

        def export():
            account_id = entry.get()
            account = None

            # Caută contul
            for a in Account.get_all():
                if str(a.account_id) == str(account_id):
                    account = a
                    break

            if not account:
                messagebox.showerror("Error", "Account not found.")
                return

            transactions = Transaction.get_by_account(account_id)

            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")
            date_filename = now.strftime("%Y-%m-%d")

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="====== ACCOUNT STATEMENT ======", ln=True)
            pdf.cell(200, 10, txt=f"Generated on: {date_str}", ln=True)
            pdf.cell(200, 10, txt="", ln=True)

            # Info cont
            pdf.cell(200, 10, txt=f"Account ID: {account.account_id}", ln=True)
            pdf.cell(200, 10, txt=f"Account Number: {account.account_number}", ln=True)
            pdf.cell(200, 10, txt=f"Balance: {account.balance:.2f}", ln=True)
            pdf.cell(200, 10, txt="", ln=True)

            # Tranzacții
            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, txt="--- Transactions ---", ln=True)
            pdf.set_font("Arial", size=12)

            if not transactions:
                pdf.cell(200, 10, txt="No transactions available.", ln=True)
            else:
                for t in transactions:
                    pdf.cell(200, 10, txt=f"{t.timestamp} | {t.id} | {t.type.upper()} | Amount: {t.amount:.2f}", ln=True)

            pdf.cell(200, 10, txt="", ln=True)
            pdf.cell(200, 10, txt="===============================", ln=True)

            file_name = f"statement_account_{account_id}_{date_filename}.pdf"
            pdf.output(file_name)
            messagebox.showinfo("Success", f"Exported to {file_name}")
            form.destroy()

        tk.Button(form, text="Export", command=export).pack(pady=10)


    # Button menu
    tk.Button(win, text="1. Create New Customer", command=create_customer).pack(fill='x')
    tk.Button(win, text="2. Create New Account", command=create_account).pack(fill='x')
    tk.Button(win, text="3. Show All Customers", command=show_customers).pack(fill='x')
    tk.Button(win, text="4. Show All Accounts", command=show_accounts).pack(fill='x')
    tk.Button(win, text="5. Show All Transactions", command=show_transactions).pack(fill='x')
    tk.Button(win, text="6. Delete Customer", command=delete_customer).pack(fill='x')
    tk.Button(win, text="7. Delete Account", command=delete_account).pack(fill='x')
    tk.Button(win, text="8. Export Statement PDF", command=generate_pdf).pack(fill='x')
    tk.Button(win, text="Exit", command=win.destroy).pack(pady=10)
