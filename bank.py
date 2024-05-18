import datetime
from database import connect_db
import mysql.connector as a
import getpass



def getaccno():
        while True:
            accno=input("Enter your 8 digit Bank AC Number : ")

            if len(accno)==8:
                return accno
            else:
                print("\n!!!!!!!!! Enter Valid 8 Digit Bank Acc Number !!!!!!!!!\n")

def getdob():
    while True:
        date_input = input("Enter a date in DD/MM/YYYY format : ")
        try:
                
            date = datetime.datetime.strptime(date_input, "%d/%m/%Y")
            return date
        except ValueError:
            print("\n!!!!!!!!!   Invalid date or format. Please try again.....    !!!!!!!!!!!\n")

def getphonenumber():
        while True:
            phnno=input("Enter 10 Digit Phone Number : ")

            if len(phnno)==10:
                return phnno
            else:
                print("\n!!!!!!!!    Enter Valid 10 Digit Number    !!!!!!!!!\n")

def getpin():
    pin= int(getpass.getpass("Enter 4 Digit Pin : "))
    if 1000 <= int(pin) <= 9999:
        return pin
    else :
        print("\n!!!!!!!!!!     Enter Valid 4 Digit Pin    !!!!!!!!!\n")
        getpin()
    
                
class login:
    def __init__(self,acno,pwd):
        self.acno=acno
        self.pwd=pwd
       
    
    def verify_login(self):
        db = connect_db()  # Establish the database connection
        try:
            cursor = db.cursor()  # Create a cursor object
            query = "SELECT * FROM account WHERE acno = %s AND pwd = %s;"
            cursor.execute(query, (self.acno, self.pwd))
            row = cursor.fetchall()
            return row[0]
        except AttributeError as err:
            print("\n!!!!!!!!!!   Database Error   !!!!!!!!!!!!!!\n")
            return False
        finally:
            if cursor:
                cursor.close()
            db.close()
            return self.acno




def deposit_amount(loginac):
    while True:    
        try:
            amount = int(input("Enter Amount : "))
            if amount < 0:
                print("\n!!!!!!!!!   Amount must be a positive number.   !!!!!!!!!!\n")
                continue
            account = input("Enter Account No : ")
            if account==loginac:
                db = connect_db()
                cursor = db.cursor()

                # Check current balance
                sql_select = "SELECT amt FROM amount WHERE acno = %s;"
                cursor.execute(sql_select, (account,))
                myresult = cursor.fetchone()

                if myresult is None:
                    print("\n!!!!!!!!!!!!!!!!!   Account not found.   !!!!!!!!!!!!!!!!!!!!\n")
                    continue
            else:
                print("\n!!!!!!!!!!!!!!  Enter Correct Account Number   !!!!!!!!!!!!!!!\n")
                continue

            # Calculate new total amount
            current_balance = myresult[0]
            new_balance = current_balance + amount

            # Update balance in database
            sql_update = "UPDATE amount SET amt = %s WHERE acno = %s;"
            cursor.execute(sql_update, (new_balance, account))
            db.commit()
            print("\n***********************************************")
            print("Deposit successful. New balance:", new_balance)
            print("***********************************************\n")
            return

        except ValueError:
            print("\n!!!!!!!!!!!   Invalid input. Please enter a valid number.   !!!!!!!!!!!!!!\n")
            continue
        except a.Error:
            print("\n!!!!!!!!!!!!!!!!!    Database Error    !!!!!!!!!!!!!!!!!!!!!\n")
            continue
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()
            input("Press Any Key to Continue...........")


def withdraw_amount(loginac, pwd):
    while True:
        try:
            amount = int(input("Enter Amount : "))
            if amount <= 0:
                print("\n!!!!!!!!!    Please enter a positive amount to withdraw.    !!!!!!!!!!\n")
                continue
            
            pin = int(input("Enter 4 digit PIN : "))
            
            if pin==pwd:

                db = connect_db()
                cursor = db.cursor()

                # Check current balance
                query = "SELECT amt FROM amount WHERE acno = %s"
                cursor.execute(query, (loginac,))
                result = cursor.fetchone()

                if result is None:
                    print("\n!!!!!!!!!!!!    Account not found.    !!!!!!!!!!!!!!!!\n")
                    continue

                current_balance = result[0]
                if amount > current_balance:
                    print(f"\n!!!!!!!!    Insufficient Funds. Available balance: {current_balance}    !!!!!!!!!\n")
                    continue
            
            else:
                print("\n!!!!!!!!!! Enter Correct PIN !!!!!!!!!!!!\n")
                continue

            # Update the balance if sufficient funds
            new_balance = current_balance - amount
            update_query = "UPDATE amount SET amt = %s WHERE acno = %s"
            cursor.execute(update_query, (new_balance, loginac))
            db.commit()
            print("\n****************************************************")
            print(f"Withdrawal successful. New balance: {new_balance}")
            print("****************************************************\n")
            return

        except ValueError:
            print("\n!!!!!!!!!!!!!!!!   Invalid input. Please enter a valid numeric amount.   !!!!!!!!!!!!!\n")
            continue
        except a.Error as err:
            print("\n!!!!!!!!!!!!!!   Database Error    !!!!!!!!!!!!!!!!!!!\n")
            continue
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()
            input("Press Any Key to Continue...........")



