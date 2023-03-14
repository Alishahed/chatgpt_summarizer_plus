import os
import streamlit as st
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup
from bs4.element import Comment


def delete_file(saved_file):
    if os.path.exists(saved_file):
        os.remove(saved_file)

def pdf_to_text(uploadedfile):
    output_txt = extract_text(os.path.join("tempDir",uploadedfile.name),"r")
    return output_txt

def save_uploadedfile(uploadedfile):
    with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    text_string = pdf_to_text(uploadedfile)
    with open(os.path.join("tempDir","tempfile.txt"),"w") as f:
        f.write(text_string)
        f.close()
    return st.success("Uploading and processing File:{}".format(uploadedfile.name))
    
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)
