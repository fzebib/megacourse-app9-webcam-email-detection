import cv2
import streamlit as st
import datetime

st.title("Motion Detector")
start = st.button("Start Camera")

if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(1)
    stop = st.button("Stop Camera")



    while True:
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        current_time = str(datetime.datetime.now().replace(microsecond=0))


        cv2.putText(img=frame, text=current_time, org=(50, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=4)

        streamlit_image.image(frame)
        if stop:
            break



