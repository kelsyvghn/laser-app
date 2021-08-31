# This is a sample Python script.
from tkinter import *
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import imutils
import cv2
import os
from tkinter import ttk

from single_page_laser_app import get_video_feed

tk = Tk()
# add widgets here


button = Button(tk, text="Run Video Feed Processor", fg='blue', command=get_video_feed)
button.place(x=80, y=100)
tk.title('Hello Python')
tk.geometry("300x200+10+20")
tk.mainloop()
