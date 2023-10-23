import os
import sys
import multiprocessing
from multiprocessing import Process
from multiprocessing import Pool
import project
import cython
import time
import tkinter
import mysql.connector as sqltor
try:
 from cython.cimports.openmp import omp_set_dynamic
except AttributeError:
       print("No such attribute")
mycon=sqltor.connect(host="localhost",user="root",passwd="aryaman", database="test")
root=tkinter.Tk()

if mycon.is_connected():
       print("successfully connected to library")
       root.title("Welcome")
       widgt1=tkinter.Label(root,text='Successfully connected to library')
       widgt1.pack()

cursor=mycon.cursor(buffered=True)
tnow=0
q=None
print("*********************")
print('Welcome to the library.enter your choice to continue')
dict1={}
def usersadd(name):
       add="INSERT INTO users(USERNAME) VALUES({})".format(name)
       cursor.execute(add)
       mycon.commit()

def usersrem(name):
       rem="DELETE FROM users WHERE USERNAME={}".format(name)
       cursor.execute(rem)
       mycon.commit()

def display():
          print("We have the following books in our library:")
          cursor.execute("select bookname from library")
          data=cursor.fetchall()
          for row in data:
             print(row)
          c=cursor.rowcount
          print("number of books in library",c)
          print("*********************")
def display2():
                cursor.execute("select bookname,username from borrow")
                data2=cursor.fetchall()
                print(data2)
def addbook():

                   a=input("enter name of book you want to add in '' ")
                   bk="INSERT INTO library(bookname) VALUES({})".format(a)
                   try:
                      cursor.execute(bk)
                      print("book has been added")
                      mycon.commit()  
                   except sqltor.IntegrityError as err:
                        print("Error: {}".format(err))
                   
                   print("*********************")
def rembook():
    
             a=input("enter name of book you want to remove in '' ")
             bk=("DELETE FROM library where bookname={}").format(a)
             cursor.execute(bk)
             mycon.commit()
             print("book removed")

def returnbk(name):
                           b=input("Enter book to be returned in ''")
                           cursor.execute("select bookname from borrow WHERE bookname={}".format(b))
                           chck1=cursor.rowcount
                           if(chck1!=0):
                              del1="DELETE FROM borrow WHERE bookname={}".format(b)
                              cursor.execute(del1)
                              mycon.commit()
                              rt="INSERT INTO library(bookname) VALUES({})".format(b)
                              cursor.execute(rt)
                              mycon.commit()
                              rettime=time.time()
                              time_delta=(rettime-dict1[name])
                              print("book returned after time",time_delta,"seconds")
                              delay_time=time_delta//30
                              if(delay_time>1):
                                     print("you have to pay a fine of ",(delay_time -1)*5,"rupees")
                           else:
                               print("book not found in borrow")
                           print("*********************")
def borrow(name):
             b=input("enter the name of the book you want to borrow in ''")
             cursor.execute("select bookname from library WHERE bookname={}".format(b))
             chck1=cursor.rowcount
             if(chck1!=0):
               trs="INSERT INTO borrow(bookname,username) VALUES({},{})".format(b,name)
               cursor.execute(trs)
               mycon.commit()
               tnow=time.time()
               dict1[name]=tnow
               
               print("book has been borrowed")
               rem="DELETE FROM library WHERE (bookname={})".format(b)
               cursor.execute(rem)
               mycon.commit()
             else:
                print("No such book in library")
             print("*********************")

try:
 user=input("Enter your username in ''")
except sqltor.IntegrityError as err:
                        print("Username already logged in")
ck="INSERT INTO users(USERNAME) VALUES({})".format(user)
cursor.execute(ck)
mycon.commit()
sel="select*from users"
cursor.execute(sel)
mycon.commit()
n=cursor.rowcount
num_threads = n
omp_set_dynamic(n)
list1=[]

while(True):
       print("Welcome to the library,enter you choice from the menu")
       print("1.Display books available")
       print("2.borrow books")
       print("3.Add books to library")
       print("4.Return books")
       print("5.see users and books borrowed")
       print("6.remove books from library")
       print("7.Signin new user")
       print("8.Logout")
       print("*********************")
       a=int(input("Enter choice"))
       
       if (a>8):
        print("Invalid choice, please try again")
       
       
       if (a==1):
         with Pool(num_threads) as p:
                    p=Process(target=display,args=())
                    
         display()
       if (a==2):
            borrow(user)
       if (a==3):
            with Pool(num_threads) as p:
                    p=Process(target=addbook,args=())
            addbook()
       if (a==4):
           
                returnbk(user)
      
       if(a==5):
                 with Pool(num_threads) as p:
                    r=Process(target=display2,args=())

                 display2()
                    
       if(a==6):
           with Pool(num_threads) as p:
                    p=Process(target=rembook,args=())
           rembook()
       if(a==7):
              name=input("Enter name of new user")
              usersadd(name)
              cursor.execute("select username from users")
              n=cursor.rowcount
              num_threads = n
              print("Number of users ",num_threads)
       if(a==8):
               
              name=input("Enter name of  user")
              usersrem(name)
              cursor.execute("select username from users")
              n=cursor.rowcount
              num_threads = n
              print("Number of users ",num_threads)

       print("Press q to quit or press enter to continue using library")
       uc=input()
       if uc=='q':
               mycon.close()
               print("thank you for using this program")
               print("*********************")
               sys.exit()

       continue    
