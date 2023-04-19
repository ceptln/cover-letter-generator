import streamlit as st
import openai
import io
import utils
import main
import re

# OpenAI setup
openai.api_key = utils.open_file('openai_api_key.txt')

st.set_page_config(
    page_title="CL Generator",
    page_icon="🤖",
    # layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/ceptln/cover-letter-generator',
        'Report a bug': "https://github.com/ceptln/cover-letter-generator",
        'About': "This app was built an deployed by Camille Goat Epitalon"
    }
)

st.sidebar.markdown(f"<h3 style='text-align: left;'>💻 Our work</h3>", unsafe_allow_html=True)
st.sidebar.info("GitHub Repository: <https://github.com/ceptln/cover-letter-generator>")
st.sidebar.markdown(f"<p></p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p></p>", unsafe_allow_html=True)
st.sidebar.markdown(f"<h3 style='text-align: left;'>📬 Contact</h3>", unsafe_allow_html=True)
markdown = """
camille.epitalon@polytechnique.edu
"""
st.sidebar.info(markdown)

title = 'Cover Letter Generator'
subtitle = "The smart tool for busy job seekers"
mission = "Get hired faster with the ultimate AI-powered cover letter generator. Our web app is designed to streamline your job application process, making it faster and easier for you to apply for your dream job 🚀"
steps = """
Here's how it works:\n
1. Upload your CV\n
2. Enter the job offer URL\n
3. Sit back and relax, your Cover Letter is being writen with ❤️\n
"""
# how_it_works = "Just follow the 2 steps below, sit back and relax while we take care of your cover letter 😎"
st.markdown(f"<h1 style='text-align: center;font-size:50px;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'><i>{subtitle}</i></h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: left;'></p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: justify;'>{mission}</p>", unsafe_allow_html=True)
# st.markdown(f"<p style='text-align: justify;'>{how_it_works}</p>", unsafe_allow_html=True)
st.text('')

task = "Upload your CV, copy paste the job offer URL and we do the rest!"
st.markdown(f"<h5 style='text-align: left;'>{task}</h5>", unsafe_allow_html=True)
cv = st.file_uploader('Your CV:', accept_multiple_files=False,
                                   type=["pdf"], label_visibility="visible")
# st.text('')
# st.markdown(f"<h5 style='text-align: left;'>Upload your CV</h5>", unsafe_allow_html=True)
url = st.text_input('The job offer URL:', placeholder='https://www.welcometothejungle.com/fr/companies/apple/jobs/data-scientist', label_visibility="visible")

st.text('')
cols = st.columns(3)
st.text('')
run = cols[1].button('Generate Cover Letter', key=None, help=None, on_click=None, args=None, kwargs=None, disabled=False)

