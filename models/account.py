from database_handler import get_connection

class Account:
    def __init__(self, account_id, customer_id, account_number, balance):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (self.balance, self.account_id))
        conn.commit()
        conn.close()

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (self.balance, self.account_id))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def create(customer_id, account_number, balance):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO accounts (customer_id, account_number, balance)
            VALUES (?, ?, ?)
        """, (customer_id, account_number, balance))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        rows = cursor.fetchall()
        conn.close()
        return [Account(*row) for row in rows]

    def __str__(self):
        return f"Account {self.account_number} | Balance: {self.balance:.2f} | Owner ID: {self.customer_id}"
