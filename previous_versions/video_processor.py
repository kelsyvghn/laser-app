from __future__ import print_function
import tkinter
import PIL
import cv2
import numpy as np
import math as m
from wand.wand.image import Image

# running webcam
# feed = 1
# running internal video
feed = '/Users/kelsyvaughn/Local/Code/Laser_App/Media/MyOutputVid6.avi'


def get_point(x1, y1, x2, y2, image):
    dx = x2 - x1
    dy = y2 - y1
    alpha = 60. / 180 * m.pi
    # rotate the displacement vector and add the result back to the original point
    xp = x1 + m.cos(alpha) * dx + m.sin(alpha) * dy
    yp = y1 + m.sin(-alpha) * dx + m.cos(alpha) * dy
    # if the above are out of range, ie they're outside the mask, process the inverse
    if xp < 200 or xp > 600 or yp < 100 or yp > 500:
        xp = x1 + m.cos(alpha) * dx + m.sin(-alpha) * dy
        yp = y1 + m.sin(alpha) * dx + m.cos(alpha) * dy
    xp = int(xp)
    yp = int(yp)
    cx = int(round((x1 + x2 + xp) / 3, 2))
    cy = int(round((y1 + y2 + yp) / 3, 2))
    cv2.rectangle(image, (xp - 5, yp - 5), (xp + 5, yp + 5), (255, 255, 0), -2)
    cv2.putText(image, "Triangulation Point", (xp - 25, yp - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 0),
                2)
    cv2.rectangle(image, (cx - 5, cy - 5), (cx + 5, cy + 5), (255, 255, 0), -2)
    cv2.putText(image, "Centroid of Triangle: ", (cx - 25, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 0),
                2)
    return xp, yp, image


def triangulate_circles(coordinates, copy):
    while len(coordinates) >= 2:
        for i in range(len(coordinates) - 1):
            x1 = coordinates[i][0]
            y1 = coordinates[i][1]
            x2 = coordinates[i + 1][0]
            y2 = coordinates[i + 1][1]
        angle = 60
        ax = x2 - x1
        by = y2 - y1
        d = m.sqrt(m.pow(ax, 2) + m.pow(by, 2) - (2 * ax * by) * m.cos(angle)) * 81.73 / 1000

        x3, y3, image = get_point(x1, y1, x2, y2, copy)
        return x3, y3, image
    else:
        return 0, 0, copy


def draw_the_circles(image, circles):
    print('circles', circles)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        x, y, image = triangulate_circles(circles, image)
        # print('the calculated triangulation is: ', triangulation)
        cv2.imshow('circles outlined', image)
        circles = x, y
        return circles, image
    elif circles is None:
        print('there were no circles found')
        return circles, image


class App:
    def __init__(self, window, window_title, video_source=feed):
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_find_circles = tkinter.Button(window, text="Find Circles", width=50, command=self.get_detected_rings)
        self.btn_find_circles.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    # method for getting rings on the given frame
    def get_detected_rings(self):
        ret, image = self.vid.get_frame()
        # adjust any distortion of the camera
        with Image(image) as img:
            args = (
                0.2,  # A
                0.0,  # B
                0.0,  # C
                1.0,  # D
                )
            img.destort('barrel', args)
        blur = cv2.GaussianBlur(image, (15, 15), 1)
        lower_green = np.array([10, 10, 0])
        upper_green = np.array([25, 25, 255])
        mask = cv2.inRange(blur, lower_green, upper_green)
        masked_image = cv2.bitwise_and(image, image, mask=mask)
        # mask outer area
        height, width, rgb = image.shape
        x = np.zeros([height, width], dtype='uint8')
        mask_outer = cv2.rectangle(x, (100, 100), (450, 450), (255, 255, 255), -1)
        masked_outer = cv2.bitwise_and(masked_image, masked_image, mask=mask_outer)
        grey_image = cv2.cvtColor(masked_outer, cv2.COLOR_BGR2GRAY)
        canny_image = cv2.Canny(grey_image, 7, 9)
        circles = cv2.HoughCircles(canny_image, cv2.HOUGH_GRADIENT, 2.75, 75, param1=300, param2=150, minRadius=10,
                                   maxRadius=30)
        circles = np.uint16(np.around(circles))
        triangulated, image_with_circles = draw_the_circles(image, circles)
        cv2.imshow('generated circles', image_with_circles)
        return triangulated, image_with_circles

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            pass

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            print('ret: ', ret)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR3
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            ret = 'Fail'
            return ret, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        # Create a window and pass it to the Application object


App(tkinter.Tk(), "Tkinter and OpenCV")
