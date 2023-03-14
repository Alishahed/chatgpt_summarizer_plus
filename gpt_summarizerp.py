import os
import openai
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
from app_util import save_uploadedfile,delete_file
import uuid



#print(os.environ)
#load_dotenv()
max_token = 3000
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
    txt_file_name = str(uuid.uuid4())+".txt"
    file_details = {"FileName":pdf_file.name,"FileType":pdf_file.type}
    save_uploadedfile(pdf_file)
    bucket_name = client.bucket("summarization_chatgpt")
    object_name_in_gcs_bucket = bucket_name.blob(txt_file_name)
    object_name_in_gcs_bucket.upload_from_filename(f'tempDir/tempfile.txt')

    #object_name_in_gcs_bucket = bucket_name.blob(pdf_file.name)
    #object_name_in_gcs_bucket.upload_from_filename(f'tempDir/{pdf_file.name}')
    auth_url = f'https://storage.cloud.google.com/summarization_chatgpt/{txt_file_name}'
    input_string = object_name_in_gcs_bucket.download_as_text()
    input_string_cut = input_string[:max_token]
    delete_file(f'tempDir/tempfile.txt')
    delete_file(f'tempDir/{pdf_file.name}')
else:
    auth_url = article_url
    #pass

if auth_url:
    response_summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "user", "content": st.secrets['chatgpt_queries']['summarizer_query1'] +
                                            input_string_cut +'\n'+
                                            st.secrets['chatgpt_queries']['summarizer_query2'] +
                                            st.secrets['chatgpt_queries']['summarizer_query3'] +
                                            st.secrets['chatgpt_queries']['summarizer_query4']
                                            }
    ],
    max_tokens = max_token
    )

    st.write(response_summary.choices[0].message.content)
