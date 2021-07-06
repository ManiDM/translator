import sqlite3

conn = sqlite3.connect('api_db.db', check_same_thread=False)
# # conn.execute("UPDATE api_keys SET max_requests = 150000")
# # conn.commit()
# # conn.execute('''ALTER TABLE api_keys ADD COLUMN name text, username text primary key, email text, password text,app text;''')
# # conn.execute('''DELETE FROM api_keys WHERE request_count=0''')

# # cursor = conn.execute(''' SELECT api,request_count,max_requests from api_keys;''')
# cursor = conn.execute('''SELECT * from api_keys''')
# for row in cursor:
#   print(row)
# conn.close()

# conn.execute('''CREATE TABLE normal_clients( 
#   	name text, 
#   	username text primary key, 
#   	email text, 
#   	password text, 
#   	app text, 
#   	api text, 
#   	request_count integer, 
#   	max_requests integer
# );''')
# print("Table created successfully")
# conn.commit()

cursor = conn.execute('''SELECT * from normal_clients''')
for row in cursor:
  print(row)
conn.close()
