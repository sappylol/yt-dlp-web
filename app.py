import streamlit as st
from config import load_config, save_config
from downloader import start_gui, start_cli, show_download_buttons, AUDIO_FORMATS, VIDEO_FORMATS
from os import system

system("chmod +x yt-dlp")

st.set_page_config(page_title="YT-DLP Web", page_icon="📥")
st.title("📥 YT-DLP Web")


if "downloaded_files" not in st.session_state:
    st.session_state.downloaded_files = []
if "zip_file" not in st.session_state:
    st.session_state.zip_file = None

config = load_config()
mode = st.radio("Select mode", ["GUI", "CLI"])

if mode == "GUI":
    with st.expander("Settings"):
        config["downloadtype"] = st.selectbox(
            "Download type", ["Video", "Audio"],
            index=0 if config["downloadtype"] == "Video" else 1
        )
        config["isplaylist"] = st.checkbox("Download as playlist", value=config["isplaylist"])
        config["audioformat"] = st.selectbox(
            "Audio format", AUDIO_FORMATS,
            index=AUDIO_FORMATS.index(config["audioformat"])
        )
        config["videoformat"] = st.selectbox(
            "Video format", VIDEO_FORMATS,
            index=VIDEO_FORMATS.index(config["videoformat"])
        )
        if st.button("Save settings"):
            save_config(config)

    url = st.text_input("🔗 Enter URL", placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if st.button("Start download"):
        start_gui(config, url)

else:
    st.subheader("yt-dlp command")
    command = st.text_input(
        "Command",
        placeholder="yt-dlp -x --audio-format mp3 https://youtu.be/dQw4w9WgXcQ"
    )
    if st.button("Execute command"):
        start_cli(command)

show_download_buttons()

