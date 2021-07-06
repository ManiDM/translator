import secrets
import base64
import sqlite3

conn = sqlite3.connect('api_db.db', check_same_thread=False)
# def generate():
#   s1 = secrets.token_urlsafe()
#   if conn.execute("SELECT 1 FROM api_keys WHERE api = ?",[s1]).fetchone():
#     generate()
#   else:
#     conn.commit()
#     return s1

def generate(session,app_name):
  s1 = secrets.token_urlsafe()
  if conn.execute("SELECT 1 FROM normal_clients WHERE api = ?",[s1]).fetchone():
    generate()
  else:
    conn.execute("INSERT INTO normal_clients (name, username, email, app, api, request_count, max_requests)values(?,?,?,?,?,?,?)",(session['name'],session['username'],session['email'],app_name,s1,0, 150000))
    conn.commit()
    return s1