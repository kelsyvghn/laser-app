# This is a sample Python script.
import tkinter as tk
from PIL import ImageTk, Image
from single_page_laser_app import *

#
# window = tk.Tk()
# # Let's create the Tkinter window
# window.title("Laser Camera Feed")
#
# # running webcam
# # feed = cv2.VideoCapture(1)
# # running internal video
# feed = cv2.VideoCapture('/Users/kelsyvaughn/Local/Code/Laser_App/Media/MyOutputVid6.avi')
#
# tk.Button(window, text="Click to Run with Default Camera Source", command=get_video_feed(feed)).pack()
#
# window.mainloop()
feed = '/Users/kelsyvaughn/Local/Code/Laser_App/Media/MyOutputVid6.avi'


def main():
    # give user the option to use local camera or external webcam, or another device (can cycle from 0-3)
    # take user input and convert to proper format for 'feed' variable
    root = tk.Tk()
    root.title("Laser Camera Feed")
    app = tk.Frame(root, bg="white")
    app.grid()
    # Create a label in the frame
    lmain = tk.Label(app)
    lmain.grid()

    # tk.Label(root, text="Please select camera input or to use default, press enter").grid(row=0)
    # user_input = tk.Entry(root)
    # user_input.grid(row=0, column=1)
    # result = tk.Label(root, text='')
    # result.grid(row=2, column=0, columnspan=2)
    # btn = tk.Button(root, text='Enter => Run Camera Feed Analysis')
    # btn.config(command=lambda: result.config(text=get_video_feed(user_input())))
    # btn.grid(row=1, column=1, sticky=tk.W, pady=4)
    # cap = cv2.VideoCapture(feed)

    # function for video streaming
    def video_stream():
        triangulation, frame, text, results = get_video_feed(feed)
        # _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, video_stream)

    video_stream()
    root.mainloop()


if __name__ == "__main__":
    main()
