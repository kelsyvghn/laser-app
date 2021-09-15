import numpy as np
import cv2 as cv
cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    print('ret, frame', (ret, frame))
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    # brightness and contrast controls
    # ***** 6 ***** create user control sliders for this
    # alpha = val1  # Simple contrast control
    # beta = val2  # Simple brightness control
    # Initialize values
    # print(' Basic Linear Transforms ')
    # print('-------------------------')
    try:
        # will need to pass down variables from main into these (instead of command line input)
        alpha = 1.4
        beta = 40

        # gamma = 2.5

    except ValueError:
        print('Error, not a number')
    # print('current val1 and val2 values: ', (val1, val2))

    # Do the operation new_image(i,j) = alpha*image(i,j) + beta
    # Instead of these 'for' loops we could have used simply:
    new_image = cv.convertScaleAbs (frame, alpha=alpha, beta=beta)

    cv.imshow('frame', new_image)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()