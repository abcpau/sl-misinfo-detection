import streamlit as st
from backend import format_premise_hypothesis, generate_inference, parse_llama_explanation

#------------------

IP_ADDRESS = '10.147.36.147'
PORT = 11434
URL = f"http://{IP_ADDRESS}:{PORT}/api/chat"
HEADERS = {"Content-Type": "application/json"}

MODEL = "llama3.1:8b"
# MODEL = "deepseek-r1:8b" # Not yet supported

#------------------

def predict(h, p):
    formatted_input = format_premise_hypothesis(p, h)
    inference = generate_inference(url=URL, headers=HEADERS, model=MODEL, content=formatted_input)
    prediction, explanation = parse_llama_explanation(inference)
    return prediction, explanation

#------------------


if "claim" not in st.session_state:
    st.session_state.claim = ""

if "premise" not in st.session_state:
    st.session_state.premise = ""
    
if "pred" not in st.session_state:
    st.session_state.pred = ""

if "expl" not in st.session_state:
    st.session_state.expl = ""


#------------------


st.title("FAKE NEWS DETECTOR!")

claim_placeholder = st.empty()
premise_placeholder = st.empty()

col1,col2 = st.columns([1,2])

expl_placeholder = st.empty()


#------------------

def display_pred():
    pred, expl = predict(st.session_state.claim, st.session_state.premise)
    st.session_state.pred = pred
    st.session_state.expl = expl

#------------------

with st.form("my_form"):

    claim = st.text_area(
        "Input Claim",
        key="claim",
        placeholder="Enter the statement you want to verify here...",
    )

    premise = st.text_area(
        "Input Premise",
        key="premise",
        placeholder="Enter some facts to help us verify your claim here...",
    )

    submit = st.form_submit_button('Verify', on_click=display_pred)

if submit:
    claim_placeholder.markdown(f"Claim: {st.session_state.claim}")
    premise_placeholder.markdown(f"Premise: {st.session_state.premise}")
    col1.markdown("<h2 style='padding-top: 0px;'>Verdict: </h2>", unsafe_allow_html=True)
    if st.session_state.pred == "fact":
        col2.markdown(f"<h2 style='padding-top: 0px; color:green'> <em>{st.session_state.pred.capitalize()}</em> </h2>", unsafe_allow_html=True)
    else:
        col2.markdown(f"<h2 style='padding-top: 0px; color:red'> <em>{st.session_state.pred.capitalize()}</em> </h2>", unsafe_allow_html=True)
    
    expl_placeholder.markdown(f"Basis: {st.session_state.expl}")