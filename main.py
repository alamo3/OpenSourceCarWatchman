import cv2, time
from Algorithm import Pipeline

from Camera import CameraManager


camManager = CameraManager.CamManager()

cv2.startWindowThread()

start_time = time.time()

fps=20

interval = int(1000/fps)


while(True):
    # reading the frame
    ret, frame = camManager.get_image()

    base_image = camManager.get_recent_image()

    faces, cnts, motion, diff_frame, thresh_frame = Pipeline.run_pipeline(frame, base_image)

    curr_time = time.time()
    delta_time = curr_time - start_time

    if delta_time > 4.0:
        camManager.next_camera()
        camManager.update_recent_image()
        start_time = curr_time

    for contour in cnts:

        (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle around the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)


    # Displaying the difference in currentframe to
    # the staticframe(very first_frame)
    cv2.imshow("Difference Frame", diff_frame)

    # Displaying the black and white image in which if
    # intensity difference greater than 30 it will appear white
    cv2.imshow("Threshold Frame", thresh_frame)
    # Displaying color frame with contour of motion of object
    frame = cv2.putText(img= frame, text="Camera "+str(camManager.current_cam + 1), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0, 255, 0), thickness=2, org=(0,20))
    frame = cv2.putText(img= frame, text="Motion: "+str(motion), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0, 255, 0) if motion else (0,0,255), thickness=2, org=(0,40))

    cv2.imshow("Color Frame", frame)



    if cv2.waitKey(interval) & 0xFF == ord('q'):
        # breaking the loop if the user types q
        # note that the video window must be highlighted!
        break

camManager.shutdown_camera_manager()
cv2.destroyAllWindows()
