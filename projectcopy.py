import os
import sys
import time
import tkinter
import mysql.connector as sqltor
from multiprocessing import Process

# Setup minimal tkinter window
root = tkinter.Tk()
root.title("Welcome")
label = tkinter.Label(root, text='Successfully connected to library')
label.pack()

# Functions with isolated DB connections for multiprocessing
def display():
    mycon = sqltor.connect(host="localhost", user="root", passwd="aryaman", database="test")
    cursor = mycon.cursor()
    cursor.execute("SELECT bookname FROM library")
    data = cursor.fetchall()
    print("Books available:")
    for row in data:
        print(row)
    mycon.close()

def display2():
    mycon = sqltor.connect(host="localhost", user="root", passwd="aryaman", database="test")
    cursor = mycon.cursor()
    cursor.execute("SELECT bookname, username, date1 FROM borrow")
    data = cursor.fetchall()
    print("Books currently borrowed:")
    for row in data:
        print(row)
    mycon.close()

def display_users():
    mycon = sqltor.connect(host="localhost", user="root", passwd="aryaman", database="test")
    cursor = mycon.cursor()
    cursor.execute("SELECT username FROM users")
    data = cursor.fetchall()
    print("Logged-in users:")
    for row in data:
        print(row)
    mycon.close()

def run_multiprocessing_demo():
    print("\nLaunching multiprocessing display demo...")
    p1 = Process(target=display)
    p2 = Process(target=display2)
    p3 = Process(target=display_users)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    print("Finished multiprocessing display.\n")

# Main loop
while True:
    print("\n*** Library System Menu ***")
    print("1. Run multiprocessing display demo")
    print("2. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        run_multiprocessing_demo()
    elif choice == '2':
        print("Exiting program.")
        sys.exit()
    else:
        print("Invalid choice. Try again.")
