import pyodbc
import time
import datetime


# import menu

now = datetime.datetime.today()

today = "#{}/{}/{}#".format(now.strftime("%d"), now.strftime("%m"), now.strftime("%Y"))
print('today\'s date: {}'.format(today))

def check_choice(var):
    ava_choice = ['1', '2', '3', '4', '5', '6']
    error_stat = 0
    for choice_cur in ava_choice:
        if var == choice_cur:
            error_stat = 0
            # print("ok",'\n')
            break
        else:
            error_stat = 1
    return error_stat


def first_menu():
    print("Welcome to Hunter store's sales system")
    print("-----------------------------------------")
    print("[*]Please select the type of view.")
    print("[1]Sales view")
    print("[2]Administrator view")


def admin_menu():
    print('Please select the following option.')
    print("[1] Print data by using sql")
    print("[2] Show all trade records within specific date")
    print("[3] Crew management")
    print("[4] Position management")
    print("[5] Product management")
    print("[6] Exit the system")
    # print("[]",end='\n')


def sales_menu():
    print('Please select the following option.')
    print('[1] Print out prise by searching product id')
    print('[2] Make transaction')
    print('[3] Exit the program')


conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=./hunter_project.accdb;'
)
con = pyodbc.connect(conn_str)

# set up cursor
cur = con.cursor()

first_menu()
view_choice = input()
view_choice_stat = 0

crt_choice = -1

while view_choice_stat == 0:
    if str(view_choice) == '1':
        print('You entered the program in SALES view.')
        sales_menu()
        view_choice_stat = 1
        crt_choice = input()
    if str(view_choice) == '2':
        print('You entered the program in ADMINISTRATOR view.')
        admin_menu()
        view_choice_stat = 2
        crt_choice = input()
    if str(view_choice) != '1' and str(view_choice) != '2':
        print('No such option.')
        print('Please enter again.')
        view_choice = input()

while view_choice_stat == 1:
    if crt_choice == '1':
        sql_string = 'select pro_name, pro_id, srp from product_detail where '
        print('Do you want to search by [n]ame or [i]d: ')
        crt1_choice = input()

        if crt1_choice == 'n':
            print('Please enter the product name')
            pro_name = input()
            sql_string = sql_string + 'pro_name = ' + '\'' + str(pro_name) + '\''

        if crt1_choice == 'i':
            print('Please input the product id: ')
            pro_id = input()
            sql_string = sql_string + 'pro_name = ' + '\'' + str(pro_id) + '\''

        # get result
        cur.execute(sql_string)
        print('The following are matching data: ')
        rows = cur.fetchall()
        for x in rows:
            for y in range(len(x)):
                print(cur.description[y][0], end=': ')
                print(x[y], end='\t')
            print()
        sales_menu()
        crt_choice = input()

    if crt_choice == '2':
        sql_string = "select trade_id from trade_record group by trade_id"
        cur.execute(sql_string)

        # get result
        rows = cur.fetchall()
        for x in rows:
            for y in range(len(x)):
                print(cur.description[y][0], end=': ')
                print(x[y], end='\t')
            print()

        print('Please enter trade id: ')
        print('The id should be the greatest number retrieved above+1 if this is a new record for another customer')
        print('You should enter the id as same as the last entered when your current customer is not finished the transcation')
        trade_id = input()
        print('Please enter product id: ')
        pro_id = input()
        print('Please enter the quantity of the product: ')
        quan = input()
        print('Please enter payment method: ([ca]sh/ [cr]edit_card/ [e]ps)')
        payment_method = input()
        print('Does the product protected by RMA? [y]es or [n]o')
        rma_status = input()
        print('Please enter your employee id: ')
        emp_id = input()

        sql_string = "update product_detail set quantity = quantity - {} where pro_id = \'{}\'".format(str(quan), str(pro_id))
        cur.execute(sql_string)
        con.commit()

        sql_string = "insert into trade_record values (\'{}\', \'{}\', {}, {}, \'{}\', \'{}\', \'{}\')".format(str(trade_id), str(pro_id), str(today), str(quan), str(payment_method), str(rma_status), str(emp_id))
        # print(sql_string)

        cur.execute(sql_string)
        con.commit()

        sales_menu()
        crt_choice = input()

    if crt_choice == '3':
        print('Exit the program? input [y] to confirm')
        ex_choice = input()
        if ex_choice == 'y':
            print('Program terminates, good bye.')
            con.close()
            break
        else:
            print('Backing to the admin menu...')
            pass


