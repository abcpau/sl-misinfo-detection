import streamlit as st
import config
from backend import parse_llama_explanation#, find_premise_via_webrag
from backend import WEB_RAG_PARAMS, INFER_PARAMS, generate_response

def load_css(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
load_css("styles.css")

#------------------
# def find_premise_via_sentence_similarity():
#     top_results = [("Premise 1", 0.7), ("Premise 2", 0.5),]
#     prem = top_results[0][0]
#     prem_similarity = top_results[0][1]
#     return top_results, prem, prem_similarity

# def find_premise_via_webcrawl():
#     websearch = [{"title": "Title 1",
#                  "href": "https://verafiles.org/",
#                  "body": "Body 1",
#                  "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/VeraFiles_logo.svg"},
#                  {"title": "Title 2",
#                  "href": "https://verafiles.org/",
#                  "body": "Body 2",
#                  "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/VeraFiles_logo.svg"}]
#     return websearch, "<>", "This is the PREMISE"

def find_premise_via_webrag():
    websearch = [{"title": "Title 1",
                 "href": "https://verafiles.org/",
                 "body": "Body 1",
                 "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/VeraFiles_logo.svg"},
                 {"title": "Title 2",
                 "href": "https://verafiles.org/",
                 "body": "Body 2",
                 "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/VeraFiles_logo.svg"}]
    return websearch, "https://verafiles.org/"

def predict(h, p):
    #--------------
    return "False", "This is the EXPLANATION"
    #--------------
    formatted_input = format_premise_hypothesis(p, h)
    inference = generate_response(url=URL, headers=HEADERS, model=MODEL, content=WEB_RAG_PARAMS(h, p))
    inference = generate_response(url=URL, headers=HEADERS, model=MODEL, params=INFER_PARAMS(h, p))
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
input_placeholder = st.empty()

claim_placeholder = st.empty()

st.markdown('<div class="center-box">', unsafe_allow_html=True)
pred_placeholder = st.empty()
st.markdown('</div>', unsafe_allow_html=True)

expl_placeholder = st.empty()

division_placeholder = st.empty()

top_prems_placeholder = st.empty()
websearch_placeholder = st.empty()
premise_placeholder = st.empty()

#------------------

def display_pred():
    
    # prem_link, websearch = find_premise_via_webrag(st.session_state.claim, url_filters=[])
    websearch, prem_link = find_premise_via_webrag()            #placeholder, to remove
    st.session_state.websearch = websearch
    st.session_state.premise = prem_link

    pred, expl = predict(st.session_state.claim, prem_link)
    st.session_state.pred = pred
    st.session_state.expl = expl

#------------------

with input_placeholder.container():
    with st.form("my_form"):

        claim = st.text_area(
            "Input Claim",
            key="claim",
            placeholder="Enter the statement you want to verify here...",
        )

        submit = st.form_submit_button('Verify', on_click=display_pred)


if submit:
    input_placeholder.empty()

    claim_placeholder.markdown(f"<div class='text-box'>Claim: {st.session_state.claim}</div>", unsafe_allow_html=True)

    verdict_color = "green" if st.session_state.pred == "fact" else "red"
    pred_placeholder.markdown(
        f"""
        <div class="verdict-box-false">
        <h2 style='padding: 5px;'>Verdict: &nbsp;
            <span style='color:{verdict_color};'><em>{st.session_state.pred.capitalize()}</em></span>
        </h2>
        </div
        """,
        unsafe_allow_html=True
        )

    expl_placeholder.markdown(f"Basis: {st.session_state.expl}")

    division_placeholder.markdown('---')

    with websearch_placeholder.container():
        st.markdown(f"<p style='margin: 0px;'>Websearch results:</p>", unsafe_allow_html=True)
        for result in st.session_state.websearch:
            st.markdown(
                f"""
                <div class="websearch-result">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <img src="{result['logo_url']}" width="30px">
                        <strong><a href="{result['href']}" target="_blank">{result['title']}</a></strong>
                    </div>
                    <p>{result['body']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    premise_placeholder.markdown(f"Premise taken from: {st.session_state.premise}")

    # col1.markdown("<h2 style='padding-top: 5px;'>Verdict: </h2>", unsafe_allow_html=True)
    # if st.session_state.pred == "fact":
    #     col2.markdown(f"<h2 style='padding-top: 5px; color:green'> <em>{st.session_state.pred.capitalize()}</em> </h2>", unsafe_allow_html=True)
    # else:
    #     col2.markdown(f"<h2 style='padding-top: 5px; color:red'> <em>{st.session_state.pred.capitalize()}</em> </h2>", unsafe_allow_html=True)