import streamlit as st


#------------------
def predict(h, p):
    prediction = 'fact'
    # prediction = 'false'
    # st.write(h, p)
    return prediction
#------------------


if "claim" not in st.session_state:
    st.session_state.claim = ""

if "premise" not in st.session_state:
    st.session_state.premise = ""
    
if "pred" not in st.session_state:
    st.session_state.pred = ""


#------------------


st.title("FAKE NEWS DETECTOR!")

col1,col2 = st.columns([1,2])


#------------------

def display_pred():
    st.session_state.pred = predict(st.session_state.claim, st.session_state.premise)

#------------------

with st.form("my_form"):

    claim = st.text_area(
        "Claim",
        key="claim",
        placeholder="Enter the statement you want to verify here...",
    )

    premise = st.text_area(
        "Premise",
        key="premise",
        placeholder="Enter some facts to help us verify your claim here...",
    )

    submit = st.form_submit_button('Verify', on_click=display_pred)

if submit:
    col1.header('Verdict:')
    col2.header(f"*{st.session_state.pred.capitalize()}*")