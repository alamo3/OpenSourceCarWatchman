import cv2


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def run_pipeline(frame, base_image):

    ##convert to grayscale
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_scale, scaleFactor=1.3, minNeighbors=5)

    gray_scale = cv2.GaussianBlur(gray_scale, (21, 21), 0)

    motion = False

    diff_frame = cv2.absdiff(base_image, gray_scale)

    thresh_frame = cv2.threshold(diff_frame, 15, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cntsMotion = []

    for contour in cnts:
        if cv2.contourArea(contour) < 5000:
            continue

        cntsMotion.append(contour)
        motion = True

    return faces, cntsMotion, motion, diff_frame, thresh_frame

