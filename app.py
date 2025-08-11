import streamlit as st

st.title("BlogCast")

url = st.text_input("Enter the blog url :")

if st.button("Generate Podcast"):
    if url:
        st.write("Url received")
        st.info("Processing starts")

    else:
        st.error("Incorrect Url")