while view_choice_stat == 2:
    if crt_choice == '1':
        x = input()
        cur.execute(x)

        # get result
        rows = cur.fetchall()
        for x in rows:
            for y in range(len(x)):
                print(cur.description[y][0], end=': ')
                print(x[y], end='\t')
            print()
        admin_menu()
        crt_choice = input()

    if crt_choice == '2':
        print("Please input the starting date (in format of dd/mm/yyyy):")
        starting_date = input()
        print("Please input the ending date (in format of dd/mm/yyyy):")
        ending_date = input()
        sql_string = "select * from trade_record where date between #" + str(starting_date) + "# and #" + str(ending_date) + "#"
        cur.execute(sql_string)

        # get result
        rows = cur.fetchall()
        for x in rows:
            for y in range(len(x)):
                print(cur.description[y][0], end=': ')
                print(x[y], end='\t')
            print()
        admin_menu()
        crt_choice = input()

    if crt_choice == '3':
        cur.execute('select employee_name, employee_id from employee_info')
        sql_string = 'insert into employee_info(employee_id, employee_name, gender, position, date_of_birth, address, status) values ('
        total_crew_count = 0

        # get result
        rows = cur.fetchall()
        for x in rows:
            total_crew_count += 1

        print('[a]dd, [c]hange status or [m]odify?')
        crt3_choice = input()

        if crt3_choice == 'a':
            print('The next employee id is: ' + str(total_crew_count + 1))
            print('Please enter employee\'s name: ')
            name = input()
            print('Please enter gender: [F] for female or [M] for Male')
            gender = input()
            print('Please enter position id: ')
            pos_id = input()
            print('Please enter date of birth: [dd/mm/yyyy]')
            dob = input()
            print('Please enter address: ')
            address = input()

            sql_string = sql_string + '\'' + str(total_crew_count + 1) + '\'' + ',' + '\'' + str(name) + '\'' + ',' + '\'' + str(gender) + '\'' + ',' + '\'' + str(pos_id) + '\'' + ',' + '#' + str(dob) + '#' + ',' + '\'' + str(address) + '\'' + ',' + '\'' + '1' + '\'' + ');'

            # print(sql_string)

            cur.execute(sql_string)
            con.commit()

        if crt3_choice == 'c':
            print('Enter the employee id: ')
            emp_id = input()
            sql_string = 'update employee_info set status = No ' + 'where employee_id = ' + '\'' + str(emp_id) + '\''
            # sql_string = 'delete from employee_info where employee_id = ' + '\'' + str(del_id) + '\''
            cur.execute(sql_string)
            con.commit()

        if crt3_choice == 'm':
            print('Enter the employee id: ')
            emp_id = input()
            print('Enter what attribute you would like to edit: ')
            att = input()
            print('Enter the value you would like to set to: ')
            val = input()
            sql_string = 'update employee_info set ' + str(att) + ' = ' + '\'' + str(val) + '\'' + ' where employee_id = ' + '\'' + str(emp_id) + '\''
            print(sql_string)
            cur.execute(sql_string)
            con.commit()

        admin_menu()
        crt_choice = input()

    if crt_choice == '4':
        cur.execute('select position_id, position_description, salary from position')
        sql_string = 'insert into position(position_id, position_description, salary) values ('
        total_position_count = 0

        # get result
        rows = cur.fetchall()
        for x in rows:
            total_position_count += 1

        print('[a]dd or [m]odify?')
        crt4_choice = input()

        if crt4_choice == 'a':
            print('The next position id is: ' + str(total_position_count + 1))
            print('Please enter position description: ')
            pos_des = input()
            print('Please enter position salary: ')
            salary = input()

            sql_string = sql_string + '\'' + str(total_position_count + 1) + '\'' + ' , ' + '\'' + str(pos_des) + '\'' + ' , ' + '\'' + str(salary) + '\'' + ');'

            print(sql_string)

            cur.execute(sql_string)
            con.commit()

        if crt4_choice == 'm':
            print('Enter the position id: ')
            pos_id = input()
            print('Enter what attribute you would like to edit: ')
            att = input()
            print('Enter the value you would like to set to: ')
            val = input()
            sql_string = 'update position set ' + str(att) + ' = ' + '\'' + str(val) + '\'' + ' where position_id = ' + str(pos_id)
            print(sql_string)
            cur.execute(sql_string)
            con.commit()

        admin_menu()
        crt_choice = input()

    if crt_choice == '5':
        cur.execute('select pro_id, pro_name, quantity, srp from product_detail')
        sql_string = 'insert into product_detail(pro_id, brand, category, pro_name, cost, quantity, srp) values ('
        total_product_count = 0

        # get result
        rows = cur.fetchall()
        for x in rows:
            for y in range(len(x)):
                print(cur.description[y][0], end=': ')
                print(x[y], end='\t')
            print()
            total_product_count += 1

        print('[a]dd or [m]odify?')
        crt5_choice = input()

        if crt5_choice == 'a':
            print('The next product id is: ' + str(total_product_count + 1))
            print('Please enter product\'s name: ')
            pro_name = input()
            print('Please enter brand: ')
            brand = input()
            print('Please enter category: ')
            category = input()
            print('Please enter cost: \n$')
            cost = input()
            print('Please enter remaining quantity: ')
            quantity = input()
            print('Please enter SRP: \n$')
            srp = input()

            sql_string = sql_string + '\'' + str(total_product_count + 1) + '\'' + ',' + '\'' + str(brand) + '\'' + ',' + '\'' + str(category) + '\'' + ',' + '\'' + str(pro_name) + '\'' + ',' + '\'' + str(cost) + '\'' + ',' + '\'' + str(quantity) + '\'' + ',' + '\'' + str(srp) + '\'' + ');'
            # print(sql_string)

            cur.execute(sql_string)
            con.commit()

        if crt5_choice == 'm':
            print('Enter the product id: ')
            pro_id = input()
            print('Enter what attribute you would like to edit: ')
            att = input()
            print('Enter the value you would like to set to: ')
            val = input()
            sql_string = 'update product_detail set ' + str(att) + ' = ' + '\'' + str(val) + '\'' + ' where pro_id = ' + '\'' + str(pro_id) + '\''
            print(sql_string)
            cur.execute(sql_string)
            con.commit()

        admin_menu()
        crt_choice = input()

    if crt_choice == '6':
        print('Exit the program? input [y] to confirm')
        ex_choice = input()
        if ex_choice == 'y':
            print('Program terminates, good bye.')
            con.close()
            break
        else:
            print('Backing to the admin menu...')
            pass
