# This is a sample Python script.
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from duplicate_single_page_laser_app import *

feed = '/Users/kelsyvaughn/Local/Code/Laser_App/Media/MyOutputVid6.avi'


def main():
    # give user the option to use local camera or external webcam, or another device (can cycle from 0-3)
    # take user input and convert to proper format for 'feed' variable
    root = tk.Tk()
    root.title("Laser Camera Feed")
    app = tk.Frame(root, borderwidth=4, bg="black")
    app.pack()
    # Create a label in the frame
    lmain = tk.Label(app)
    lmain.pack()

    source_options = ['computer webcam', 'laser webcam', 'local']

    # give user option to adjust camera brightness
    # contrast and brightness sliders
    contrast_value = tk.DoubleVar()
    contrast_value = 1.0

    bright_value = tk.IntVar()
    bright_value = 100

    contrast_label = tk.Label(root, text="Contrast")
    contrast_label.pack()
    contrast_slider = tk.Scale(
        root,
        from_=1.0,
        to=3.0,
        orient='horizontal'
    )
    print('contrast value', contrast_value)
    contrast_slider.pack()
    #
    bright_label = tk.Label(root, text="Brightness")
    bright_label.pack()
    bright_slider = tk.Scale(
        root,
        from_=0,
        to=100,
        orient='horizontal'
    )
    print('brightness value', bright_value)
    bright_slider.pack()
    user_selected_contrast = contrast_slider.get()
    user_selected_brightness = bright_slider.get()



    def change_feed():
        tk.Label.config(text=video_stream(feed_selection.get()))

    feed_label = tk.Label(root, text="Feed Selection")
    feed_label.pack()
    feed_selection = tk.StringVar()
    feed_selection.set('laser webcam')

    drop = tk.OptionMenu(root, feed_selection, *source_options)
    drop.pack()

    source_btn = tk.Button(root, text='Process Changes and Receive Feed', width=30, command=change_feed).pack()

    # instantiates a list box to display found coordinates
    user_selection_list = tk.Listbox(root, selectmode="multiple")
    user_selection_list.pack(fill='both')

    # selected = tk.StringVar()

    def get_selected():
        selected_items = []
        for item in user_selection_list.curselection():
            # selection = user_selection_list.get(item)
            selected_items.append(item)
        print('items selected', selected_items)
        return selected_items

    def user_calculations(coordinates, image):
        # # goes through the listbox to see which coordinates the user selected
        # needs to wait until user selects something...
        user_selection = get_selected()
        triangulate_coords = triangulate_user_selection(coordinates, user_selection, image)
        return triangulate_coords

    def video_stream(feed_source):
        slider_changes_btn = tk.Button(root, text='Adjust Brightness and Contrast',
                                       command=lambda: user_adjustments(frame, user_selected_contrast,
                                                                        user_selected_brightness))

        if feed_source == 'computer webcam':
            # print('computer webcam was feed_source', feed_source, contrast_value, bright_value)
            feed_source = 0
            # circles, frame, coord = get_video_feed(feed_source, contrast_value, bright_value)
            circles, frame, coord = get_video_feed(feed_source)

        elif feed_source == 'laser webcam':
            # change back to 1 when program is set to run
            feed_source = feed
            # feed_source = 1
            # circles, frame, coord = get_video_feed(feed_source, contrast_value, bright_value)
            circles, frame, coord = get_video_feed(feed_source)

        elif feed_source == 'local':
            feed_source = feed
            # circles, frame, coord = get_video_feed(feed_source, contrast_value, bright_value)
            circles, frame, coord = get_video_feed(feed_source)

        else:
            feed_source = feed
            # circles, frame, coord = get_video_feed(feed_source, contrast_value, bright_value)
            circles, frame, coord = get_video_feed(feed_source)

        # _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        # lmain.after(1, video_stream)

        # coord is the list, already created/returned from the previous run of the video feed
        # loops through each found coordinate and displays in listbox
        for each_coord in range(len(coord)):
            # print('this is the coord', coord[each_coord])
            user_selection_list.insert(tk.END, coord[each_coord])


        # print('user selection results', user_selection)
        selection_btn = tk.Button(root, text='select coordinates and click to process', width=30,
                                  command=lambda: user_calculations(coord, frame)).pack()


        # print('this is what coord returns', coord)

    root.mainloop()


if __name__ == "__main__":
    main()
