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

    source_options = ['computer webcam', 'laser webcam', 'local']

    def change_feed():

        tk.Label.config(text=video_stream(feed_selection.get()))

    feed_selection = tk.StringVar()
    feed_selection.set('laser webcam')

    drop = tk.OptionMenu(root, feed_selection, *source_options)
    drop.pack()

    source_btn = tk.Button(root, text='choose video source', width=30, command=change_feed).pack()

    label = tk.Label(root, text=" ")
    label.pack()

    def selected(user_list):
        count = 0
        selections = []
        for i in user_list.curselection():
            selections.append(count, i)
            count += 1
        return selections

    def run_user_calculations(input_coordinates, video):
        user_selection_list = tk.Listbox(root, selectmode="multiple")
        user_selection_list.pack(fill='both')
        # coord is the list, already created/returned from the previous run of the video feed
        count = 0
        for each_coord in range(len(input_coordinates)):
            user_selection_list.insert(count, input_coordinates[each_coord])
            count += 1

        find_selected = selected(user_selection_list)
        user_calculation = triangulate_circles(find_selected, video)
        print('find selected', find_selected)
        print('user selection list', user_selection_list)
        print('user_calculations', user_calculation)
        coord_selection_btn = tk.Button(root, text='run calculations with selected', width=30,
                                        command=user_calculation).pack()
        return user_calculation

    def video_stream(source):
        if source == 'computer webcam':
            print('computer webcam was source', source)
            source = 0
            # triangulation, frame, text, results = get_video_feed(source)
            circles, frame, coord = get_video_feed(source)
        elif source == 'laser webcam':
            # change back to 1 when program is set to run
            # feed = '/Users/kelsyvaughn/Local/Code/Laser_App/Media/MyOutputVid5.avi'
            source = 1
            # triangulation, frame, text, results = get_video_feed(source)
            circles, frame, coord = get_video_feed(source)
        elif source == 'local':
            source = feed
            # triangulation, frame, text, results = get_video_feed(source)
            circles, frame, coord = get_video_feed(source)
        else:
            # triangulation, frame, text, results = get_video_feed(source)
            circles, frame, coord = get_video_feed(source)

        # _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, video_stream)
        # user_results = run_user_calculations(coord, frame)

        # user_calculation_btn = tk.Button(root, text='select individual coordinates', width=30,
        #                                  command=run_user_calculations(coord, frame)).pack()

        # print('this is what coord returns', coord)

    video_stream(feed)
    root.mainloop()


if __name__ == "__main__":
    main()
