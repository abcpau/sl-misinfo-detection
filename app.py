import streamlit as st
import config
from backend import format_premise_hypothesis, generate_inference, parse_llama_explanation

#------------------
def find_premise_via_sentence_similarity():
    top_results = [("Premise 1", 0.7), ("Premise 2", 0.5),]
    prem = top_results[0][0]
    prem_similarity = top_results[0][1]
    return top_results, prem, prem_similarity

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

def find_premise_via_webcrawl():
    websearch = [{"title": "Title 1",
                 "href": "https://verafiles.org/",
                 "body": "Body 1",
                 "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/VeraFiles_logo.svg"},
                 {"title": "Title 2",
                 "href": "https://verafiles.org/",
                 "body": "Body 2",
                 "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b8/VeraFiles_logo.svg"}]
    return websearch, "<>", "This is the PREMISE"


def predict(h, p):
    #--------------
    return "False", "This is the EXPLANATION"
    #--------------
    formatted_input = format_premise_hypothesis(p, h)
    inference = generate_inference(url=URL, headers=HEADERS, model=MODEL, content=formatted_input)
    prediction, explanation = parse_llama_explanation(inference)
    return prediction, explanation

#------------------

if "claim" not in st.session_state:
    st.session_state.claim = ""

if "premise_finder" not in st.session_state:
    st.session_state.premise_finder = None

if "premise" not in st.session_state:
    st.session_state.premise = ""
    
if "pred" not in st.session_state:
    st.session_state.pred = ""

if "expl" not in st.session_state:
    st.session_state.expl = ""


#------------------


st.title("FAKE NEWS DETECTOR!")

claim_placeholder = st.empty()
top_prems_placeholder = st.empty()
websearch_placeholder = st.empty()
markdown_placeholder = st.empty()           # to remove
premise_placeholder = st.empty()

col1,col2 = st.columns([1,2])

expl_placeholder = st.empty()


#------------------

def display_pred():
    st.session_state.premise_finder_index = premise_finder_options.index(premise_finder)
    pf = st.session_state.premise_finder_index
    st.write(pf)

    if pf == 0:
        pred, expl = predict(st.session_state.claim, st.session_state.premise)
        st.session_state.pred = pred
        st.session_state.expl = expl


    elif pf == 1:
        top_prems, prem = find_premise_via_sentence_similarity()    #placeholder, to remove
        st.session_state.top_prems = top_prems 
        st.session_state.premise = prem

        pred, expl = predict(st.session_state.claim, prem)
        st.session_state.pred = pred
        st.session_state.expl = expl
    

    elif pf == 2:
        # websearch, prem_link = find_premise_via_webrag(st.session_state.claim, url=URL, headers=HEADERS, model=MODEL)
        websearch, prem_link = find_premise_via_webrag()            #placeholder, to remove
        st.session_state.websearch = websearch
        st.session_state.premise = prem_link

        pred, expl = predict(st.session_state.claim, prem_link)
        st.session_state.pred = pred
        st.session_state.expl = expl


    else:
        # websearch, markdown, prem = find_premise_via_webcrawl(st.session_state.claim, url=URL, headers=HEADERS, model=MODEL)
        websearch, markdown, prem = find_premise_via_webcrawl()     #placeholder, to remove
        st.session_state.websearch = websearch     
        st.session_state.markdown = markdown     
        st.session_state.premise = prem     

        pred, expl = predict(st.session_state.claim, prem)
        st.session_state.pred = pred
        st.session_state.expl = expl

#------------------

premise_finder_options = ["I have my own premise",
                        "Check your dataset",
                        "Refer to the Internet using WebRAG",
                        "Refer to the Internet using WebCrawl"]

premise_finder = st.radio(
        "Where will we get the premise?",
        premise_finder_options,
         key="premise_finder",
)


with st.form("my_form"):

    claim = st.text_area(
        "Input Claim",
        key="claim",
        placeholder="Enter the statement you want to verify here...",
    )


    if premise_finder == "I have my own premise":
        premise = st.text_area(
            "Input Premise",
            key="premise",
            placeholder="Enter some facts to help us verify your claim here...",
        )



    submit = st.form_submit_button('Verify', on_click=display_pred)


if submit:
    claim_placeholder.markdown(f"Claim: {st.session_state.claim}")


    if st.session_state.premise_finder_index == 0:
        premise_placeholder.markdown(f"Premise: {st.session_state.premise}")


    elif st.session_state.premise_finder_index == 1:
        with top_prems_placeholder.container():
            st.markdown(f"Top premises:\n")
            for prem in st.session_state.top_prems:
                st.markdown(f"{prem[0]}: {prem[1]*100}% similar\n")
        premise_placeholder.markdown(f"Premise: {st.session_state.premise}")


    elif st.session_state.premise_finder_index == 2:
        with websearch_placeholder.container():
            st.markdown(f"Websearch results:\n", unsafe_allow_html=True)
            for result in st.session_state.websearch:
                st.markdown(f"""<img src="{result['logo_url']}" width='30px'>""", unsafe_allow_html=True)
                st.markdown(f"{result['title']}\n")
                st.markdown(f"{result['href']}\n")
                st.markdown(f"{result['body']}\n")
        premise_placeholder.markdown(f"Premise taken from: {st.session_state.premise}")


    elif st.session_state.premise_finder_index == 3:
        with websearch_placeholder.container():
            st.markdown(f"Websearch results:\n", unsafe_allow_html=True)
            for result in st.session_state.websearch:
                st.markdown(f"""<img src="{result['logo_url']}" width='30px'>""", unsafe_allow_html=True)
                st.markdown(f"{result['title']}\n")
                st.markdown(f"{result['href']}\n")
                st.markdown(f"{result['body']}\n")
        markdown_placeholder.markdown(f"Markdown (temp, to remove):<br>{st.session_state.markdown}", unsafe_allow_html=True)
        premise_placeholder.markdown(f"Premise: {st.session_state.premise}")


    col1.markdown("<h2 style='padding-top: 0px;'>Verdict: </h2>", unsafe_allow_html=True)
    if st.session_state.pred == "fact":
        col2.markdown(f"<h2 style='padding-top: 0px; color:green'> <em>{st.session_state.pred.capitalize()}</em> </h2>", unsafe_allow_html=True)
    else:
        col2.markdown(f"<h2 style='padding-top: 0px; color:red'> <em>{st.session_state.pred.capitalize()}</em> </h2>", unsafe_allow_html=True)
    
    expl_placeholder.markdown(f"Basis: {st.session_state.expl}")