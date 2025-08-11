import streamlit as st
from firecrawl import FirecrawlApp 

st.title("BlogCast")

url = st.text_input("Enter the blog url :")

if st.button("Generate Podcast"):
    if url:
        try:
            app = FirecrawlApp(api_key = st.secrets["FIRECRAWL_API_KEY"])

            st.info("Scraping Blog Content...")
            
            scrape_result = app.scrape_url(url=url)

            st.subheader("Scraped Content (as Markdown):")
            st.markdown(scrape_result.markdown)

        except Exception as e:
            st.error(f"An error occured : {e}")

    else:
        st.error("Enter the URL First....")