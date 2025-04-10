# Bank System – Python Tkinter Application

This is a desktop banking system implemented in **Python** using **Tkinter**. The application simulates a real-world banking environment with customer and employee panels, supporting user account management, secure transactions, and persistent storage via **SQLite**.

## Features
- Create and manage customer accounts
- Process deposits, withdrawals, and transfers
- Track all transactions per account
- Store data in local SQLite databases (bank2.db)
- Fully object-oriented design: separate classes for Account, Customer, Transaction, and Bank
- 
### Customer Panel
- Secure login with name and password
- View personal accounts and balances
- Deposit and withdraw money
- View complete transaction history
- View personal information (name, age, CNP)
- Export account statements to PDF

### Employee Panel
- Create new customers and accounts
- View all customers, accounts, and transactions
- Delete customers and accounts
- Export statements for any account (PDF)

## Data & Persistence

- Data is stored in a local **SQLite** database (`bank.db`)
- Includes tables for customers, accounts, and transactions
- All transactions and updates are stored persistently

## Technologies Used

- Python 3.12
- Tkinter (GUI)
- SQLite (embedded database)
- FPDF (PDF generation)
- Object-Oriented Programming


## 🚀 How to Run

1. Install dependencies:
```bash
pip install fpdf

