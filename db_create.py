import sqlite3  
  
con = sqlite3.connect("licenseplate.db")  
# print("Database opened successfully")  
cur=con.cursor()
cur.execute('begin transaction;')
# cur.execute("insert into User (username, password) values (?,?)", ('admin', 'password'))

# cur.execute("drop table user")
# cur.execute('''SELECT name FROM sqlite_schema 
# WHERE type = 'table' 
# AND name NOT LIKE 'sqlite_%'
# ORDER BY 1;''')
#cur.execute("create table User (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)")  
# cur.execute("select * from User")
cur.execute("delete from LicensePlate where platenumber='jaja'")
# print(cur.fetchall())
cur.execute('commit transaction;')
con.close()