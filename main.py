import cv2
import time
from emailing import send_email

video = cv2.VideoCapture(1)
time.sleep(1)


first_frame = None
status_list = []
while True:
    #No object detected
    object_status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 55, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dilated_frame)

    contours, check = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            #Object detected
            object_status = 1
    #Add object status to the list    
    status_list.append(object_status)
    #Keep the last two statuses
    status_list = status_list[-2:]
    print(status_list)
    #If the last two statuses are 1 and 0, then an object was detected and then it left the frame
    if status_list[0] == 1 and status_list[1] == 0:
            send_email()


    
    cv2.imshow("Caputre", frame)


    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()


