import sqlite3  
  
con = sqlite3.connect("database.db")  
# print("Database opened successfully")  
cur=con.cursor()
# cur.execute('begin transaction;')
# cur.execute("insert into LicensePlate (name, address, phone, platenumber, isdeleted) values (?,?,?,?,?)", ('Soumyadeep', 'Hyderabad', '9546555884', 'JH05BU2017', '0'))
#cur.execute("drop table LicensePlate")
# cur.execute('''SELECT name FROM sqlite_schema 
# WHERE type = 'table' 
# AND name NOT LIKE 'sqlite_%'
# ORDER BY 1;''')
# cur.execute('drop table LicensePlate')
# cur.execute("create table LicensePlate (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address TEXT, phone TEXT, platenumber TEXT NOT NULL UNIQUE, isdeleted TEXT NOT NULL)")  
cur.execute("select * from LicensePlate")
print(cur.fetchall())
# cur.execute('commit transaction;')

  
con.close()