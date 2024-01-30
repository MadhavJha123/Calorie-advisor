import streamlit as st
import google.generativeai as genai
from PIL import Image
import cv2
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt, image[0]])
    return response.text

def image_setup(file):
    if file is not None:
        bytes_data = file.getvalue()

        image_parts = [
            {
                "mime_type": file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File selected")

st.set_page_config(page_title="Calorie Advisor App")

st.header("Calorie Advisor App")

# Option to choose between image upload and live camera capture
option = st.radio("Choose Image Source:", ("Upload Image", "Capture Live Image"))

if option == "Upload Image":
    uploaded_file = st.file_uploader("Choose a meal image...", type=['jpg', 'jpeg', 'png', 'jfif'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

elif option == "Capture Live Image":
    st.subheader("Live Camera Capture")
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #st.image(frame_rgb, caption="Live Camera Feed", use_column_width=True)

    # Capture live image on button click
    if st.button("Capture Image"):
        
        captured_image = Image.fromarray(frame_rgb)
        st.image(captured_image, caption="Captured Image", use_column_width=True)
        capture.release()

    

submit = st.button("Show Total Calories")

prompt = """
You are an expert in nutritionist where you need to see the food items from the image and calculate the 
total calories, also provide the details of every food item with calorie intake in below format
 1. Item 1 - no. of calories
 2. Item 2 - no. of calories
 ---
 ---
 Finally also mention whether the food is healthy or not and also mention the percentage split of 
 the ratio of carbohydrates, fats, fibers, sugar and other important things required in our diet 
 and finally if the diet contains sugar also tell that is this diet safe for diabetic patients or not and if it is safe
 then how much should they eat it.
"""

if submit:
    with st.spinner("Getting recipe details"):
        if option == "Upload Image":
            image_data = image_setup(uploaded_file)
        elif option == "Capture Live Image":
            # Convert the captured image to bytes
            _, buffer = cv2.imencode('.jpg', frame)
            bytes_data = buffer.tobytes()
            image_data = [{"mime_type": "image/jpeg", "data": bytes_data}]
            st.image(image_data[0]['data'])

        response = get_response(prompt, image_data)
        st.header("Details of Calories")
        st.write(response)
