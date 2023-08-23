import streamlit as st
from streamlit_extras.app_logo import add_logo
import speech_recognition as sr
import tensorflow as tf
import tensorflow_hub as hub 
import numpy as np
from transformers import BertTokenizer

page_bg_img = """
<style>

div.stButton > button:first-child {
    width: 200px;
    height: 60px;
    padding: 0.6em 2em;
    border: none;
    outline: none;
    color: rgb(255, 255, 255);
    background: #222;
    cursor: pointer;
    position: relative;
    z-index: 0;
    border-radius: 10px;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

div.stButton > button:before {
    content: "";
  background: linear-gradient(
    45deg,
    #ff0000,
    #ff7300,
    #fffb00,
    #48ff00,
    #00ffd5,
    #002bff,
    #7a00ff,
    #ff00c8,
    #ff0000
  );
  position: absolute;
  top: -2px;
  left: -2px;
  background-size: 400%;
  z-index: -1;
  filter: blur(5px);
  -webkit-filter: blur(5px);
  width: calc(100% + 4px);
  height: calc(100% + 4px);
  animation: glowing-button 20s linear infinite;
  transition: opacity 0.3s ease-in-out;
  border-radius: 10px;
}

@keyframes glowing-button {
    0% {
        background-position: 0 0;
        }
    50% {
        background-position: 400% 0;
        }
    100% {
        background-position: 0 0;
        }
}

div.stButton > button:after {
    z-index: -1;
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    background: #222;
    left: 0;
    top: 0;
    border-radius: 10px;
}


[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1626553683558-dd8dc97e40a4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1887&q=80");
background-size: cover;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}

[data-testid="stSidebar"] > div:first-child {
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
background : black;
}

[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}

[data-testid="stToolbar"] {
right: 2rem;
}

div[role=radiogroup] label:first-of-type {
            visibility: hidden;
            height: 0px;
        }
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
add_logo("https://github.com/NebulaTris/brainsherlock/blob/main/16915065502869741.jpg?raw=true")

st.title("Speech Analysis 🗣️")

st.sidebar.success("Speech Analysis has been selected")

st.write(" Speech Analysis will be done with the use of machine learning python libraries and the use of the webcam. The model will be trained to detect the emotions of the user.")

# Load and compile your mental health prediction model here
model = tf.keras.Sequential([
    hub.KerasLayer("https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1",
                   output_shape=[20], input_shape=[], dtype=tf.string,
                   trainable=True),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam',
              loss=tf.losses.BinaryCrossentropy(from_logits=True),
              metrics=[tf.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])
def postprocessor(preds):
    preds_range = preds.max() - preds.min()
    probab = []
    for i in preds:
        probab.append((i - preds.min()) * 100 / preds_range)
    return np.mean(probab)
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def calculate_mental_health_score(text):
    # Use the model to make predictions
    results = model.predict(np.array([text]))
    
    # Post-process the predictions
    preds_range = results.max() - results.min()
    probab = [((i - results.min()) * 100 / preds_range) for i in results]
    score = np.mean(probab)
    st.write("Your mental health score is:", score)
    return score
def categorize_mental_health(score):
    if score <= 20:
        return "Severely Depressed"
    elif score <= 30:
        return "Moderately severely Depressed"
    elif score <= 40:
        return "Moderately Depressed"
    elif score <= 50:
        return "Mildly Depressed"
    else:
        return "Not Depressed"
def main():
    st.title("Real-Time Mental Health Prediction")

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("Please click the button below, allow microphone access, and describe how you are feeling:")
        record_button = st.button("Record")

        if record_button:
            st.write("Recording...")
            audio = recognizer.listen(source)
            st.write("Recording finished!")
            try:
                transcribed_text = recognizer.recognize_google(audio)
                st.write("Transcribed:", transcribed_text)

                # Calculate mental health score
                score = calculate_mental_health_score(transcribed_text)
                mental_health_category = categorize_mental_health(score)

                st.write("Your mental health score is:", score)
                st.write("Mental Health Category:", mental_health_category)

            except sr.UnknownValueError:
                st.write("Could not understand audio")
            except sr.RequestError as e:
                st.write("Could not process audio:", e)

if __name__ == "__main__":
    main()