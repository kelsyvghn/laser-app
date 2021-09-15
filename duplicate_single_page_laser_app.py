import cv2
import numpy as np
import math as m
import glob


def triangulate_circles(coordinates, copy):
    print('coordinates passed through', coordinates)
    # create an if statement that allows for if len(coordinates is < 2 OR if the user has provided coordinates
    while len(coordinates) > 2:
        for i in range(len(coordinates) - 1):
            x1 = coordinates[i][0]
            y1 = coordinates[i][1]
            x2 = coordinates[i + 1][0]
            y2 = coordinates[i + 1][1]
        angle = 60
        ax = x2 - x1
        by = y2 - y1
        d = m.sqrt(m.pow(ax, 2) + m.pow(by, 2) - (2 * ax * by) * m.cos(angle)) * 81.73 / 1000
        # print('d is', d)

        x3, y3, image = get_point(x1, y1, x2, y2, copy)
        cv2.putText(image, f'(x, y): {x3, y3}.', (x3, y3), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        results = (x3, y3, image, d, coordinates)
        return results
    else:
        results = None
        return results


def get_point(x1, y1, x2, y2, image):
    # add user input to above pass-down ( can change what is passed down from triangulate_circles )
    # calculate dx and dy based on user given coordinates

    # express coordinates of the point (x2, y2) with respect to point (x1, y1)
    dx = x2 - x1
    dy = y2 - y1

    alpha = 60. / 180 * m.pi
    # rotate the displacement vector and add the result back to the original point
    xp = x1 + m.cos(alpha) * dx + m.sin(alpha) * dy
    yp = y1 + m.sin(-alpha) * dx + m.cos(alpha) * dy
    print('first xp and yp output', (xp, yp))
    # # if the above are out of range, ie they're outside the mask, process the inverse
    # if xp < 100 or xp > 450 or yp < 100 or yp > 450:
    #     print('outside mask, triangulation was flipped')
    #     xp = x1 + m.cos(alpha) * dx + m.sin(-alpha) * dy
    #     yp = y1 + m.sin(alpha) * dx + m.cos(alpha) * dy
    # print('second xp and yp output', (xp, yp))
    # reduces the decimal points to 2
    xp = int(xp)
    yp = int(yp)
    print('third xp and yp output', (xp, yp))

    # Formula to calculate centroid
    # cx = int(round((x1 + x2 + xp) / 3, 2))
    # cy = int(round((y1 + y2 + yp) / 3, 2))

    # print("Centroid ", (cx, cy))
    cv2.rectangle(image, (xp - 5, yp - 5), (xp + 5, yp + 5), (255, 255, 0), -2)
    cv2.putText(image, "Triangulation Point", (xp - 25, yp - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 0), 2)
    # cv2.rectangle(image, (cx - 5, cy - 5), (cx + 5, cy + 5), (255, 255, 0), -2)
    # cv2.putText(image, "Centroid of Triangle", (cx - 25, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #             (255, 255, 0),
    #             2)

    return xp, yp, image


def triangulate_user_selection(coordinates, indexes, copy):
    print('coordinates passed through', coordinates, indexes)
    # the original coordinates are passed through, along with the indexes
    # that the user has chosen
    while len(coordinates) >= 2:
        # x1, y1 will be the first index that the user passed down, etc
        x1 = coordinates[indexes[0]][0]
        y1 = coordinates[indexes[0]][1]
        x2 = coordinates[indexes[1]][0]
        y2 = coordinates[indexes[1]][1]
        print('user selected coordinates: ', ((x1, y1), (x2, y2)))
        angle = 60
        ax = x2 - x1
        by = y2 - y1
        d = m.sqrt(m.pow(ax, 2) + m.pow(by, 2) - (2 * ax * by) * m.cos(angle)) * 81.73 / 1000
        # print('d is', d)

        x3, y3, image = get_point(x1, y1, x2, y2, copy)
        cv2.putText(image, f'(x, y): {x3, y3}.', (x3, y3), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        results = (x3, y3, image, d, coordinates)
        cv2.imshow('user selected coordinates triangulation', copy)
        return results
    else:
        results = None
        return results


# draw circles onto the video frames, image by image
def draw_the_circles(image, circles):
    # print('circles', circles)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            # this will print the coordinates on each circle
            cv2.putText(image, f'coordinates: {x, y}.', (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
        # this next function call passes down the coordinates of the circles,
        # it should also pass down any user selections
        # to do that it needs to return all the coordinate c
        # x, y, image, dist, coordinates = triangulate_circles(circles, image)
        # cv2.imshow('circles outlined', image)
        # circles = x, y
        # removed triangulation process here to avoid overlay and allow only for user selection of coordinates
        # return circles, image, coordinates
        return circles, image, circles
    elif circles is None:
        print('there were no circles found')
        return circles, image, circles


def user_adjustments(image, contrast_value, bright_value):
    # brightness and contrast controls
    # ***** 6 ***** create user control sliders for this
    # alpha = val1  # Simple contrast control
    # beta = val2  # Simple brightness control
    # Initialize values
    # print(' Basic Linear Transforms ')
    # print('-------------------------')
    try:
        # will need to pass down variables from main into these (instead of command line input)
        # alpha = 1.4
        # beta = 40
        alpha = contrast_value
        beta = bright_value

    except ValueError:
        print('Error, not a number')
    print('current user adjustment values: ', (alpha, beta))

    # Do the operation new_image(i,j) = alpha*image(i,j) + beta
    # Instead of these 'for' loops we could have used simply:
    new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    # but we wanted to show you how to access the pixels :)
    # for y in range(image.shape[0]):
    #     for x in range(image.shape[1]):
    #         for c in range(image.shape[2]):
    #             new_image[y, x, c] = np.clip(alpha * image[y, x, c] + beta, 0, 255)
    return new_image

    # blur image a bit to tone down brightness on particular portions


# method for getting rings on the given frame
# def get_detected_rings(image, val1, val2):
def get_detected_rings(image):
    # new_image = np.zeros(image.shape, image.dtype)
    cv2.imwrite('Test/input_img.jpg', image)
    # 1 add a control for this ?
    # was 15
    blur = cv2.GaussianBlur(image, (3, 3), 1)
    cv2.imwrite('Test/blur_img.jpg', blur)
    # ***** 2 ***** add a control for this color order is BGR (Blue, Green, Red)
    lower_green = np.array([18, 18, 0])
    # ***** 3 ***** add a control for this
    upper_green = np.array([50, 50, 255])
    mask = cv2.inRange(blur, lower_green, upper_green)
    cv2.imwrite('Test/mask_img.jpg', mask)
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    cv2.imwrite('Test/masked_img.jpg', masked_image)

    # mask outer area
    height, width, rgb = image.shape

    x = np.zeros([height, width], dtype='uint8')
    # ***** 4 ***** add a control for this, in case frame is too small/large
    mask_outer = cv2.rectangle(x, (100, 100), (450, 450), (255, 255, 255), -1)
    masked_outer = cv2.bitwise_and(masked_image, masked_image, mask=mask_outer)

    # turn image to greyscale
    grey_image = cv2.cvtColor(masked_outer, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('Test/grey_image.jpg', grey_image)

    # use Canny's edge detection to detect edges
    canny_image = cv2.Canny(grey_image, 7, 9)
    cv2.imwrite('Test/canny_image.jpg', canny_image)

    # generate circles on the image
    circles = cv2.HoughCircles(canny_image, cv2.HOUGH_GRADIENT, 2.75, 75, param1=300, param2=150, minRadius=10,
                               maxRadius=30)
    # convert to uint
    circles = np.uint16(np.around(circles))
    coordinate_of_circles, image_with_circles, prev_coordinates = draw_the_circles(image, circles)
    cv2.imwrite('Test/generated_circles.jpg', image_with_circles)
    # cv2.imshow('generated circles', image_with_circles)

    return coordinate_of_circles, image_with_circles, prev_coordinates


def calibration(frame_input):
    # ***** 5 ***** create a yaml file for this
    chessboardSize = (4, 3)
    frameSize = (640, 480)

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob('*.jpg')

    for image in images:

        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
            # cv2.imshow('img', img)
            # cv2.waitKey(1000)

    cv2.destroyAllWindows()

    ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)
    # print('input frame type', type(frame_input))
    img = frame_input
    h, w = img.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))

    # Undistort
    dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    # cv2.imwrite('Test/caliResult1.png', dst)

    # Undistort with Remapping
    mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    # cv2.imwrite('Test/caliResult2.png', dst)

    # Reprojection Error
    mean_error = 0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error

    print("total error: {}".format(mean_error / len(objpoints)))

    return dst


# def get_video_feed(selection, value1, value2):
def get_video_feed(selection, contrast_value, bright_value):
    video = cv2.VideoCapture(selection)
    while video.isOpened():

        is_grabbed, frame = video.read()

        if not is_grabbed:
            break

        # new_image = user_adjustments(frame, contrast_value, bright_value)
        # cv2.imshow('user adjusted image', new_image)
        # cv2.waitKey(1)
        dst_image = calibration(frame)

        # need to calibrate camera before this runs
        # circle_coordinates, frame, prev_coord = get_detected_rings(dst_image, value1, value2)
        # cv2.imshow('generated circles feed', dst_image)
        cv2.imwrite('Test/dst_image.jpg', dst_image)
        circle_coordinates, frame, prev_coord = get_detected_rings(dst_image)
        # circle_coordinates, frame, prev_coord = [], frame, []
        # cv2.imshow('generated circles feed', dst_image)
        # results = 'the distance between circle centers is: ' + str(round(dist, 3)) + ' or approximately 0' + str(
        #     round((dist * 0.2645833333), 3)) + 'mm'

        video.release()
        # print("Video Feed Processing")
        return circle_coordinates, frame, prev_coord


# get_circles = get_video_feed(feed)
cv2.destroyAllWindows()