def balance(loginac):
    while True:
        try:
            
            db = connect_db()
            cursor = db.cursor()
            query = "SELECT amt FROM amount WHERE acno = %s"
            cursor.execute(query, (loginac,))
            result = cursor.fetchone()
            
            if result is None:
                print("\n!!!!!!!!!!!!!!!!!    Account Not Found.    !!!!!!!!!!!!!!!!!!!!!\n")
            else:
                print("\n***********************************************")
                print(f"Balance for Account {loginac} is {result[0]}")
                print("***********************************************\n")
                return
            
        except a.Error:
            print("\n!!!!!!!!!!!!!!!    Database error   !!!!!!!!!!!!!!!!!!!!\n")
            continue
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
            input("Press Any Key to Continue...........")


def display_account(loginac):
    
    db = connect_db()
    cursor = db.cursor()
    a = "select * from account where acno = %s"
    data = (loginac,)
    
    cursor.execute(a, data)
    myresult = cursor.fetchone()
    
    desc=['Name','Acc No','DOB','Address','Phone','Opening Balance','A/C Creation Date']
    if myresult:
        columns = [i.upper() for i in desc]
        print("\n--------------------------------")
        for col, val in zip(columns, myresult):
            if col=="pwd":
                
                continue
            else:
                print(f"{col}: {val}", end="  \n")
                print("\n")

        
        print("--------------------------------")  # For newline after the loop
    else:
        print("\n!!!!!!!!!!!!    No account found with this number.    !!!!!!!!!!!!!!!!!\n")
    input("Press Any Key to Continue...........")



def transfer_amount(from_account, to_account, amount,pwd):
    pin=int(input("Enter PIN : "))
    if pin == pwd:
        db = connect_db()
        if db is None:
            print("\n!!!!!!!!!!!!!!!    Database connection failed    !!!!!!!!!!!!!!!!\n")
            return

        try:
            cursor = db.cursor()

            # Start transaction
            db.start_transaction()

            # Fetch balances of the sender and receiver accounts
            cursor.execute("SELECT amt FROM amount WHERE acno = %s", (from_account,))
            result = cursor.fetchone()
            sender_balance = result[0] if result else None  # Ensure that the balance is correctly extracted

            cursor.execute("SELECT amt FROM amount WHERE acno = %s", (to_account,))
            result = cursor.fetchone()
            receiver_balance = result[0] if result else None  # Ensure that the balance is correctly extracted
        

            # Check for valid accounts and sufficient funds
            if sender_balance is None or receiver_balance is None:
                print("\n!!!!!!!!!!!!!!!!!    One of the account numbers is invalid.    !!!!!!!!!!!!!!!!!\n")
                return
            if sender_balance < amount:
                print("\n!!!!!!!!!!!!!!!!    Insufficient balance to transfer amount.    !!!!!!!!!!!!!!!!!\n")
                return

            # Update balances
            new_sender_balance = sender_balance - amount
            cursor.execute("UPDATE amount SET amt = %s WHERE acno = %s", (new_sender_balance, from_account))

            new_receiver_balance = receiver_balance + amount
            cursor.execute("UPDATE amount SET amt = %s WHERE acno = %s", (new_receiver_balance, to_account))

            #transaction date
            today_date = datetime.datetime.now()
            
            # Insert transaction record
            cursor.execute("INSERT INTO transactions (tran_date, from_account, to_account, amount) VALUES (%s, %s, %s, %s)",(today_date, from_account, to_account, amount))
            
            # Commit the transaction
            db.commit()
            print("\n***********************************************")
            print("Amount transferred successfully")
            print("***********************************************\n")
        except a.Error as err:
            print("\n!!!!!!!!!!!!!!    Error during transaction    !!!!!!!!!!!!!!!!!\n")
            db.rollback()
        finally:
            cursor.close()
        
            db.close()
    else:
        print("\n!!!!!!!!!   PIN Error, Try Again   !!!!!!!!!!!!\n")
    input("Press Any Key to Continue...........")


