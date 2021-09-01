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
    # find length of the coordinates value
    # cycle through coordinates to find best ones to use
    # print('these are the coordinates: ', coordinates)
    # if there are more than 3 values
    while len(coordinates) >= 2:

    # if len(coordinates) >= 2:
    #     # x1 = coordinates[0][0]
    #     # x2 = coordinates[1][0]
    #     # y1 = coordinates[0][1]
    #     # y2 = coordinates[1][1]
        for i in range(len(coordinates)-1):
            x1 = coordinates[i][0]
            y1 = coordinates[i][1]
            x2 = coordinates[i+1][0]
            y2 = coordinates[i+1][1]
        # calculation the distance between two circle centers using known angle (equilateral triangle, so 60)
        angle = 60
        ax = x2 - x1
        by = y2 - y1
        d = m.sqrt(m.pow(ax, 2) + m.pow(by, 2) - (2 * ax * by) * m.cos(angle)) * 81.73 / 1000
    #     print('distance between two circles: ', d)
    #     # print('the distance between the coordinates: ', d)
    #     # calculate the coordinates to the center circle/camera center
    #     # # the x3 y3 coordinates are calculated as follows
    #     # cv2.imshow('triangulated circles', copy)
    #     # cv2.waitKey(0)
        x3, y3, image = get_point(x1, y1, x2, y2, copy)
        return x3, y3, image
    else:
    # else:
    #     print('there was not enough information to complete this request', coordinates)
        return 0, 0, copy


def get_point(x1, y1, x2, y2, image):
    # print('the given center values are : ', (x1, y1, x2, y2))

    # express coordinates of the point (x2, y2) with respect to point (x1, y1)
    dx = x2 - x1
    dy = y2 - y1

    alpha = 60. / 180 * m.pi
    # rotate the displacement vector and add the result back to the original point
    xp = x1 + m.cos(alpha) * dx + m.sin(alpha) * dy
    yp = y1 + m.sin(-alpha) * dx + m.cos(alpha) * dy

    # print('the xp and yp are: ', (xp, yp))
    # if the above are out of range, ie they're outside the mask, process the inverse
    # first we need to verify that the xp and yp are out of the masking bounds - the triangulation point
    # the masking range is (200, 100) (600, 500) so out of bounds would be 200 < x < 600 and 100 < y < 500
    #
    if xp < 200 or xp > 600 or yp < 100 or yp > 500:
        xp = x1 + m.cos(alpha) * dx + m.sin(-alpha) * dy
        yp = y1 + m.sin(alpha) * dx + m.cos(alpha) * dy

    xp = int(xp)
    yp = int(yp)
    # print('the new xp and yp are: ', (xp, yp))

    # calculate the centroid of the triangle if the points are on opposite sides
    # Formula to calculate centroid
    cx = int(round((x1 + x2 + xp) / 3, 2))
    cy = int(round((y1 + y2 + yp) / 3, 2))

    # print("Centroid ", (cx, cy))
    cv2.rectangle(image, (xp - 5, yp - 5), (xp + 5, yp + 5), (255, 255, 0), -2)
    cv2.putText(image, "Triangulation Point", (xp - 25, yp - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 0),
                2)
    cv2.rectangle(image, (cx - 5, cy - 5), (cx + 5, cy + 5), (255, 255, 0), -2)
    cv2.putText(image, "Centroid of Triangle: ", (cx - 25, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 0),
                2)
    # cv2.imshow('Triangulation Image', image)
    # cv2.imwrite('triangulation.jpg', image)
    # cv2.waitKey(0)
    return xp, yp, image


# video = several frames (images shown after each other)
# draw circles onto the video frames, image by image
def draw_the_circles(image, circles):
    # for i in circles[0, :]:
    #     # outer circle
    #     cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
    #
    #     # center of circle
    #     cv2.circle(image, (i[0], i[1]), 2, (0, 255, 0), 3)
    #     # cv2.rectangle(image, (i[0] - 5, i[1] - 5), (i[0] + 5, i[1] + 5), (0, 128, 255), -1)
    print('circles', circles)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        x, y, image = triangulate_circles(circles, image)
        # print('the calculated triangulation is: ', triangulation)
        cv2.imshow('circles outlined', image)
        circles = x, y
        return circles, image
        # cv2.waitKey(0)
    elif circles is None:
        print('there were no circles found')
        return circles, image


# method for getting rings on the given frame
def get_detected_rings(image):
    # (height, width) = (image.shape[0], image.shape[1])
    # blur image a bit to tone down brightness
    blur = cv2.GaussianBlur(image, (15, 15), 1)
    # lower_green = np.array([10, 10, 0])
    # upper_green = np.array([25, 25, 255])
    lower_green = np.array([10, 10, 0])
    upper_green = np.array([25, 25, 255])
    mask = cv2.inRange(blur, lower_green, upper_green)
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # mask outer area
    height, width, rgb = image.shape
    # video is 1280, 720
    x = np.zeros([height, width], dtype='uint8')
    mask_outer = cv2.rectangle(x, (100, 100), (450, 450), (255, 255, 255), -1)
    # mask = cv2.rectangle(x, (0, 0), (width, height), (255, 255, 255), -1)
    masked_outer = cv2.bitwise_and(masked_image, masked_image, mask=mask_outer)

    # turn image to greyscale
    grey_image = cv2.cvtColor(masked_outer, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('Test/grey_image1.jpg', grey_image)

    # use Canny's edge detection to detect edges
    canny_image = cv2.Canny(grey_image, 7, 9)
    cv2.imwrite('Test/canny_image.jpg', canny_image)

    # add and apply mask to the image (not written yet)

    # generate circles on the image
    # circles = cv2.HoughCircles(canny_image, cv2.HOUGH_GRADIENT, 2.75, 1.5, param1=300, param2=100, minRadius=0,
    #                            maxRadius=45)
    circles = cv2.HoughCircles(canny_image, cv2.HOUGH_GRADIENT, 2.75, 75, param1=300, param2=150, minRadius=10,
                               maxRadius=30)
    # circles = cv2.HoughCircles(canny_image, cv2.HOUGH_GRADIENT, 1, 120, param1=100, param2=30, minRadius=5,
    # maxRadius=0)

    # convert to uint
    circles = np.uint16(np.around(circles))

    # generate circles onto the image with another method

    triangulated, image_with_circles = draw_the_circles(image, circles)
    cv2.imshow('generated circles', image_with_circles)

    return triangulated, image_with_circles


def get_video_feed(video):
    # the code below opens the video, grabs it frame by frame and then runs the above methods on the frames
    while video.isOpened():

        is_grabbed, frame = video.read()

        if not is_grabbed:
            break
            # need to callibrate camera before this runs
        # undistorted_frame = calibration(frame)
        frame, triangulation = get_detected_rings(frame)
        # print('the frame pixels', frame)
        # coins = get_detected_rings(coin_image)
        # frame = get_detected_lanes(frame)
        # height, width = frame.shape
        # cv2.imshow("Circle Detection Video", frame)
        # cv2.waitKey(0)
        video.release()
        return triangulation, frame


get_circles = get_video_feed(feed)
cv2.destroyAllWindows()
