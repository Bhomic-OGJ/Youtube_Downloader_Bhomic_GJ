import streamlit as st
from pytubefix import YouTube
import os

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
