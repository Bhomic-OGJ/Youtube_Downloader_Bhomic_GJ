import streamlit as st
from pytubefix import YouTube
import os
from PIL import Image

def download_video(url, download_audio=False):
    try:
        yt = YouTube(url)
        
        if download_audio:
            stream = yt.streams.filter(only_audio=True).first()
            file_extension = ".mp3"
        else:
            stream = yt.streams.get_highest_resolution()
            file_extension = ".mp4"
        
        download_path = stream.download()
        new_file_path = download_path.replace(".mp4", file_extension) if download_audio else download_path
        
        if download_audio:
            os.rename(download_path, new_file_path)
        
        return new_file_path
    except Exception as e:
        return str(e)

# Streamlit App
st.title("YouTube Video/Audio Downloader")

url = st.text_input("Enter YouTube Video URL")
option = st.radio("Select Download Option", ("Video", "Audio"))

download_audio = option == "Audio"

if st.button("Download"):
    if url:
        file_path = download_video(url, download_audio)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Click here to download",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="audio/mp3" if download_audio else "video/mp4"
                )
            os.remove(file_path)  # Remove file after download
        else:
            st.error("Failed to download. Please check the URL and try again.")
    else:
        st.warning("Please enter a valid YouTube URL.")




ad_code = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2102345545169156"
     crossorigin="anonymous"></script>
"""

st.components.v1.html(ad_code, height=100)

# QR Code for Support
st.markdown("---")
st.subheader("☕ Support this app")

# buymeacoffee_url = "https://www.buymeacoffee.com/yourusername"  # Replace with your actual link
qr_path = "qr.jpeg"

image = Image.open(qr_path)
st.image(image, caption="Scan to Buy Me a Coffee", width=200)
# st.markdown(f"[Or click here to support]({buymeacoffee_url})")