def transaction_history(loginac):
    db = connect_db()
    if db is None:
        print("\n!!!!!!!!!!!!!!!!!!!!!    Database connection failed    !!!!!!!!!!!!!!!!!!\n")
        return

    try:
        cursor = db.cursor()
        query = "SELECT tran_date, from_account, to_account, amount FROM transactions WHERE from_account = %s ORDER BY tran_date DESC LIMIT 5"
        cursor.execute(query, (loginac,))
        transactions = cursor.fetchall()

      
        if transactions:
            print(f"Passbook for Account: {loginac}")
            print("{:<20} {:<20} {:<20} {:<20}".format("Date", "From", "To", "Amount"))
            for transaction in transactions:
                
                # Format the date for better readability
                formatted_date = transaction[0].strftime('%Y-%m-%d %H:%M:%S')
                print("{:<20} {:<20} {:<20} {:<20}".format(formatted_date, transaction[1], transaction[2], transaction[3]))
        else:
            print("\n!!!!!!!!!!!    No transaction history found for Account:", loginac,"    !!!!!!!!!!!\n")
        

    except a.Error as err:
        print("Error:", err)
    finally:
        if cursor:
            cursor.close()
        db.close()
        input("Press Any Key to Continue...........")



def close_account(loginac,pwd):
    db = connect_db()
    pin = int(input("Enter PIN : "))
    choice=input("Are you sure you want to Delete your account permanently [y/n] : ")
    if choice=='y' or choice=='Y':
        if pin==pwd:
            sql1 = "delete from account where acno = %s"
            sql2 = "delete from amount where acno = %s"
            data = (loginac,)
            cursor = db.cursor()
            cursor.execute(sql1, data)
            cursor.execute(sql2, data)
            db.commit()
            print("\n*****************************************************")
            print("**********  Account Deleted Successfully  ***********")
            print("*****************************************************\n")
        else: 
            print("\n!!!!!!!!!!!   Wrong Pin   !!!!!!!!!!!!!!!!\n")
    elif choice=='n'or choice=='N':
        print("\n******************* THANKYOU! FOR BEING WITH US *****************\n")
    else:
        print("!!!!!!!!!!!    Enter valid Choice    !!!!!!!!!!!!!")
    input("Press Any Key to Continue...........")






    
def service(acno,pwd):
    loginac=acno
    while True:
        print("""
            
            1. Deposit Amount
            2. Withdraw Amount
            3. Balance Enquiry
            4. Display Customer Details
            5. Transefer Amount
            6. Transaction History
            7. Close An Account
            8. Exit
        """)
        choice = input("Enter Task No: ")
        if choice == '1':
            deposit_amount(loginac)
        elif choice == '2':
            withdraw_amount(loginac,pwd)
        elif choice == '3':
            balance(loginac)
        elif choice == '4':
            display_account(loginac)
        elif choice == '5':
            
            to_account = input("Enter To Account No: ")
            amount = int(input("Enter Amount: "))
            transfer_amount(loginac, to_account, amount,pwd)
        elif choice == '6':
            
            transaction_history(loginac) 

        elif choice == '7':
            close_account(loginac,pwd)
        elif choice == '8':
            break
               
        else:
            print("!!!!   Invalid choice   !!!!")
    

def intro():
    print("*******************************************************")
    print("*************    Railworld Bank    ********************")
    print("*******************************************************\n")
    home()

def home():
    print("1. Registered User.")
    print("2. New User.")
    choice = int(input("\nEnter Your Choice : "))
    if choice == 1:
        print("===============================================================")
        print("=========================    LOGIN    =========================")
        print("===============================================================\n\n")
        acno = getaccno()  # Get account number from the user
        pwd = getpin()    # Get date of birth from the user, formatted correctly
        
        # Create an instance of the Login class with the provided acno and dob
        user_login = login(acno, pwd)
        
        # Call verify_login on the instance, not the class
        if user_login.verify_login():
            print("====================================================================")
            print("==================      Login successful!      =====================")
            print("====================================================================\n\n")
            service(acno,pwd)
        else:
            print("====================================================================")
            print("! Login failed. Please check your Account Number and Password. !")
            print("====================================================================\n\n")
    elif choice == 2:
        print("==========================================================================")
        print("=========================    New Registration    =========================")
        print("==========================================================================\n\n")
        name=input("Enter Name : ")
        acno=getaccno()
        dob=getdob()
        ad=input("Enter Address : ")
        phn=getphonenumber()
        ob=int(input("Enter Opening Balance :"))
        pwd = getpin()
        acc_cr_date=datetime.datetime.now()
        data1=(name,acno,dob,ad,phn,ob,acc_cr_date,pwd)
        data2=(name,acno,ob)

        sql1=('insert into account values(%s,%s,%s,%s,%s,%s,%s,%s)')
        sql2=('insert into amount values(%s,%s,%s)')

        db=connect_db()
        cursor=db.cursor()
        cursor.execute(sql1,data1)
        cursor.execute(sql2,data2)
        # userid= cursor.execute("select id from account where acno = %s",acno)
        db.commit()

        print("****************************************************************")
        print("************** Data Entered Succesfully,'Login Now'**************")
        print("*****************************************************************\n")
        cursor.close()
        db.close()
        
        home()

    else:
        print("!!!!!!Enter Valid Input!!!!!!\n")

        home()


intro()    
    

