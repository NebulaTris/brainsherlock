import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_webrtc import webrtc_streamer
import av
import webbrowser
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
from streamlit_extras.switch_page_button import switch_page

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

st.title("Facial Analysis 👤")

st.sidebar.success("Facial Analysis has been selected")

model = load_model("model.h5")
label = np.load("label.npy")

holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils

if "run" not in st.session_state:
    st.session_state["run"] = ""

run = np.load("emotion.npy")[0]

try:
    emotion = np.load("emotion.npy")[0]
except:
    emotion = ""

    
class EmotionProcessor:
    def recv(self,frame):
        frm = frame.to_ndarray(format="bgr24")
        frm = cv2.flip(frm, 1)  
        res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
        
        lst = []
        if res.face_landmarks:
            for i in res.face_landmarks.landmark:
                lst.append(i.x - res.face_landmarks.landmark[1].x)
                lst.append(i.y - res.face_landmarks.landmark[1].y)
        
            if res.left_hand_landmarks:
                for i in res.left_hand_landmarks.landmark:
                    lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
            else:
                for i in range(42):
                    lst.append(0.0)
        
            if res.right_hand_landmarks:
                for i in res.right_hand_landmarks.landmark:
                    lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
            else:
                for i in range(42):
                    lst.append(0.0)
        
            lst = np.array(lst).reshape(1, -1)
        
            pred = label[np.argmax(model.predict(lst))]
            print(pred)
            cv2.putText(frm, pred, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            
            np.save("emotion.npy",np.array([pred]))
            
            emotion = pred
       
        drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_CONTOURS)
        drawing.draw_landmarks(frm, res.left_hand_landmarks, hands.HAND_CONNECTIONS) 
        drawing.draw_landmarks(frm, res.right_hand_landmarks, hands.HAND_CONNECTIONS)
    
        return av.VideoFrame.from_ndarray(frm, format="bgr24")
    
if st.session_state["run"] != "false":
    webrtc_streamer(key="key", desired_playing_state=True , video_processor_factory=EmotionProcessor)
btn = st.button("Check your mental state")

if btn:
    if not(emotion):
        st.warning("Please wait for your mental state to be detected")
        
    else:
        np.save("emotion.npy",np.array([""]))
        st.session_state["run"] = run
        st.write(emotion)

