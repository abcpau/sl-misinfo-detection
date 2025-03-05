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

claim_placeholder = st.empty()
premise_placeholder = st.empty()

col1,col2 = st.columns([1,2])


#------------------

def display_pred():
    st.session_state.pred = predict(st.session_state.claim, st.session_state.premise)

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
    col2.markdown(f"<h2 style='padding-top: 0px; color:red'> <em>{st.session_state.pred.capitalize()}</em> </h2>", unsafe_allow_html=True)