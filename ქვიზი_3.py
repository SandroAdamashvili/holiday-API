import requests
import json
import sqlite3

conn = sqlite3.connect("holidays_database.sqlite")
cursor = conn.cursor()

# 2013-2050

key = '1eba6f69c66947ce9ac261784d19bd16'
url = f'https://holidays.abstractapi.com/v1/'
while True:
    try:
        user_year = int(input("შეიყვანეთ წელი: "))
        user_month = int(input("შეიყვანეთ თვე: "))
        user_day = int(input("შეიყვანეთ რიცხვი: "))
        assert 2013 <= user_year <= 2050
        assert 1 <= user_month <= 12
        assert 1 <= user_day <= 31
        break
    except(ValueError, AssertionError):
        print("მონაცემები არასწორადაა შეყვანილი")
payload = {'api_key': key, 'country': 'GE', 'year': user_year, 'month': user_month, 'day': user_day}
r = requests.get(url, params=payload)
print(r.headers)
print(r.status_code)
res = r.json()
# print(json.dumps(res, indent=4))

with open('json.data', 'w') as file:
    json.dump(res, file, indent=4)

# cursor.execute('''CREATE TABLE holidays
# (id INTEGER PRIMARY KEY AUTOINCREMENT,
# year INT,
# month INT,
# day INT,
# info VARCHAR(200));''')

cursor.execute("INSERT INTO holidays (year, month, day, info) VALUES(?, ?, ?, ?)",
               (user_year, user_month, user_day, json.dumps(res, indent=4)))
conn.commit()
