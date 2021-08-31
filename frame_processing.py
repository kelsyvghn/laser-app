import math as m
import cv2
import numpy as np





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
        # cv2.waitKey(0)
    elif circles is None:
        print('there were no circles found')
        return circles, image


# method for getting rings on the given frame
def get_detected_rings(self):
    ret, image = self.vid.get_frame()
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
