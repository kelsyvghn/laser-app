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
    app.grid()
    # Create a label in the frame
    lmain = tk.Label(app)
    lmain.grid()

    source_options = ['computer webcam', 'laser webcam', 'local']

    # give user option to adjust camera brightness
    # contrast and brightness sliders
    contrast_value = tk.DoubleVar()
    contrast_value.set(1.4)

    bright_value = tk.IntVar()
    bright_value.set(40)

    contrast_slider = tk.Scale(
        root,
        from_=1.0,
        to=3.0,
        resolution=0.01,
        orient='horizontal',
        label="Contrast"
    )
    print('contrast value', contrast_value)
    contrast_slider.grid(row=0, column=1, sticky=W, pady=2)
    bright_slider = tk.Scale(
        root,
        from_=0,
        to=100,
        orient='horizontal',
        label="Brightness"
    )
    print('brightness value', bright_value)
    bright_slider.grid(row=2, column=1, sticky=W, pady=2)
    user_selected_contrast = float(contrast_slider.get())
    user_selected_brightness = int(bright_slider.get())

    # slider_changes_btn = tk.Button(root, text='Adjust Brightness and Contrast',
    #                                command=lambda: user_adjustments(user_selected_contrast,
    #                                                                 user_selected_brightness, user_selected_gamma))

    def change_feed():
        tk.Label.config(text=video_stream(feed_selection.get()))

    feed_label = tk.Label(root, text="Feed Selection")
    feed_label.grid(row=1, column=0, pady=2)
    feed_selection = tk.StringVar()
    feed_selection.set('laser webcam')

    drop = tk.OptionMenu(root, feed_selection, *source_options)
    drop.grid(row=2, column=0, pady=2)

    source_btn = tk.Button(root, text='Run Feed', width=30, command=change_feed).grid(row=3, column=0, pady=2)

    # instantiates a list box to display found coordinates
    user_selection_list = tk.Listbox(root, selectmode="multiple")
    user_selection_list.grid(row=4, column=1, sticky=W, pady=2)


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

        if feed_source == 'computer webcam':
            feed_source = 0
            circles, frame, coord = get_video_feed(feed_source, user_selected_contrast,
                                                   user_selected_brightness)
            # circles, frame, coord = get_video_feed(feed_source)

        elif feed_source == 'laser webcam':
            # change back to 1 when program is set to run
            feed_source = 1
            # feed_source = 1
            circles, frame, coord = get_video_feed(feed_source, user_selected_contrast,
                                                   user_selected_brightness)
            # circles, frame, coord = get_video_feed(feed_source)

        elif feed_source == 'local':
            feed_source = feed
            circles, frame, coord = get_video_feed(feed_source, user_selected_contrast,
                                                   user_selected_brightness)
            # circles, frame, coord = get_video_feed(feed_source)

        else:
            feed_source = feed
            circles, frame, coord = get_video_feed(feed_source, user_selected_contrast,
                                                   user_selected_brightness)
            # circles, frame, coord = get_video_feed(feed_source)

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
        # should couple this with the ability to run video feed first, then run the circle finder portion/triangulation

        selection_btn = tk.Button(root, text='select coordinates and click to process', width=30,
                                  command=lambda: user_calculations(coord, frame)).grid(row=6, column=1, sticky=W, pady=2)

        # print('this is what coord returns', coord)

    root.mainloop()


if __name__ == "__main__":
    main()
