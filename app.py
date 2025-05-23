import streamlit as st
import time
from config import URL, HEADERS, OPEN_WEBUI_MODEL, OLLAMA_MODEL
from backend import parse_llama_explanation, find_premise_via_webrag, is_model_running
from backend import WEB_RAG_PARAMS, INFER_PARAMS, generate_response

# st.set_page_config(layout="wide")

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

# def find_premise_via_webrag():
#     websearch = [{"title": "Title 1",
#                  "href": "https://verafiles.org/",
#                  "body": "Body 1",
#                  "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/VeraFiles_logo.svg"},
#                  {"title": "Title 2",
#                  "href": "https://verafiles.org/",
#                  "body": "Body 2",
#                  "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/VeraFiles_logo.svg"}]
#     return websearch, "https://verafiles.org/"

def predict(h, p):
    #--------------
    # return "False", "This is the EXPLANATION"
    #--------------
    inference = generate_response(url=URL, headers=HEADERS, model=OPEN_WEBUI_MODEL, params=WEB_RAG_PARAMS(h, p))
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M')}] CLAIM: {h}")
    print(f"[{time.strftime('%Y-%m-%d %H:%M')}] PREMISE: {p}")
    print(f"[{time.strftime('%Y-%m-%d %H:%M')}] INFERENCE: {inference}\n")
    prediction, explanation = parse_llama_explanation(inference)
    return prediction, explanation

#------------------

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "claim" not in st.session_state:
    st.session_state.claim = ""

if "premise" not in st.session_state:
    st.session_state.premise = ""
    
if "pred" not in st.session_state:
    st.session_state.pred = ""

if "expl" not in st.session_state:
    st.session_state.expl = ""

if "websearch" not in st.session_state:
    st.session_state.websearch = []

#------------------

def overlay_html(text):
    return f"""
    <style>
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }}
    .overlay h1 {{
        color: black;
        font-size: 2em;
        text-align: center;
    }}
    </style>
    <div class="overlay">
        <h1>[{time.strftime('%Y-%m-%d %H:%M')}] {text}</h1>
    </div>
    """

def display_pred():
    st.session_state.submitted = True
    
    status_placeholder = st.empty()
    if not is_model_running(OLLAMA_MODEL):
        print(f"[{time.strftime('%Y-%m-%d %H:%M')}] Ollama model is not running. Initializing model.")
        status_placeholder.markdown(overlay_html('Initializing model...'), unsafe_allow_html=True)
        time.sleep(10)
    status_placeholder.markdown(overlay_html('Inferencing...'), unsafe_allow_html=True)
    
    prem_link, websearch = find_premise_via_webrag(st.session_state.claim)
    st.session_state.websearch = websearch
    st.session_state.premise = prem_link

    if prem_link != '':
        pred, expl = predict(st.session_state.claim, prem_link)
        st.session_state.pred = pred
        st.session_state.expl = expl
    
    status_placeholder.empty()


def reset_state():
    st.session_state.submitted = False
    st.rerun()

#------------------

logo_url = 'https://www.shutterstock.com/image-vector/cow-logo-farm-product-design-600nw-2506761705.jpg'

header = st.container()
with header:
    st.markdown(
                f"""
                <div class="header">
                    <div class="title-row">
                        <img src="{logo_url}" width="100px">
                        <h1 class="title" style="word-break: keep-all">PATUNAI</h1>
                    </div>
                    <p class="subtitle"> A Filipino Misinformation Detector </p>
                </div>
                """,
                unsafe_allow_html=True
            )


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



if not st.session_state.submitted:
    with input_placeholder.container():
        with st.form("my_form"):

            claim = st.text_area(
                "Input Claim",
                key="claim",
                placeholder="Enter the statement you want to verify here...",
            )

            submit = st.form_submit_button('Verify', on_click=display_pred)


else:
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

    expl_placeholder.markdown(f"Explanation: {st.session_state.expl}")

    division_placeholder.markdown('---')

    with websearch_placeholder.container():
        if st.session_state.websearch:
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
        else:
            st.markdown(f"<p style='margin: 0px;'>No suitable web searches found.</p>", unsafe_allow_html=True)
            
    premise_placeholder.markdown(f"Premise taken from: {st.session_state.premise}")

    st.markdown('---')


    refresh = st.button('Try another claim!')
    if refresh:
        reset_state()
    
# About this Project and Contact Information section (always visible)
with st.container():
    st.info(
        """
        ### About PATUNAI
        Pattern Analysis Tool for Unverified News using AI (PATUNAI) is a research project aimed at detecting misinformation in Filipino news and social media. It leverages advanced AI and web search to help users verify claims quickly and accurately. This tool is for educational and research purposes only.
        
        **Contact Information**  
        Project Lead: Paul Regonia, D.Sc.  
        Researchers and Developers: [Abcede, Pauline](mailto:mgabcede1@up.edu.ph) and [Salazar, Led](mailto:lrsalazar@up.edu.ph)
        """,
        icon="🔍"
    )