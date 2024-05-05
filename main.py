import mysql.connector as m
import datetime
print(dir(m))
mydatabase=m.connect(host="localhost",user="root",password="1234",database="bank")
cursor=mydatabase.cursor()

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


def login():

    
    def verify_login(acno, dob):
        if mydatabase.is_connected():
            cursor = mydatabase.cursor()
            query = """SELECT * FROM account WHERE acno = %s AND dob = %s;"""
            cursor.execute(query, (acno, dob))
            row = cursor.fetchone()
            if row:
                return True
            else:
                return False
        if mydatabase.is_connected():
            cursor.close()
            mydatabase.close()
    
    acno=getaccno()
    dob= getdob()

    if verify_login(acno, dob):
        print("====================================================================")
        print("==================      Login successful!      =====================")
        print("====================================================================")
    else:
        print("====================================================================")
        print("! Login failed. Please check your account number and date of birth. !")
        print("====================================================================")


def newUser():

    def getphonenumber():
        while True:
            phnno=input("Enter Phone Number : ")

            if len(phnno)==10:
                return phnno
            else:
                print("!!!!!!!! Enter Valid 10 Digit Number !!!!!!!!!\n")

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

    mydatabase.cursor()
    cursor.execute(sql1,data1)
    cursor.execute(sql2,data2)
    mydatabase.commit()
    print("****************************************************************")
    print("************** Data Entered Succesfully,'Login Now'**************")
    print("*****************************************************************")

    login()

def intro():
    print("*******************************************************")
    print("*************    Railworld Bank    ********************")
    print("*******************************************************")
    home()

def home():
    print("1. Already Registered User.")
    print("2. New User.")
    choice= int(input("\nEnter Your Choice : "))
    if choice==1:
        login()
    elif choice==2:
        newUser()
    else:
        print("!!!!!!Enter Valid Input!!!!!!\n")


intro()



    
    

