from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai


load_dotenv() ## loading all the environment variables

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))


## Function to load Gemini Pro model and to get respone

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response



## Initialize application

st.set_page_config(page_title='Q&A ChatBot')
st.header('Q&A ChatBot Application')

## Initialize Session State for chat history if it doesnot exist


if 'chat_history' not in st.session_state:
    st.session_state ['chat_history'] = []


input = st.text_input('Input Message:',key = 'input')
submit = st.button('Submit')

if submit and input:
    response = get_gemini_response(input)

    ## Adding input and response to chat history
    st.session_state['chat_history'].append('You',input)
    st.subheader('Response')
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append('Response',chunk.text)


st.subheader('Chat History')

for job,text in st.session_state['chat_history']:
    st.write(f'{job}:{text}')