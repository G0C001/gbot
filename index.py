import streamlit as st
import os
import PIL.Image
import google.generativeai as genai

# Configure Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyB4XgWlQ6WOlMjcYnpw6uzFPgm9ug2qwM0"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Create a checkbox to toggle between windows
window_selector = st.checkbox("Click to view Pro And Vision")

# Add content to the first window
if not window_selector:
    st.title("G-Bot-Pro")
    # Add more content for the first window as needed
    try:
        model = genai.GenerativeModel('gemini-pro')

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Ask me Anything"
                }
            ]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        def llm_function(query):
            response = model.generate_content(query)

            with st.chat_message("assistant"):
                st.markdown(response.text)

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": query
                }
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response.text
                }
            )

        query = st.text_input("Type here", key="window1_input")

        if query:
            with st.chat_message("user"):
                st.markdown(query)
            llm_function(query)

    except Exception as e:
        st.error(f"Error: {e}")

# Add content to the second window
else:
    st.title("G-Bot-Vision")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = PIL.Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
    user_input_text = st.text_input("Type here")  
    generate_button = st.button("Generate Content")

    if uploaded_file is not None and generate_button:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([user_input_text, img])
        st.markdown(response.text)