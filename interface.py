import pyodbc
import time
#import menu

def check_choice(var):
    ava_choice = ['1','2','3','4','5','6']
    error_stat = 0
    for choice_cur in ava_choice:
        if var == choice_cur:
            error_stat = 0
            #print("ok",'\n')
            break
        else:
            error_stat = 1
    return error_stat

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=./database2.accdb;'
)
con = pyodbc.connect(conn_str)

#set up cursor
cur = con.cursor()

choice = input()

while check_choice(choice) == 0:
    if choice == '1':
        x = input()
        cur.execute(x)

        #get result
        rows = cur.fetchall()
        for x in rows:
            for y in range(len(x)):
                print(cur.description[y][0], end=' ')
                print(x[y], end='\t')
            print()

    if choice == '2':
        pass
    if choice == '6':
        break
    choice = input()
