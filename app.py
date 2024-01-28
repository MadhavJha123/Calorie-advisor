import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

# credential_path = "application_default_credentials.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(prompt, image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([prompt, image[0]])
    return response.text

def image_setup(file):
    if file is not None:
        bytes_data=file.getvalue()

        image_parts=[
            {
                "mime_type":file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File selected")
    

st.set_page_config(page_title="Calorie Advisor App")

st.header("Calorie Advisor App")
uploaded_file=st.file_uploader("Choose a meal image...",type=['jpg','jpeg','png','jfif'])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="uploaded image", use_column_width=True)

submit=st.button("Show total calories")

prompt="""
You are an expert in nutritionist where you need to see the food items from the image and calculte the 
total calories, also provide the details of every food items with calories intake in below format
 1. Item 1 - no. of calories
 2. Item 2 - no. of calories
 ---
 ---
 Finally also mention whether the food is healthy or not and also mention the percentage split of 
 the ratio of carbohydrates, fats, fibers, sugar and other important thing required in out diet 
 and finally if the diet contains sugar also tell that is this diet safe for diabetic patients or not and if it is safe
 then how much should they eat it.
"""

if submit:
    with st.spinner("Getting recipe details"):
        image_data= image_setup(uploaded_file)
        response= get_response(prompt, image_data)
        st.header("Details of calories")
        st.write(response)