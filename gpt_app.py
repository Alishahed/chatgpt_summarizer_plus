import os
import openai
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
from app_util import save_uploadedfile

#print(os.environ)
#load_dotenv()

openai.api_key = st.secrets['open_ai_key']['OPENAI_API_KEY']
#openai.api_key_path = '/home/ali/Projects/chatgpt_teacher/chatgpt_api_test/.env'

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

with st.sidebar:
    st.title('Article Summarizer+')
    pdf_file = st.file_uploader("Upload .pdf", type=['pdf'])
    st.subheader("OR")
    article_url = st.text_input('Enter the Article URL here')
if pdf_file is not None:
    file_details = {"FileName":pdf_file.name,"FileType":pdf_file.type}
    save_uploadedfile(pdf_file)
    bucket_name = client.bucket("summarization_chatgpt")
    object_name_in_gcs_bucket = bucket_name.blob(pdf_file.name)
    object_name_in_gcs_bucket.upload_from_filename(f'tempDir/{pdf_file.name}')
    auth_url = f'https://storage.cloud.google.com/summarization_chatgpt/{pdf_file.name}'
else:
    auth_url = article_url

if auth_url:
    response_summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": st.secrets['chatgpt_queries']['summarizer_query1'] +
                                            auth_url+'\n'+
                                            st.secrets['chatgpt_queries']['summarizer_query2'] +
                                            st.secrets['chatgpt_queries']['summarizer_query3'] +
                                            st.secrets['chatgpt_queries']['summarizer_query4']}
    ]
    #     messages=[
    #             {"role": "user", "content": f"Can you summarize this document and its results in 3 paragraph:{auth_url}'\n"+
    #                                 f"What are the main results of this paper? Put it maximum 5 bullet.\n"+
    #                                 f"What keywords Do I need to understand for understanding this paper?\n"+
    #                                 f"Can you provide a tutorial to learn about each of the above keywords for a beginner? Please provide the link to the tutorials too.\n"}
    # ]
    )

    st.write(response_summary.choices[0].message.content)
