import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

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
background-image: url("https://images.unsplash.com/photo-1642957097388-ed683dade3aa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=870&q=80");
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
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
add_logo("https://github.com/NebulaTris/brainsherlock/blob/main/16915065502869741.jpg?raw=true")

st.title("Text Analysis ✍🏼")
st.sidebar.success("Text Analysis has been selected")

st.write("This is a text analysis tool that can be used to analyze the sentiment of a text. It can also be used to classify the text into one of the following categories: Depressed, Non-Depressed and Suicidal.")
# List of questions
questions = [
    "How would you describe your experience at your workplace/college/school in the past few days?",
    "How do you like to spend your leisure time? How do you feel after it?",
    "Life has its ups and downs. Although handling successes can be difficult, setbacks can affect mental health strongly. How do you manage your emotions after failures?",
    "Are there any improvements/decline in your salary/grades?",
    "Any recent unpleasant experience that you would like to share?",
    "In a broad sense, how would you describe the way your life is going on?"
]

answers = []
for i, question in enumerate(questions):
    st.markdown(f"Question {i+1}: {question}")
    answer = st.text_input(f"Answer {i+1}:", key=f"answer_{i}")
    answers.append(answer)

# Display user answers
st.write("Your answers:")
for i, answer in enumerate(answers):
    st.write(f"Answer {i+1}: {answer}")
    
# Add the "Submit" button
submit_button = st.button("Submit", key="submit_button")

if submit_button:
    st.write("Analyzing...")


# Load the dataset CSV file
def preprocess(file):
    data = pd.read_csv(file, delimiter=';', header=None, names=['text;emotion'])
    hos = []
    for i in range(len(data)):
        text_emotion = data['text;emotion'][i].split(';')
        text = ';'.join(text_emotion[:-1])  # Combine text parts separated by semicolons
        emotion = text_emotion[-1]  # Extract emotion
        if emotion in ['joy', 'love', 'surprise']:
            hos.append(1)  # happy is 1
        else:
            hos.append(0)  # sad is 0
    data['text'] = text  # Add 'text' column
    data['emotion'] = emotion  # Add 'emotion' column
    data['hos'] = hos
    return data
    except FileNotFoundError:
    st.error("File not found. Please provide the correct file path.")
    return None

train_data = preprocess(r"https://github.com/Jixiee/brainsherlock-jixiee/blob/main/Dataset(Text).csv")
print(train_data.head())
train = train_data.copy()

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

val_data = preprocess(r"https://github.com/Jixiee/brainsherlock-jixiee/blob/main/dataset.csv")
val = val_data.copy()
history = model.fit(train_data['text'],  # Use the 'text' column for training data
                    train_data['hos'],
                    epochs=40,
                    batch_size=512,
                    verbose=0)
# Use the model to make predictions
def postprocessor(preds):
    preds_range = preds.max() - preds.min()
    probab = []
    for i in preds:
        probab.append((i - preds.min()) * 100 / preds_range)
    return np.mean(probab)
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def encode_texts(texts, max_length):
    encoded = tokenizer(texts, padding='max_length', truncation=True, max_length=max_length, return_tensors='tf')
    return encoded

results = model.predict(np.array(answers))
score = postprocessor(results)

print('Your mental health score is:', score)
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

mental_health_category = categorize_mental_health(score)
st.write(f"Your mental health score is: {score}")
st.write(f"Mental Health Category: {mental_health_category}")