if run:
    if_issue_persists = "If the issue persists, please reach out to me."
    cv_extract_failed = "⚠️ Sorry buddy, but we were not able to extract any text from your CV."
    cv_upload_new = "Check the quality of your PDF file and retry."
    cv_isnot_cv = "⚠️ Sorry buddy, but the PDF file you uploaded does not look like a CV."
    url_not_found = "⚠️ Sorry but the URL you provided does not exist."
    url_not_found_https = f"⚠️ Sorry but the URL you provided does not exist. Perhaps you meant https://{url}?"
    unscrapable_websites = ['indeed', 'linkedin', 'jobteaser', 'notion']
    st.text('')
    if cv is None:
        st.markdown(f"<p style='text-align: center;'>Oupssss, you forgot to upload your CV 🤓</p>", unsafe_allow_html=True)   
    elif url is None or url == "":
        st.markdown(f"<p style='text-align: center;'>Oupssss, you forgot to enter the URL 🤓</p>", unsafe_allow_html=True)   
    elif url[0] != '"' and any(website in url for website in unscrapable_websites):
        pattern = '|'.join(unscrapable_websites)
        website = re.search(pattern, url).group()
        st.markdown(f"<p style='text-align: center;'>⚠️ Unfortunately, we were enable to scrap <i>{website.title()}</i> website because of firewalls on their side.</p>", unsafe_allow_html=True)           
        st.text('')
        st.text('')
        st.markdown(f"<p style='text-align: left;'><b>💡 We are working on an integration but as of now, you have two options here:</b></p>", unsafe_allow_html=True)
        st.markdown(f"1. Find the offer on another website, such as _WelcomeToTheJungle_ or the company website.")
        st.markdown('2.  If the issue persists, it means that the website is protected and cannot be scraped. To overcome the issue, you can just <b>copy/paste the job offer directly in the URL field, <u>between quotation marks "...".</u></b>.', unsafe_allow_html=True)                
    elif url[0] != '"' and not utils.is_valid_url(url):
        st.markdown(f"<p style='text-align: center;'>Oupssss, you did not enter a valid URL 🤓</p>", unsafe_allow_html=True)   
    else:
        with st.spinner("""We are creating your cover letter... The process usually takes **less than 2 minutes**."""):
            # Extracting text from CV
            try:
                cv = main.extract_text_from_pdf(cv)
                cv_ok = True
            except:
                st.markdown(f"<p style='text-align: center;'>{cv_extract_failed}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>{cv_upload_new} {if_issue_persists}</p>", unsafe_allow_html=True)
                cv_ok = False
            # Extracting text from the job offer website
            try:
                offer = main.extract_text_from_url(url)
                # Welcome to the Jungle shit
                offer.replace('Relevant advice, informative Q&As, inspirational portraits, newsworthy reports, videos, job openings, company profiles and more…', '')
                offer_ok = True
            except:
                if url[0] == '"':
                    offer = url[1:-1]
                    offer_ok = True
                else: 
                    offer_ok = False
                    st.markdown(f"<p style='text-align: center;'>Oupssss, you did not enter a valid URL 🤓</p>", unsafe_allow_html=True)   
                    st.text('')
                    st.markdown(f"<p style='text-align: left;'><b>💡 You have two options here:</b></p>", unsafe_allow_html=True)
                    st.markdown(f"1. Enter a new valid URL and re-start")
                    st.markdown('2.  If the issue persists, it means that the website is protected and cannot be scraped. To overcome the issue, you can just <b>copy/paste the job offer directly in the URL field, <u>between quotation marks "...".</u></b>.', unsafe_allow_html=True)                
            if cv_ok and offer_ok:
                st.markdown(f"<p style='text-align: left;font-family:courier;font-size:80%;color:grey;'><i>[1/5] checking that the PDF is a proper CV and that the URL refers a job offer...</i></p>", unsafe_allow_html=True)
                if not main.is_a_cv(cv) or len(cv) < 200:
                    if len(cv) < 10:
                        st.markdown(f"<p style='text-align: center;'>{cv_extract_failed}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: center;'>{cv_upload_new} {if_issue_persists}</p>", unsafe_allow_html=True)
                    else: 
                        st.markdown(f"<p style='text-align: center;'>{cv_isnot_cv}</p>", unsafe_allow_html=True)
                elif not main.is_a_job_offer(offer) or len(offer) < 200:
                    st.markdown(f"<p style='text-align: center;'>Sorry buddy, but the URL you provided does not look like job offer 🤯</p>", unsafe_allow_html=True)
                    st.text('')
                    st.markdown(f"<p style='text-align: left;'><b>💡 You have two options here:</b></p>", unsafe_allow_html=True)
                    st.markdown(f"1. Enter a new valid URL and re-start")
                    st.markdown('2.  If the issue persists, it means that the website is protected and cannot be scraped. To overcome the issue, you can just <b>copy/paste the job offer directly in the URL field, <u>between quotation marks "...".</u></b>.', unsafe_allow_html=True)                
                else:
                    st.markdown(f"<p style='text-align: left;font-family:courier;font-size:80%;color:grey;'><i>[2/5] parsing the CV to extract specific content...</i></p>", unsafe_allow_html=True)
                    cv_content = main.extract_content_from_CV(cv)
                    st.markdown(f"<p style='text-align: left;font-family:courier;font-size:80%;color:grey;'><i>[3/5] parsing the job offer to extract specific content...</i></p>", unsafe_allow_html=True)
                    offer_content = main.extract_content_from_offer(offer)
                    prompt_filling_dict = main.create_prompt_filling_dict(cv_content, offer_content)
                    st.markdown(f"<p style='text-align: left;font-family:courier;font-size:80%;color:grey;'><i>[4/5] creating the different cover letter blocks...</i></p>", unsafe_allow_html=True)
                    cl_blocks = main.create_cover_letter_blocks(prompt_filling_dict)
                    st.markdown(f"<p style='text-align: left;font-family:courier;font-size:80%;color:grey;'><i>[5/5] creating the word document...</i></p>", unsafe_allow_html=True)
                    document, document_name = main.create_cover_letter(cl_blocks)
                    bio = io.BytesIO()
                    document.save(bio)
                    if document:
                        st.text('')
                        st.text('')
                        st.markdown(f"<h3 style='text-align: center;'>Your Cover Letter is ready 🎁</h3>", unsafe_allow_html=True)
                        st.text('')
                        cols = st.columns(3)
                        cols[1].download_button(
                            label="Download your Cover Letter",
                            data=bio.getvalue(),
                            file_name=f"{document_name}.docx",
                            mime="docx")