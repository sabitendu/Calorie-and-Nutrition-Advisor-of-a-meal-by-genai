import streamlit as st
import google.generativeai as genai 
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv() 

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate response with given prompt and image
def nutri_response(input_prompt, image_data):
    # Call the model
    model = genai.GenerativeModel("gemini-pro-vision")
    # Generate response
    response = model.generate_content([input_prompt, image_data])
    return response.text

# The uploaded image data should be taken out by model in a format in this case google gemini pro can understand
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Open the image using PIL
        image = Image.open(uploaded_file)
        return image
    else:
        raise FileNotFoundError("No file uploaded")

## Initialize the Streamlit app front end setup

# Set the page name
st.set_page_config(page_title="Calorie Advisor App")

# Set the header
st.header("Calorie Calculation and Advising")

# Set the file uploader
uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Set the submit button
submit = st.button("Tell me about Total Calories")

# Set the input prompt for desired result
input_prompt = """
You are an expert nutritionist. You will receive images of food items.
Calculate the total calories, and provide details of each food item with calorie intake in the format below:

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----

"""

# If submit button is clicked
if submit:
    # Get image data
    image_data = input_image_setup(uploaded_file)
    # Load the response
    response = nutri_response(input_prompt, image_data)
    # Header of the response
    st.header("The Response for the Food Item is")
    # Write the response
    st.write(response)

