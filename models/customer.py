from database_handler import get_connection

class Customer:
    def __init__(self, customer_id, first_name, last_name, age, password, cnp):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.password = password
        self.cnp = cnp

    @staticmethod
    def create(first_name, last_name, age, password, cnp):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customers (first_name, last_name, age, password, cnp)
            VALUES (?, ?, ?, ?, ?)
        """, (first_name, last_name, age, password, cnp))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        conn.close()
        return [Customer(*row) for row in rows]

    def __str__(self):
        return f"{self.first_name} {self.last_name} | Age: {self.age} | CNP: {self.cnp}"
