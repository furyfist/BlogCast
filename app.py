import streamlit as st
import google.generativeai as genai
from firecrawl import FirecrawlApp

# Configure the Gemini API client
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Main App Interface 
st.title("Blog Cast : Blog to Podcast Converter")

url = st.text_input("Enter Blog URL:")

if st.button("Generate Podcast"):
    if url:
        # Create a placeholder for status messages
        status_message = st.empty()
        
        try:
            # SCRAPE CONTENT with Firecrawl
            status_message.info("1/3: Scraping blog content...  scraping:")
            app = FirecrawlApp(api_key=st.secrets["FIRECRAWL_API_KEY"])
            scrape_result = app.scrape_url(url=url)
            scraped_text = scrape_result.markdown

            # GENERATE SCRIPT with Gemini
            status_message.info("2/3: Generating podcast script... ")
            
            # prompt for Gemini
            prompt = f"""
            You are an expert podcast host. Your task is to take the following blog post content and convert it into an engaging and conversational podcast script.

            Follow these instructions:
            1.  Start with a catchy introduction that hooks the listener.
            2.  Clearly state the main topic of the blog post.
            3.  Summarize the key points in a logical order.
            4.  Use a friendly, conversational tone, as if you are talking directly to a person. Avoid jargon where possible.
            5.  End with a concluding thought or a question for the listener.
            6.  The entire script should be concise and well-structured.

            Here is the blog post content:
            ---
            {scraped_text}
            ---
            """

            # Initialize the Gemini model and generate the content
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            # DISPLAY RESULTS
            status_message.success("3/3: All done! ✨")
            
            st.subheader("Generated Podcast Script:")
            st.markdown(response.text)

        except Exception as e:
            status_message.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a URL first.")