from database_handler import get_connection

class Transaction:
    def __init__(self, id, account_id, type, amount, timestamp):
        self.id = id
        self.account_id = account_id
        self.type = type
        self.amount = amount
        self.timestamp = timestamp

    def get_id(self):
        return self.id

    def get_account_id(self):
        return self.account_id

    def get_type(self):
        return self.type

    def get_amount(self):
        return self.amount

    def get_timestamp(self):
        return self.timestamp

    @staticmethod
    def create(account_id, type, amount):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (account_id, type, amount)
            VALUES (?, ?, ?)
        """, (account_id, type, amount))

        # Update balance
        if type == 'deposit':
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        elif type == 'withdraw':
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_account(account_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE account_id = ?", (account_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Transaction(*row) for row in rows]

    def __str__(self):
        return f"[{self.timestamp}] {self.type.upper()} {self.amount:.2f} (Account {self.account_id})"
