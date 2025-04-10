import tkinter as tk
from tkinter import messagebox
from models.customer import Customer
from models.account import Account
from models.transaction import Transaction
from fpdf import FPDF
from datetime import datetime


def open_customer_window():
    login_win = tk.Toplevel()
    login_win.title("Customer Login")
    login_win.geometry("350x200")

    # Login Fields
    tk.Label(login_win, text="First Name").pack()
    fname_entry = tk.Entry(login_win)
    fname_entry.pack()

    tk.Label(login_win, text="Last Name").pack()
    lname_entry = tk.Entry(login_win)
    lname_entry.pack()

    tk.Label(login_win, text="Password").pack()
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def login():
        fname = fname_entry.get()
        lname = lname_entry.get()
        password = password_entry.get()

        try:
            password = int(password)
        except ValueError:
            messagebox.showerror("Error", "Password must be a number.")
            return

        customers = Customer.get_all()
        current = None
        for c in customers:
            if c.first_name == fname and c.last_name == lname and c.password == password:
                current = c
                break

        if not current:
            messagebox.showerror("Login Failed", "Incorrect name or password.")
            return

        messagebox.showinfo("Success", f"Welcome, {current.first_name}!")
        login_win.destroy()
        show_customer_menu(current)

    tk.Button(login_win, text="Login", command=login).pack(pady=10)

