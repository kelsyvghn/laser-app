import cv2
import numpy as np
import math as m
# from main import *
from calibration import *


# running webcam
# feed = cv2.VideoCapture(1)
# running internal video
feed = cv2.VideoCapture('/Users/kelsyvaughn/Local/Code/Laser_App/Media/MyOutputVid6.avi')


def triangulate_circles(coordinates, copy):
    while len(coordinates) >= 2:
        for i in range(len(coordinates)-1):
            x1 = coordinates[i][0]
            y1 = coordinates[i][1]
            x2 = coordinates[i+1][0]
            y2 = coordinates[i+1][1]
        angle = 60
        ax = x2 - x1
        by = y2 - y1
        d = m.sqrt(m.pow(ax, 2) + m.pow(by, 2) - (2 * ax * by) * m.cos(angle)) * 81.73 / 1000
        x3, y3, image = get_point(x1, y1, x2, y2, copy)
        return x3, y3, image
    else:)
        return 0, 0, copy


def get_point(x1, y1, x2, y2, image):
    dx = x2 - x1
    dy = y2 - y1
    alpha = 60. / 180 * m.pi
    xp = x1 + m.cos(alpha) * dx + m.sin(alpha) * dy
    yp = y1 + m.sin(-alpha) * dx + m.cos(alpha) * dy
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


def draw_the_circles(image, circles):
    print('circles', circles)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        x, y, image = triangulate_circles(circles, image)
        cv2.imshow('circles outlined', image)
        circles = x, y
        return circles, image
    elif circles is None:
        print('there were no circles found')
        return circles, image


def get_detected_rings(image):
    blur = cv2.GaussianBlur(image, (15, 15), 1)
    lower_green = np.array([10, 10, 0])
    upper_green = np.array([25, 25, 255])
    mask = cv2.inRange(blur, lower_green, upper_green)
    masked_image = cv2.bitwise_and(image, image, mask=mask)
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


def get_video_feed(video):
    while video.isOpened():
        is_grabbed, frame = video.read()
        if not is_grabbed:
            break
        undistorted_frame = calibration(frame)
        returned_frame, triangulation = get_detected_rings(undistorted_frame)
        cv2.imshow("Circle Detection Video", returned_frame)
        cv2.waitKey(1)
        video.release()
        return triangulation, returned_frame


get_circles = get_video_feed(feed)
cv2.destroyAllWindows()
