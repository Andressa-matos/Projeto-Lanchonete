import sqlite3

conn = sqlite3.connect("UserData.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Usuario TEXT NOT NULL,
    Password TEXT NOT NULL
);
""")

# cadastroUsuario()
