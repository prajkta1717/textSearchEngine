import MySQLdb
db = MySQLdb.connect("localhost","root","root123","test" )
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
sql = "Select * from cavideos"
a = cursor.execute(sql)
print(a)
db.close()