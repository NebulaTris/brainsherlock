import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="BrainSherlock",
    page_icon="🧠",
)

page_bg_img = """
<style>

div.stButton > button:first-child {
    width: 200px;
    height: 60px;
    padding: 0.6em 2em;
    border: none;
    outline: none;
    color: rgb(255, 255, 255);
    background: #1a1a1a;
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
    background: #1a1a1a;
    left: 0;
    top: 0;
    border-radius: 10px;
}


[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1613901282987-990c3918479f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80");
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
add_logo("https://github.com/NebulaTris/brainsherlock/blob/main/16915065502869741.jpg?raw=true")
    
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("BrainSherlock 🕵️")
st.sidebar.success("Select a page below.")

st.markdown("**Hey there, fellow human! Feeling a bit down in the dumps, or is the sunny side of life giving you the blues? Fear not, for our zany AI contraption is here to scrutinize your melancholy with all the whimsical wisdom it can muster!** 🤖🎩")
st.markdown("**Here at BrainSherlock, we've harnessed the power of cosmic text analysis, intergalactic behavioral pattern analysis, and quirky speech analysis to decipher the enigmatic depths of your emotions. Our funky algorithms will spin through your words, decode your behaviors, and even tap into the vibes of your voice, all in the name of mental exploration!**")
st.markdown("**So, whether you're pouring out your soul through text messages or just letting your emotions run wild, our AI buddy is ready to be your quirky therapist. Are you a wallflower with a secret passion for disco dancing? Do your emotions flip-flop like a trampoline artist? Or perhaps you've got a case of the 'monday blues' that won't quit? Our AI detectives are on the case!**")
st.markdown("**Remember, the key to mental well-being is often a mix of humor and genuine understanding. Let's embrace our quirkiness and embark on a whimsical journey to explore our emotions together!** 🌈🎢")
st.markdown("**Choose your adventure below, and let's get started!** 🚀")

col1, col2, col3 = st.columns(3)

with col1:
    btn = st.button("Text Analysis")
    if btn:
        switch_page("Text Analysis")

with col2:
    btn2 = st.button("Behavioural Pattern Analysis")
    if btn2:
        switch_page("Behavioural Pattern Analysis")

with col3:
    btn3 = st.button("Speech Analysis")
    if btn3:
        switch_page("Speech Analysis")
