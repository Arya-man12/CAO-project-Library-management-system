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
import datetime
from datetime import datetime
mycon=sqltor.connect(host="localhost",user="root",passwd="aryaman", database="test")
root=tkinter.Tk()
if mycon.is_connected():
       print("Successfully connected to library")
       root.title("Welcome")
       widgt1=tkinter.Label(root,text='Successfully connected to library')
       widgt1.pack()

cursor=mycon.cursor(buffered=True)
tnow=0
q=None
print("*********************")
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
          c=cursor.rowcount
          data=cursor.fetchall()
          mycon.commit()
          for row in data:
               print(row)
          print("number of books in library",c)
          print("*********************")
def display2():
                cursor.execute("select bookname,username,date1 from borrow")
                data2=cursor.fetchall()
                mycon.commit()
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
             cursor.execute("select bookname from library WHERE bookname={}").format(a)
             chck3=cursor.rowcount
             if(chck3!=0):
              bk=("DELETE FROM library where bookname={}").format(a)
              cursor.execute(bk)
              mycon.commit()
             else:
              print("book removed")

def returnbk():
                    
                           b=input("Enter book to be returned in ''")
                           cursor.execute("select bookname from borrow WHERE bookname={}".format(b))
                           chck1=cursor.rowcount
                           if(chck1!=0):
                            
                              del1="select DATEDIFF(curdate(),(select date1 from borrow where bookname={}))".format(b);
                              cursor.execute(del1)
                              mycon.commit()
                              sub=str(cursor.fetchone()[0])
                              delay=int(sub)
                              delay=abs(delay)
                            
                              if(delay>7):
                                print("Number of days late is",delay-7)
                                print("Book overdue fine is 50rs per day")
                                print("Total fine",delay*50)

                              del1="DELETE FROM borrow WHERE bookname={}".format(b)
                              cursor.execute(del1)
                              m=cursor.rowcount
                              mycon.commit()
                              rt="INSERT INTO library(bookname) VALUES({})".format(b)
                              cursor.execute(rt)
                              mycon.commit()
                        
                           else:
                               print("book not found in borrow")
                           print("*********************")
                        
def borrow(name):
             b=input("enter the name of the book you want to borrow in ''")
             cursor.execute("select bookname from library WHERE bookname={}".format(b))
             chck1=cursor.rowcount
             from datetime import date
            
             if(chck1!=0):
               trs="INSERT INTO borrow(bookname,username,date1) VALUES({},{},curdate())".format(b,name)
               cursor.execute(trs)
               mycon.commit()
               tnow=time.time()
               print("book has been borrowed")
               print("Book should be returned within 7 days")
               rem="DELETE FROM library WHERE (bookname={})".format(b)
               cursor.execute(rem)
               mycon.commit()
             else:
                print("No such book in library")
             print("*********************")
iter=0
while(True):
       omp_set_dynamic(1)
       if(iter==0):
           user='admin'
           num_threads = 1
           print("Initial user is admin ,sign in a new user if you wish to borrow and return books")
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
           if(user!='admin'):
              borrow(user)
           else:
               print("User not signed in")
       if (a==3):
            with Pool(num_threads) as p:
                    p=Process(target=addbook,args=())
            addbook()
       if (a==4):
              if(user!='admin'):
                  returnbk()
              else:
                print("User not signed in")
       if(a==5):
                 with Pool(num_threads) as p:
                    r=Process(target=display2,args=())

                 display2()
                    
       if(a==6):
           with Pool(num_threads) as p:
                    p=Process(target=rembook,args=())
           rembook()
       if(a==7):
              user=input("Enter name of new user")
              usersadd(user)
              cursor.execute("select username from users")
              n=cursor.rowcount
              num_threads = n
              print("Number of current users",num_threads)
       if(a==8):
               
              name=input("Enter name of user")
              cursor.execute("select USERNAME FROM users WHERE username={}".format(name))
              online=cursor.rowcount
              if(online==0):
                    print("User not logged in")
              else:           
               usersrem(name)
              cursor.execute("select username from users")
              n=cursor.rowcount
              num_threads = n
              print("Number of current users ",num_threads)

       print("Press q to quit or press enter to continue using library")
       uc=input()
       if uc=='q':
               mycon.close()
               print("thank you for using this program")
               print("*********************")
               sys.exit()
       iter+=1
      
       continue    