def show_customer_menu(customer):
    win = tk.Toplevel()
    win.title(f"Customer Menu – {customer.first_name}")
    win.geometry("400x400")

    def view_accounts():
        accounts = Account.get_all()
        found = [a for a in accounts if str(a.customer_id) == str(customer.customer_id)]
        if not found:
            messagebox.showinfo("Accounts", "You have no accounts.")
        else:
            msg = "\n".join([f"{a.account_id} – {a.account_number} | Balance: {a.balance:.2f}" for a in found])
            messagebox.showinfo("Your Accounts", msg)

    def deposit():
        acc_id = simple_input("Account ID")
        amount = simple_input("Deposit Amount", numeric=True)
        acc = find_account(customer.customer_id, acc_id)
        if acc:
            acc.deposit(float(amount))
            Transaction.create(acc.account_id, "deposit", float(amount))
            messagebox.showinfo("Success", "Deposit successful.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def withdraw():
        acc_id = simple_input("Account ID")
        amount = simple_input("Withdraw Amount", numeric=True)
        acc = find_account(customer.customer_id, acc_id)
        if acc:
            success = acc.withdraw(float(amount))
            if success:
                Transaction.create(acc.account_id, "withdraw", float(amount))
                messagebox.showinfo("Success", "Withdrawal successful.")
            else:
                messagebox.showerror("Error", "Insufficient funds.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def view_transactions():
        accounts = Account.get_all()
        owned = [a for a in accounts if str(a.customer_id) == str(customer.customer_id)]
        all_trans = []
        for a in owned:
            all_trans += Transaction.get_by_account(a.account_id)
        if not all_trans:
            messagebox.showinfo("Transactions", "No transactions available.")
        else:
            msg = "\n".join([f"{t.timestamp} – {t.type.upper()} – {t.amount:.2f}" for t in all_trans])
            messagebox.showinfo("Transactions", msg)

    def about_me():
        info = f"Name: {customer.first_name} {customer.last_name}\nAge: {customer.age}\nCNP: {customer.cnp}"
        messagebox.showinfo("Your Info", info)

    # def export_statement():
    #     accounts = Account.get_all()
    #     owned = [a for a in accounts if str(a.customer_id) == str(customer.customer_id)]
    #     all_trans = []
    #     for a in owned:
    #         all_trans += Transaction.get_by_account(a.account_id)

    #     pdf = FPDF()
    #     pdf.add_page()
    #     pdf.set_font("Arial", size=12)
    #     pdf.cell(200, 10, txt=f"Statement for {customer.first_name} {customer.last_name}", ln=True)
    #     for t in all_trans:
    #         pdf.cell(200, 10, txt=f"{t.timestamp} – {t.type} – {t.amount}", ln=True)
    #     pdf.output(f"statement_{customer.customer_id}.pdf")
    #     messagebox.showinfo("Exported", "Statement exported successfully!")
      
    def export_statement():
        accounts = Account.get_all()
        owned = [a for a in accounts if str(a.customer_id) == str(customer.customer_id)]
        all_trans = []
        for a in owned:
            all_trans.append({
                "account": a,
                "transactions": Transaction.get_by_account(a.account_id)
            })

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        date_filename = now.strftime("%Y-%m-%d")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Antet PDF
        pdf.cell(200, 10, txt="====== CUSTOMER STATEMENT ======", ln=True)
        pdf.cell(200, 10, txt=f"Generated on: {date_str}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)

        # Info client
        pdf.cell(200, 10, txt=f"Customer ID: {customer.customer_id}", ln=True)
        pdf.cell(200, 10, txt=f"Name: {customer.first_name} {customer.last_name}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {customer.age}", ln=True)
        pdf.cell(200, 10, txt=f"CNP: {customer.cnp}", ln=True)
        pdf.cell(200, 10, txt=f"Password: {customer.password}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)

        if not owned:
            pdf.cell(200, 10, txt="This customer has no accounts.", ln=True)
        else:
            for group in all_trans:
                acc = group["account"]
                txs = group["transactions"]

                pdf.set_font("Arial", style='B', size=12)
                pdf.cell(200, 10, txt="--- Account ---", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Account ID: {acc.account_id}", ln=True)
                pdf.cell(200, 10, txt=f"Account Number: {acc.account_number}", ln=True)
                pdf.cell(200, 10, txt=f"Balance: {acc.balance:.2f}", ln=True)

                pdf.set_font("Arial", style='B', size=12)
                pdf.cell(200, 10, txt="--- Transactions ---", ln=True)
                pdf.set_font("Arial", size=12)
                if not txs:
                    pdf.cell(200, 10, txt="No transactions.", ln=True)
                else:
                    for t in txs:
                        pdf.cell(200, 10, txt=f"{t.timestamp} | {t.id} | {t.type.upper()} | Amount: {t.amount:.2f}", ln=True)
                pdf.cell(200, 10, txt="", ln=True)

        pdf.cell(200, 10, txt="===============================", ln=True)

        # Nume fișier final
        file_name = f"statement_{customer.first_name}_{date_filename}.pdf"
        pdf.output(file_name)
        messagebox.showinfo("Exported", f"Statement saved as {file_name}")

     # Button Menu
    tk.Button(win, text="1. View My Accounts", command=view_accounts).pack(fill='x')
    tk.Button(win, text="2. Deposit", command=deposit).pack(fill='x')
    tk.Button(win, text="3. Withdraw", command=withdraw).pack(fill='x')
    tk.Button(win, text="4. See your transactions", command=view_transactions).pack(fill='x')
    tk.Button(win, text="5. About me", command=about_me).pack(fill='x')
    tk.Button(win, text="6. Export Statement PDF", command=export_statement).pack(fill='x')
    tk.Button(win, text="7. Exit", command=win.destroy).pack(fill='x')

# Helper functions
def simple_input(title, numeric=False):
    top = tk.Toplevel()
    top.title(title)
    val = tk.StringVar()

    tk.Label(top, text=title).pack()
    entry = tk.Entry(top, textvariable=val)
    entry.pack()
    entry.focus()

    def submit():
        top.destroy()

    tk.Button(top, text="OK", command=submit).pack()
    top.wait_window()
    value = val.get()
    if numeric:
        try:
            return float(value)
        except ValueError:
            return 0
    return value

def find_account(customer_id, account_id):
    accounts = Account.get_all()
    for acc in accounts:
        if str(acc.customer_id) == str(customer_id) and str(acc.account_id) == str(account_id):
            return acc
    return None
