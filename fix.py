import pyodbc
import time
#import menu

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=./database2.accdb;'
)
con = pyodbc.connect(conn_str)
cur = con.cursor()

x = input()

cur.execute(x)
rows = cur.fetchall()

for x in rows:
    for y in range(len(x)):
        print(cur.description[y][0], end=' ')
        print(x[y], end='\t')
    print()
