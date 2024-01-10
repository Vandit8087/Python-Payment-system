import mysql.connector

us_er = input("Enter the name of your user :")
pass_word = input("Enter the password of your user :")
db = mysql.connector.connect(host="localhost", port="3306",user=us_er, passwd=pass_word, auth_plugin='mysql_native_password')
a = """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
*                                                                                 *
*                                                                                 *
*                                                                                 *
*                             ONLINE PAYMENT SYSTEM                               *
*                                                                                 *
*                                                                                 *
*                                                                                 *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
"""

print(a)

c = db.cursor()
c.execute("create database if not exists banksys;")
c.execute("use banksys; ")
c.execute("create table if not exists balances(accno int(5) primary key, name varchar(50), balance int(20));")
c.execute("create table if not exists transactions(value int(20), fromacc int(5), toacc int(5));")


def showall(c):
    c.execute("select * from balances;")
    data = c.fetchall()
    for i in data:
        print(i)


def create_acc(accno, name, balance, c):
    c.execute(f"insert into balances values({accno},'{name}',{balance});")
    print(f"account {accno} created")
    db.commit()


def delete_acc(accno, c):
    c.execute(f"select * from balances where accno = {accno};")
    o = c.fetchall()
    if not o:
        print("acc does not exist")
    else:
        c.execute(f"delete from balances where (accno = {accno});")
        db.commit()
        print(f"account {accno} deleted")
        return


def show_bal(accno, c):
    c.execute(f"select * from balances where accno = {accno};")
    o = c.fetchall()
    if not o:
        print("acc does not exist")
    for i in o:
        print(f"balance - ₹{i[2]} in account {i[0]} owned by {i[1]}")
    db.commit()
    return i[2]


def transact(fromacc, toacc, value, c):
    c.execute(f"select * from balances where accno = {fromacc};")
    o = c.fetchall()
    if not o:
        print("acc does not exist")
    else:
        c.execute(f"select * from balances where accno = {fromacc};")
        o1 = c.fetchall()
        c.execute(f"select * from balances where accno = {toacc};")
        o2 = c.fetchall()
        if not o1 or not o2:
            print("acc does not exist")
        else:
            from_bal = show_bal(fromacc, c)
            if from_bal < value:
                print("insufficient balance")
                return
            else:
                c.execute(
                    f"update balances set balance = balance - {value} where accno = {fromacc};")
                c.execute(
                    f"update balances set balance = balance + {value} where accno = {toacc};")
                c.execute(
                    f"insert into transactions values({value},{fromacc},{toacc});")
                db.commit()
                print("transaction successful")
                return


def show_all_trans(c):
    c.execute("select * from transactions;")
    data = c.fetchall()
    for i in data:
        print(i)


while True:
    print("1. Create Account")
    print("2. Delete Account")
    print("3. Show Balance")
    print("4. Transaction")
    print("5. All Account Balances")
    print("6. Show All Transactions")
    print("7. Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        accno = int(input("Enter Account Number: "))
        name = input("Enter Name: ")
        balance = int(input("Enter Balance: "))
        create_acc(accno, name, balance, c) 

    elif ch == 2:
        accno = int(input("Enter Account Number to delete: "))
        delete_acc(accno, c)

    elif ch == 3:
        accno = int(input("Enter Account Number: "))
        show_bal(accno, c)

    elif ch == 4:
        fromacc = int(input("Enter From Account Number: "))
        toacc = int(input("Enter To Account Number: "))
        value = int(input("Enter Value: "))
        transact(fromacc, toacc, value, c)

    elif ch == 5:
        showall(c)

    elif ch == 6:
        show_all_trans(c)

    elif ch == 7:
        break

    else:
        print("Invalid Choice")
        continue

db.commit()
db.close()