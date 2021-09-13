# This is a sample Python script.
import tkinter as tk
from PIL import ImageTk, Image
from single_page_laser_app import *

feed = '/Users/kelsyvaughn/Local/Code/Laser_App/Media/MyOutputVid6.avi'


def main():
    # give user the option to use local camera or external webcam, or another device (can cycle from 0-3)
    # take user input and convert to proper format for 'feed' variable
    root = tk.Tk()
    root.title("Laser Camera Feed")
    app = tk.Frame(root, borderwidth=4, bg="white")
    app.pack()
    # Create a label in the frame
    lmain = tk.Label(app)
    lmain.pack()

    source_options = ['computer webcam', 'laser webcam', 'other']

    def change_feed():

        tk.Label.config(text=video_stream(clicked.get()))

    clicked = tk.StringVar()
    clicked.set('laser webcam')

    drop = tk.OptionMenu(root, clicked, *source_options)
    drop.pack()

    source_btn = tk.Button(root, text='choose video source', width=30, command=change_feed).pack()

    label = tk.Label(root, text=" ")
    label.pack()

    def video_stream(source):
        if source == 'computer webcam':
            print('computer webcam was source', source)
            source = 0
            triangulation, frame, text, results = get_video_feed(source)
        elif source == 'laser webcam':
            # change back to 1 when program is set to run
            # feed = '/Users/kelsyvaughn/Local/Code/Laser_App/Media/MyOutputVid5.avi'
            source = 1
            triangulation, frame, text, results = get_video_feed(source)
        elif source == 'other':
            source = 2
            triangulation, frame, text, results = get_video_feed(source)
        else:
            triangulation, frame, text, results = get_video_feed(source)

        # _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, video_stream)

    video_stream(feed)
    root.mainloop()


if __name__ == "__main__":
    main()
