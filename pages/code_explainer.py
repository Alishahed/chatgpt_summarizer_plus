import openai
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st

max_token = 3000

with st.sidebar:
    st.subheader("This app describes codes in human language")
    github_url = st.text_input('Enter the GitHub URL to the code/script here')


if github_url:
    response_summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": st.secrets['chatgpt_queries']['github_exp_query1'] +
                                                github_url
                                            }
        ],
        max_tokens = max_token
        )

    st.write(response_summary.choices[0].message.content)