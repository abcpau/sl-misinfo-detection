import streamlit as st
import time
from config import URL, HEADERS, MODEL
from backend import parse_llama_explanation, find_premise_via_webrag
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
    inference = generate_response(url=URL, headers=HEADERS, model=MODEL, params=WEB_RAG_PARAMS(h, p))
    print("INFERENCE:", inference)
    prediction, explanation = parse_llama_explanation(inference)
    print("PREDICTION:", prediction, explanation)
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

# Add initialization for last_date_time_used
if "last_date_time_used" not in st.session_state:
    st.session_state.last_date_time_used = ""


#------------------

def display_pred():
    st.session_state.submitted = True
    
    # Update last_date_time_used to current date and time
    st.session_state.last_date_time_used = time.strftime('%Y-%m-%d %H:%M:%S')
    status_placeholder = st.empty()
    current_date_time = st.session_state.last_date_time_used
    status_placeholder.markdown(f'# {current_date_time} | Initializing model...', unsafe_allow_html=True)
    time.sleep(5)
    current_date_time = time.strftime('%Y-%m-%d %H:%M:%S')
    status_placeholder.markdown(f'# {current_date_time} | Inferencing...', unsafe_allow_html=True)
    
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