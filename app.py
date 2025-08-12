import streamlit as st
import google.generativeai as genai
from firecrawl import FirecrawlApp
from elevenlabs.client import ElevenLabs

# Configure page settings and API clients
st.set_page_config(layout="wide")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elevenlabs_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])
firecrawl_app = FirecrawlApp(api_key=st.secrets["FIRECRAWL_API_KEY"])

# App interface
st.title("Blog Cast: Blog to Podcast Converter 🎙️")
url = st.text_input("Enter the URL of the blog post you want to convert:")

if st.button("Generate Podcast"):
    if url:
        status_message = st.empty()
        
        try:
            # Scrape content
            status_message.info("1/4: Scraping blog content... 🕸️")
            scrape_result = firecrawl_app.scrape_url(url=url)
            
            # Generate script with Gemini
            status_message.info("2/4: Generating podcast script... ✍️")
            prompt = f"""
            You are an expert podcast host. Your task is to take the following blog post content and convert it into an engaging and conversational podcast script.

            Follow these instructions:
            1.  Start with a catchy introduction.
            2.  Summarize the key points in a logical, conversational order.
            3.  Use a friendly tone and avoid jargon.
            4.  End with a concluding thought or a question for the listener.
            5.  Ensure the script is concise and well-structured.

            Here is the blog post content:
            ---
            {scrape_result.markdown}
            ---
            """
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            podcast_script = response.text
            
            # Generate audio with ElevenLabs
            status_message.info("3/4: Generating audio... 🎧")
            audio_generator = elevenlabs_client.text_to_speech.convert(
                text=podcast_script,
                voice_id="21m00Tcm4TlvDq8ikWAM",  
                model_id="eleven_multilingual_v2",  
                output_format="mp3_44100_128"  
            )

            # Collect audio chunks into bytes (fix for generator output)
            audio_bytes = b"".join(chunk for chunk in audio_generator)

            # Display final results
            status_message.success("4/4: Podcast ready! ✨")
            
            st.subheader("Listen to Your Podcast:")
            st.audio(audio_bytes, format='audio/mpeg')  # Fixed: Pass bytes instead of generator

            # download button
            st.download_button(
                label="Download Podcast (MP3) ",
                data=audio_bytes,
                file_name="podcast_episode.mp3",
                mime="audio/mpeg"
            )

            st.subheader("Generated Script:")
            st.markdown(podcast_script)

        except Exception as e:
            status_message.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a URL first.")