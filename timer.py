#!/usr/bin/env python
import subprocess
import time
from configparser import ConfigParser
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from pynput import keyboard
import threading

# The key combination to check
COMBINATION = { keyboard.Key.shift,keyboard.Key.ctrl,keyboard.Key.esc}

# The currently active modifiers
current = set()


# global variables initialization
awake_time = 5
sleep_time = 5
skiptime = 0
wait_time = 0
break_interrupt=False


class notification:
    def __init__(self, master):

        self.master = master
        master.title("EyesAlert!!!")

        self.t = Label(master,
                       text="You're engaged for long time!!! \nRecommended to take break.",font = ('Sawasdee', 15,'bold'))
        self.t.pack()

        self.t = Label(master,
                       text="Default break starts automatically after:", font=('URW Chancery L', 15))
        self.t.pack()

        self.time = Label(master, text=wait_time, font=('Comic Sans MS', 30))
        self.time.pack()

        self.t = Label(master,
                       text="SECONDS", font=('Comic Sans MS', 15))
        self.t.pack()

        self.b = Button(master, text="Manual break !", foreground="green", activeforeground="brown", bd="3px;",
                        font=('Comic Sans MS', 13, 'bold'), command=self.m_break)
        self.b.pack(side=LEFT, padx=15)

        self.b = Button(master, text="Skip now !", foreground="green", activeforeground="brown", bd="3px;",
                        font=('Comic Sans MS', 13, 'bold'), command=self.skip)
        self.b.pack(side=LEFT, padx=10)

        self.b = Button(master, text="Help !", foreground="green", activeforeground="brown", bd="3px;", bg='#A9A9A0',
                        font=('Comic Sans MS', 13, 'bold'), command=self.help)
        self.b.pack(side=LEFT, padx=10)

        self.update()
        # update wait_time



    def update(self):
        global wait_time
        while wait_time < 1:
            return 0
        wait_time -= 1
        self.time["text"] = wait_time
        # After 1 second, update the status
        self.master.after(1000, self.update)

    def m_break(self):
        global sleep_time

        answer = simpledialog.askinteger("set-time", "Enter the break-time in seconds.. ",
                                         parent=self.master,
                                         minvalue=0, maxvalue=3000)
        if answer is not None:

            sleep_time = answer
        else:
            print("Please enter time")

    def help(self):
        messagebox.showinfo("help","\n\n  Click on Manual break!  to set break time, "
                            "\n\n  Click on Skip now!   to skip for desired seconds!\n\n")




    def skip(self):
        global skiptime
        answer = simpledialog.askinteger("set-time", "Enter the skip-time in seconds.. ",
                                         parent=self.master,
                                         minvalue=0, maxvalue=3000)
        if answer is not None:
            skiptime = answer
        else:
            print("Please enter time")


def main():
    global awake_time
    global skiptime

    time.sleep(awake_time)
    # waits for awake_time
    #read_file()
    # reads global variables from file


    while True:
        i = 0
        root = Tk()
        my_interface = notification(root)
        root.update_idletasks()

        # updates dialog box every o.1 sec
        while i < 260:
            time.sleep(0.1)
            root.update()
            i += 1

        # hides notification box
        root.withdraw()

        if skiptime == 0:
            # screen offs for sleep_time
            take_a_break(sleep_time)
            break;
        elif skiptime > 0:
            # sets awake_time as skiptime
            awake_time = skiptime
            skiptime = 0
            break;

def take_a_break(sleep_time):
    get = subprocess.check_output(["xrandr"]).decode("utf-8").split()
    screens = [get[i - 1] for i in range(len(get)) if get[i] == "connected"]
    for scr in screens:
        # uncomment either one of the commands below [1]
        # darken the screen, or...
        subprocess.call(["xrandr", "--output", scr, "--brightness", "0"])
        # turn it upside down :)
        #subprocess.call(["xrandr", "--output", scr, "--rotate", "inverted"])
    i=0
    while i<sleep_time:
      time.sleep(1)
      i+=1
      if break_interrupt == True:
          break;



    for scr in screens:
        # back to "normal"
        subprocess.call(["xrandr", "--output", scr, "--brightness", "1"])
        #subprocess.call(["xrandr", "--output", scr, "--rotate", "normal"])


def read_file():
    global awake_time  # default value
    global sleep_time
    global wait_time

    parser = ConfigParser()  #
    parser.read('new.txt')
    for section in ['time']:
        print('%s section exists: %s' % (section, parser.has_section(section)))
        for option in ['awake_time', 'sleep_time', 'wait_time']:
            print('%s.%-12s  : %s' % (section, option, parser.has_option(section, option)))
            if parser.has_option(section, option) == True:

                if option == 'awake_time':
                    try:
                        awake_time = parser.getint('time', option)
                    except ValueError:
                        print("wrong value is set for awake_time")
                elif option == 'sleep_time':
                    try:
                        sleep_time = parser.getint('time', option)
                    except ValueError:
                        print("wrong value is set for sleep_time")
                elif option == 'wait_time':
                    try:
                        wait_time = parser.getint('time', option)
                    except ValueError:
                        print("wrong value is set for wait_time")




def on_press(key):
    global break_interrupt
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            print('All modifiers active!')
            break_interrupt=True



def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

def m():
 while True:
    main()

main_thread = threading.Thread(m())
read_file()
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()



main_thread.start()




