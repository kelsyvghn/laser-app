# This is a sample Python script.
import tkinter as tk
from PIL import ImageTk, Image
from duplicate_single_page_laser_app import *

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

        tk.Label.config(text=video_stream(feed_selection.get()))

    feed_selection = tk.StringVar()
    feed_selection.set('laser webcam')

    drop = tk.OptionMenu(root, feed_selection, *source_options)
    drop.pack()

    source_btn = tk.Button(root, text='choose video source', width=30, command=change_feed).pack()

    label = tk.Label(root, text=" ")
    label.pack()

    def run_triangulation(coordinates, frames):
        x, y, image, dist = triangulate_circles((coordinates, frames))

    def return_options(circles_output, coordinate_selection):
        coordinate_selections = []
        # print('this is what circles_output contains: ', circles_output)
        for (x, y, r) in circles_output:
            print('circle coordinates in return_options ', (x, y, r))
            coordinate_selections.append((x, y, r))
        return coordinate_selections

    def video_stream(source):
        if source == 'computer webcam':
            print('computer webcam was source', source)
            source = 0
            # triangulation, frame, text, results = get_video_feed(source)
            circles, frame = get_video_feed(source)
            x, y, image, dist = triangulate_circles((circles, frame))
        elif source == 'laser webcam':
            # change back to 1 when program is set to run
            # feed = '/Users/kelsyvaughn/Local/Code/Laser_App/Media/MyOutputVid5.avi'
            source = 1
            # triangulation, frame, text, results = get_video_feed(source)
            circles, frame = get_video_feed(source)
        elif source == 'other':
            source = 2
            # triangulation, frame, text, results = get_video_feed(source)
            circles, frame = get_video_feed(source)
        else:
            # triangulation, frame, text, results = get_video_feed(source)
            circles, frame = get_video_feed(source)
        # _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, video_stream)
        ##
        coordinate_selection = tk.StringVar()
        coordinate_selection.set('using returned coordinates')
        selection_list = tk.Listbox(root, selectmode='multiple')
        selection_list.pack(expand='yes', fill='both')

        coordinate_options = return_options(circles, coordinate_selection)
        # print('this is what coordinate_selections contains: ', coordinate_options)

        # selections = tk.Listbox(root, coordinate_selection, *coordinate_options)
        # selections.pack()
        count = 0
        for each in range(len(coordinate_options)):
            selection_list.insert(count, coordinate_options[each])
            count += 1
            selected = []

            # selection = tk.Listbox(root, text=f'coordinates {each}', variable=coordinate_selection, value=each)
        # return an array of user selected coordinates to pass to the triangulation method with the current image(frame)

        source_btn = tk.Button(root, text='run selected coordinates to triangulate', width=30,
                               command=run_triangulation(selected, frame)).pack()

        label_too = tk.Label(root, text=" ")
        label_too.pack()

        # return circles, image

        ##
        # needs to output circle coordinates onto image, and written (visible in another column) as a list or similar

    video_stream(feed)
    root.mainloop()


if __name__ == "__main__":
    main()
