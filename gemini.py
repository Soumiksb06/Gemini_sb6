# Import necessary libraries
import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai
from PIL import Image

# Set up API key
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]  # Ensure your Streamlit app has access to this secret
genai.configure(api_key=GOOGLE_API_KEY)

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# List available models and select one
models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
selected_model_name = st.selectbox("Select a model", models)
model = genai.GenerativeModel(selected_model_name)

# Function to generate content
def generate_content(prompt):
    response = model.generate_content(prompt)
    return response

# Create the app interface
st.title("Generative AI Chatbot with Streamlit")
st.markdown("This is a chatbot interface powered by Generative AI.")

# Chat interface
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_input("You:", key="user_input")
if st.button("Send"):
    if user_input:
        # Display user input
        st.markdown(f"**You:** {user_input}")
        
        # Generate response
        response = generate_content(user_input)
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        st.session_state["chat_history"].append({"role": "bot", "content": response.text})
        
        # Display response
        st.markdown(f"**Bot:** {response.text}")

# Display chat history
st.markdown("## Chat History")
for message in st.session_state["chat_history"]:
    st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

# Embedding functionality (optional, can be expanded as needed)
st.markdown("## Embedding Content")
embed_text = st.text_input("Text to embed:", key="embed_input")
if st.button("Embed Text"):
    result = genai.embed_content(
        model="models/embedding-001",
        content=embed_text,
        task_type="retrieval_document",
        title="Embedding of single string"
    )
    st.write(f"Embedding: {result['embedding']}")

# Image processing (optional, can be expanded as needed)
st.markdown("## Image Processing")
uploaded_image = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    img = Image.open(uploaded_image)
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    
    # Process the image with the model (if applicable)
    # response = model.generate_content(img)
    # st.markdown(to_markdown(response.text))

# Run the app
if __name__ == "__main__":
    st.write("Running the Generative AI Chatbot app")
