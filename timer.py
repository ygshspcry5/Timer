#!/usr/bin/env python
import subprocess
import sys       #for console
import time
from configparser import  ConfigParser


from tkinter import *
from tkinter import simpledialog

awaketime = 5  # default value
sleeptime = 5  # default value
skiptime = 0
rem_time=25



class notification:

    def __init__(self, master):


          slave=master

          self.master=master
          master.title("Alert!!!")


          self.t = Label(slave,
                  text="You're engaged for long time!!! \nRecommended to take break.\n\n Manual break to set break time, "
                       "Skip now to skip for desired seconds!\nPlease choose a option\n5 min break starts automatically after:\n")
          self.t.pack()
          self.time= Label(slave,text=rem_time, font = ('Comic Sans MS',30))
          self.time.pack()

          self.b = Button(slave, text="Manual break !", command=self.m_break)
          self.b.pack(side=LEFT, padx=20)
          self.b = Button(slave, text="Auto break !", command=self.a_break)
          self.b.pack(side=LEFT, padx=15)
          self.b = Button(slave, text="Skip now !", command=self.skip)
          self.b.pack(side=LEFT, padx=15)

          self.start()
          #self.update_label()

    def start(self):
          global rem_time
          rem_time-=1
          self.time["text"] = rem_time

        # After 1 second, update the status
          self.master.after(1000, self.start)




    def m_break(self):
        global sleeptime

        answer = simpledialog.askinteger("set-time", "Enter the break-time in seconds.. ",
                                         parent=self.master,
                                         minvalue=0, maxvalue=1000)
        if answer is not None:
            global x
            print("Your time is ", answer)
            sleeptime = answer

        else:
            print("Please enter time")



    def a_break(self):
        global sleeptime
        sleeptime=5

    def skip(self):
        global skiptime
        answer = simpledialog.askinteger("set-time", "Enter the skip-time in seconds.. ",
                                         parent=self.master,
                                         minvalue=0, maxvalue=1000)
        if answer is not None:
            print("Your time is ", answer)
            skiptime=answer
        else:
            print("Please enter time")



def main():
    global awaketime  # default value
    global sleeptime
    global skiptime
    global rem_time
    rem_time=25
    skiptime=0



    print(sleeptime)
    print(awaketime)
    time.sleep(awaketime)
    root = Tk()
    while True:
        i=0
        my_interface = notification(root)

        root.update_idletasks()
        while i<100:
         time.sleep(0.1)

         root.update()
         i+=1

        root.withdraw()
        if skiptime==0:
            awaketime=15
            take_a_break(sleeptime)
            break;
        elif skiptime>0:

            awaketime=skiptime
            break;









def take_a_break(sleeptime):
    get = subprocess.check_output(["xrandr"]).decode("utf-8").split()
    screens = [get[i - 1] for i in range(len(get)) if get[i] == "connected"]
    for scr in screens:
        # uncomment either one of the commands below [1]
        # darken the screen, or...
        #subprocess.call(["xrandr", "--output", scr, "--brightness", "0"])
        # turn it upside down :)
        subprocess.call(["xrandr", "--output", scr, "--rotate", "inverted"])
    time.sleep(sleeptime)
    for scr in screens:
        # back to "normal"
        subprocess.call(["xrandr", "--output", scr, "--brightness", "1"])
        subprocess.call(["xrandr", "--output", scr, "--rotate", "normal"])


def read_file():
    global awaketime  # default value
    global sleeptime

    parser = ConfigParser()#
    parser.read('new.txt')
    for section in ['time']:
        print('%s section exists: %s' % (section, parser.has_section(section)))
        for option in ['awaketime', 'sleeptime']:
            print('%s.%-12s  : %s' % (section, option, parser.has_option(section, option)))
            if parser.has_option(section, option)==True:


                if option=='awaketime':
                  try:
                    awaketime = parser.getint('time', option)
                  except ValueError:
                    print("wrong value is set for awaketime")
                elif option=='sleeptime':
                  try:
                    sleeptime =parser.getint('time',option)
                  except ValueError:
                    print("wrong value is set for sleeptime")


read_file()
while True:


 main()
