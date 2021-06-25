import pypyodbc
from datetime import date
import os
class AzureDB:
    dsn = f'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{os.getenv("DB_SERVER")},{os.getenv("PORT")};Database={os.getenv("DATABASE")};Uid={os.getenv("user")};Pwd={os.getenv("PASS")};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()
    def finalize(self):
        if self.conn:
            self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()
    def __enter__(self):
        return self
    def azureGetData(self):
        try:
            self.cursor.execute("SELECT name,comment,date from guestbook")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit (1)
    def azureAddData(self,name_,comment):
        self.cursor.execute(f"INSERT into guestbook (name, comment,date ) values ('{name_}', '{comment}','{date.today().strftime('%Y%m%d')}')")
        self.conn.commit()
    def azureDeleteData(self):
        self.cursor.execute("DELETE FROM data WHERE name = 'Adam'")
        self.conn.commit()
