import cv2, time
import numpy as np

cv2.startWindowThread()

cap = cv2.VideoCapture(0)

base_image = None

start_time = time.time()

fps=20

interval = int(1000/fps)

while(True):
    # reading the frame
    ret, frame = cap.read()

    ##convert to grayscale
    gray_scale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    gray_scale = cv2.GaussianBlur(gray_scale, (21,21), 0)

    motion = False

    curr_time = time.time()
    delta_time = curr_time - start_time

    if base_image is None or delta_time > 10.0:
        base_image = gray_scale
        start_time = curr_time

    diff_frame = cv2.absdiff(base_image, gray_scale)

    thresh_frame = cv2.threshold(diff_frame, 15, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    for contour in cnts:
        if cv2.contourArea(contour) < 5000:
            continue
        motion = True

        (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle around the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Displaying image in gray_scale
    cv2.imshow("Gray Frame", gray_scale)

    # Displaying the difference in currentframe to
    # the staticframe(very first_frame)
    cv2.imshow("Difference Frame", diff_frame)

    # Displaying the black and white image in which if
    # intensity difference greater than 30 it will appear white
    cv2.imshow("Threshold Frame", thresh_frame)

    # Displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)

    if cv2.waitKey(interval) & 0xFF == ord('q'):
        # breaking the loop if the user types q
        # note that the video window must be highlighted!
        break

cap.release()
cv2.destroyAllWindows()
