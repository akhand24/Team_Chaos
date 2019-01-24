#!/usr/bin/python

import serial
import pymysql
from tkinter import *
from tkinter import messagebox



ui_message = "Scan ID"

# establish connection to MySQL. You'll have to change this for your database.

try:
    dbConn = pymysql.connect("localhost", "root", "12345", "library") #or die("could not connect to database")
# open a cursor to the database
except Exception:
        #print("Error in MySQL connexion")
        messagebox.showerror("!!!ERROR!!!","CHECK THE MYSQL CONNECTION")
else:
    cursor = dbConn.cursor()

device = 'COM6'  # this will have to be changed to the serial port you are using
try:
    print("Trying...", device)
    arduino = serial.Serial(device, 9600)
except:
    print("Failed to connect on", device)

while(1):
    try:
        data = arduino.readline().decode("utf-8")  # read the data from the arduino
        print(data)

        try:
            cursor.execute("SELECT sid FROM student WHERE sid = '"+data+"';")
            result_sid = cursor.fetchall()
            if(result_sid!=""):
                cursor.execute("SELECT sid FROM issue WHERE sid = '" + data + "';")
                result_issue = cursor.fetchall()
                if(result_issue==""):
                    ui_message = "Scan Book RFID"
                    data = arduino.readline().decode("utf-8")
                    cursor.execute("SELECT bid FROM issue WHERE bid = '" + data + "';")
                    result_bid = cursor.fetchall()
                    if(result_bid==data):
                        cursor.execute("DELETE FROM issue WHERE bid = '"+result_bid+"';")
                        ui_message = messagebox.showinfo("Thank you","Book is returned")
                    else:
                        cursor.execute("INSERT INTO issue VALUES('"+result_bid+"','"+result_sid+"',current_date(),current_date()+14);")
                        ui_message = messagebox.showinfo("CONGRATS","book is issued")

                else:
                    ui_message = messagebox.showerror("!!!SORRY!!!"," Already Issued a Book")
            else:
                ui_message = messagebox.showerror("!!!SORRY!!!","Err! Student ID not found")
        except pymysql.IntegrityError:
            #print("failed to insert data")
            messagebox.showerror("!!!ERROR!!!","Failed to insert the data")
        finally:
            cursor.close()  # close just incase it failed
    except:
        print("Failed to get data from RFID Reader!")
