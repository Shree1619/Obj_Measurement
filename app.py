# app.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import utlis

def main():
    st.title("Object Measurement App")

    menu = ["About Us", "Upload Image", "Live Camera Feed"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "About Us":
        st.subheader("About Us")
        st.write("This is a simple object measurement app using OpenCV and Streamlit.")

    elif choice == "Upload Image":
        st.subheader("Upload Image")
        uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image = np.array(image)
            st.image(image, caption="Uploaded Image.", use_column_width=True)

            if st.button("Measure Object"):
                wP = 210  # You can adjust this value according to your needs
                hP = 297  # You can adjust this value according to your needs
                measure_object(image, wP, hP)

    elif choice == "Live Camera Feed":
        st.subheader("Live Camera Feed")
        run_camera()

def measure_object(image, wP, hP):
    imgContours, conts = utlis.getContours(image, minArea=50000, filter=4)
    if len(conts) != 0:
        biggest = conts[0][2]
        imgWarp = utlis.warpImg(image, biggest, image.shape[1], image.shape[0], wP, hP)
        imgContours2, conts2 = utlis.getContours(imgWarp, minArea=2000, filter=4, cThr=[50, 50], draw=False)

        if len(conts2) != 0:
            for obj in conts2:
                cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 1)
                nPoints = utlis.reorder(obj[2])
                nW = round((utlis.findDis(nPoints[0][0] // 0.8, nPoints[1][0] // 0.8) / 10), 1)
                nH = round((utlis.findDis(nPoints[0][0] // 0.8, nPoints[2][0] // 0.8) / 10), 1)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                (nPoints[1][0][0], nPoints[1][0][1]), (0, 0, 255), 1, 8, 0, 0.05)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                (nPoints[2][0][0], nPoints[2][0][1]), (0, 255, 255), 1, 8, 0, 0.05)
                x, y, w, h = obj[3]
                cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
                cv2.putText(imgContours2, '{}cm'.format(nH), (x - 70, y + h // 2),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
            st.image(imgContours2, caption="Measured Object.", use_column_width=True)

def run_camera():
    cap = cv2.VideoCapture(0)
    cap.set(10, 160)
    cap.set(3, 1920)
    cap.set(4, 1080)

    while True:
        success, img = cap.read()
        img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        st.image(img, caption="Live Camera Feed.", use_column_width=True)
        imgContours, conts = utlis.getContours(img, minArea=50000, filter=4)

        if len(conts) != 0:
            biggest = conts[0][2]
            imgWarp = utlis.warpImg(img, biggest, img.shape[1], img.shape[0], wP=210, hP=297)
            imgContours2, conts2 = utlis.getContours(imgWarp, minArea=2000, filter=4, cThr=[50, 50], draw=False)

            if len(conts2) != 0:
                for obj in conts2:
                    cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)
                    nPoints = utlis.reorder(obj[2])
                    nW = round((utlis.findDis(nPoints[0][0] // 1, nPoints[1][0] // 1) / 10), 1)
                    nH = round((utlis.findDis(nPoints[0][0] // 1, nPoints[2][0] // 1) / 10), 1)
                    cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                    (nPoints[1][0][0], nPoints[1][0][1]), (255, 0, 255), 3, 8, 0, 0.05)
                    cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                    (nPoints[2][0][0], nPoints[2][0][1]), (255, 0, 255), 3, 8, 0, 0.05)
                    x, y, w, h = obj[3]
                    cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 0, 255), 2)
                    cv2.putText(imgContours2, '{}cm'.format(nH), (x - 70, y + h // 2),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 0, 255), 2)
                st.image(imgContours2, caption="Measured Object.", use_column_width=True)

        if st.button("Stop Camera"):
            cap.release()
            break

if __name__ == "__main__":
    main()
