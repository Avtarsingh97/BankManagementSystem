import datetime
from database import connect_db


def getaccno():
        while True:
            accno=input("Enter Bank AC Number : ")

            if len(accno)==8:
                return accno
            else:
                print("!!!!!!!!! Enter Valid 8 Digit Bank Acc Number !!!!!!!!!\n")

def getdob():
    while True:
        date_input = input("Enter a date in DD/MM/YYYY format : ")
        try:
                
            date = datetime.datetime.strptime(date_input, "%d/%m/%Y")
            return date
        except ValueError:
            print("!!!!!!!!!Invalid date or format. Please try again.!!!!!!!!!!!\n")

def getphonenumber():
        while True:
            phnno=input("Enter Phone Number : ")

            if len(phnno)==10:
                return phnno
            else:
                print("!!!!!!!! Enter Valid 10 Digit Number !!!!!!!!!\n")


class login:
    def __init__(self,acno,dob):
        self.acno=acno
        self.dob=dob
       
    
    def verify_login(self):
        db = connect_db()  # Establish the database connection
        try:
            cursor = db.cursor()  # Create a cursor object
            query = "SELECT * FROM account WHERE acno = %s AND dob = %s;"
            cursor.execute(query, (self.acno, self.dob))
            row = cursor.fetchone()
            cursor.fetchall()
            return bool(row)
        except db.Error as err:
            print("Database error:", err)
            return False
        finally:
            if cursor:
                cursor.close()
            db.close()

def intro():
    print("*******************************************************")
    print("*************    Railworld Bank    ********************")
    print("*******************************************************\n")
    home()

def home():
    print("1. Already Registered User.")
    print("2. New User.")
    choice = int(input("\nEnter Your Choice : "))
    if choice == 1:
        print("===============================================================")
        print("=========================    LOGIN    =========================")
        print("===============================================================\n\n")
        acno = getaccno()  # Get account number from the user
        dob = getdob()    # Get date of birth from the user, formatted correctly
        
        # Create an instance of the Login class with the provided acno and dob
        user_login = login(acno, dob)
        
        # Call verify_login on the instance, not the class
        if user_login.verify_login():
            print("====================================================================")
            print("==================      Login successful!      =====================")
            print("====================================================================\n\n")
        else:
            print("====================================================================")
            print("! Login failed. Please check your account number and date of birth. !")
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
        
        data1=(name,acno,dob,ad,phn,ob)
        data2=(name,acno,ob)

        sql1=('insert into account values(%s,%s,%s,%s,%s,%s)')
        sql2=('insert into amount values(%s,%s,%s)')

        db=connect_db()
        cursor=db.cursor()
        cursor.execute(sql1,data1)
        cursor.execute(sql2,data2)
        db.commit()
        print("****************************************************************")
        print("************** Data Entered Succesfully,'Login Now'**************")
        print("*****************************************************************\n")
        
        
        home()

    else:
        print("!!!!!!Enter Valid Input!!!!!!\n")

        home()


intro()



    
    

