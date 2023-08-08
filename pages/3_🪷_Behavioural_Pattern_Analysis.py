import streamlit as st
import time

page_bg_img = """
<style>

div.stButton > button:first-child {
    all: unset;
    width: 120px;
    height: 30px;
    font-size: 16px;
    background: transparent;
    border: none;
    position: relative;
    color: #f0f0f0;
    cursor: pointer;
    z-index: 1;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;

}
div.stButton > button:before, div.stButton > button:after {
    content: '';
    position: absolute;
    bottom: 0;
    right: 0;
    z-index: -99999;
    transition: all .4s;
}

div.stButton > button:before {
    transform: translate(0%, 0%);
    width: 100%;
    height: 100%;
    background: #0f001a;
    border-radius: 10px;
}
div.stButton > button:after {
  transform: translate(10px, 10px);
  width: 35px;
  height: 35px;
  background: #ffffff15;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border-radius: 50px;
}

div.stButton > button:hover::before {
    transform: translate(5%, 20%);
    width: 110%;
    height: 110%;
}


div.stButton > button:hover::after {
    border-radius: 10px;
    transform: translate(0, 0);
    width: 100%;
    height: 100%;
}

div.stButton > button:active::after {
    transition: 0s;
    transform: translate(0, 5%);
}




[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1630873292791-66937fdabdb8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1887&q=80");
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
st.title("Behavioural Pattern Analysis 🪷")
st.sidebar.success("Behavioural Pattern Analysis has been selected")

st.write("This behaviour pattern gives us a score on the basis of the quiz that is present below.")
st.write("The score is calculated on the basis of the answers given by the user.")


st.markdown(
    """<style>
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)

with st.form("my_form"):
    output = 0
    res = st.radio(
        "**1. Do you often have feelings of sadness, hopelessness, or irritability that interfere with how you think and experience everyday activities such as sleeping, eating, and managing your daily tasks?**",
        ('Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree') , horizontal=True)
    
    if res == 'Strongly Agree':
        output += 1.0
    elif res == 'Agree':
        output += 0.8
    elif res == 'Neutral':
        output += 0.6
    elif res == 'Disagree':
        output += 0.4
    else:
        output += 0.2
    
    res1 = st.radio(
        "**2. Has medication and traditional therapy helped alleviate your symptoms in the past?**",
        ('Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree') , horizontal=True)
    
    if res1 == 'Strongly Agree':
        output += 1.0
    elif res1 == 'Agree':
        output += 0.8
    elif res1 == 'Neutral':
        output += 0.6
    elif res1 == 'Disagree':
        output += 0.4
    else:
        output += 0.2
     
    res2 = st.radio(
        "**3. Has your appetite changed from what it used to be, either eating a lot less or a lot more than usual? Have you recently lost or gained weight without trying to do so?**",
        ('Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree') , horizontal=True)
    
    if res2 == 'Strongly Agree':
        output += 1.0
    elif res2 == 'Agree':
        output += 0.8
    elif res2 == 'Neutral':
        output += 0.6
    elif res2 == 'Disagree':
        output += 0.4
    else:
        output += 0.2
    
    res3 = st.radio(
        "**4. Do you have thoughts of suicide?**",
        ('Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree') , horizontal=True)
    
    if res3 == 'Strongly Agree':
        output += 1.0
    elif res3 == 'Agree':
        output += 0.8
    elif res3 == 'Neutral':
        output += 0.6
    elif res3 == 'Disagree':
        output += 0.4
    else:
        output += 0.2 
    st.write("*If you are having thoughts of suicide and are thinking of engaging in any unsafe behaviors, please seek immediate help*")
    
    res4 = st.radio(
        "**5. Are you having difficulty concentrating or making decisions?**",
        ('Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree') , horizontal=True)
    
    if res4 == 'Strongly Agree':
        output += 1.0
    elif res4 == 'Agree':
        output += 0.8
    elif res4 == 'Neutral':
        output += 0.6
    elif res4 == 'Disagree':
        output += 0.4
    else:
        output += 0.2 
    
    res5 = st.radio(
        "**6. Is your mood or behavior affecting relationships with your family and friends?**",
        ('Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree') , horizontal=True)
    
    if res5 == 'Strongly Agree':
        output += 1.0
    elif res5 == 'Agree':
        output += 0.8
    elif res5 == 'Neutral':
        output += 0.6
    elif res5 == 'Disagree':
        output += 0.4
    else:
        output += 0.2
    
    res6 = st.radio(
        "**Have you lost interest in many activities you used to enjoy?**",
        ('Strongly Agree', 'Agree', 'Neutral', 'Disagree', 'Strongly Disagree') , horizontal=True)
    
    if res6 == 'Strongly Agree':
        output += 1.0
    elif res6 == 'Agree':
        output += 0.8
    elif res6 == 'Neutral':
        output += 0.6
    elif res6 == 'Disagree':
        output += 0.4
    else:
        output += 0.2
    
    def analyse():
        msg = st.toast('Gathering data...')
        time.sleep(1)
        msg.toast('Analyzing...')
        time.sleep(1)
        msg.toast('Ready!')
    
    if st.form_submit_button('Submit'):
        analyse()
        result = output
        if result <= 1.4:
            st.subheader("You are not depressed.")
            time.sleep(1)
            st.balloons()
        elif result > 1.5 and result <= 2.8:
            st.subheader("You are mildly depressed.")
            time.sleep(1)
            st.snow()
        elif result > 2.9 and result <= 4.2:
            st.subheader("You are moderately depressed.")
            time.sleep(1)
            st.snow()
        elif result > 4.3 and result <= 5.6:
            st.subheader("You are moderately severe depressed.")
            time.sleep(1)
            st.snow()
        else:
            st.subheader("You are severely depressed.")
            st.warning('Please seek immediate help', icon="⚠️")
