import os
import streamlit as st
from pdfminer.high_level import extract_text


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
    
