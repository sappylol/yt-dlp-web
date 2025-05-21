
import streamlit as st
from os import listdir, path

DOWNLOAD_DIR = "downloads"

SUPPORTED_FORMATS = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".vorbis": "audio/ogg",
    ".mp4": "video/mp4",
    ".webm": "video/webm"
}

VALID_EXTENSIONS = tuple(SUPPORTED_FORMATS.keys())

def offer_downloads():
    files = [f for f in listdir(DOWNLOAD_DIR) if f.endswith(VALID_EXTENSIONS)]
    files.sort(key=lambda x: path.getmtime(path.join(DOWNLOAD_DIR, x)), reverse=True)

    if files:
        for file in files:
            full_path = path.join(DOWNLOAD_DIR, file)
            ext = path.splitext(file)[1].lower()
            mime = SUPPORTED_FORMATS.get(ext, "application/octet-stream")
            with open(full_path, "rb") as f:
                st.download_button(
                    label=f"📥 Download {file}",
                    data=f,
                    file_name=file,
                    mime=mime
                )
    else:
        st.warning("No media file found to offer for download.")
