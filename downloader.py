import streamlit as st
import subprocess
import re
import zipfile
from datetime import datetime
from os import path, makedirs, remove, listdir

DOWNLOAD_DIR = "downloads"
YT_DLP_EXEC = "./yt-dlp"
AUDIO_FORMATS = ["mp3", "wav", "aac", "ogg", "vorbis"]
VIDEO_FORMATS = ["mp4", "webm"]
YOUTUBE_REGEX = r"https?://(www\.)?(youtube\.com|youtu\.be)/.+"

if not path.exists(DOWNLOAD_DIR):
    makedirs(DOWNLOAD_DIR)

def cleanup_downloads():
    for file in listdir(DOWNLOAD_DIR):
        try:
            remove(path.join(DOWNLOAD_DIR, file))
        except Exception as e:
            st.error(f"Error deleting {file}: {e}")
    st.session_state.downloaded_files = []
    st.session_state.zip_file = None

def run_command(commandline):
    output_box = st.empty()
    progress_bar = st.progress(0)
    try:
        process = subprocess.Popen(
            commandline,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            output_box.text(line.strip())
            match = re.search(r"(\d{1,3}\.\d)%", line)
            if match:
                percent = float(match.group(1))
                progress_bar.progress(min(int(percent), 100))
        process.wait()
        if process.returncode != 0:
            st.error("Download failed. Check the URL or command.")
            return False
        progress_bar.progress(100)
        st.success("✅ Download completed!")
        return True
    except Exception as e:
        st.error(f"Error running command: {e}")
        return False

def zip_playlist():
    zip_name = f"playlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = path.join(DOWNLOAD_DIR, zip_name)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in listdir(DOWNLOAD_DIR):
            full_path = path.join(DOWNLOAD_DIR, file)
            if path.isfile(full_path) and not file.endswith(".zip"):
                zipf.write(full_path, arcname=file)
    return zip_name

def list_downloaded_files():
    return [
        f for f in listdir(DOWNLOAD_DIR)
        if path.isfile(path.join(DOWNLOAD_DIR, f)) and not f.endswith(".zip")
    ]

def start_gui(config, url):
    if not url:
        st.warning("⚠️ No URL provided.")
        return False
    if not re.match(YOUTUBE_REGEX, url):
        st.error("Invalid or unsupported URL.")
        return False
    cleanup_downloads()
    cmd = [YT_DLP_EXEC, "-o", f"{DOWNLOAD_DIR}/%(title)s.%(ext)s"]
    if config["downloadtype"] == "Audio":
        audio_fmt = "vorbis" if config["audioformat"] in ["ogg", "vorbis"] else config["audioformat"]
        cmd += ["-x", "--audio-format", audio_fmt]
    else:
        cmd += ["-f", config["videoformat"]]
    if config.get("isplaylist"):
        cmd.append("--yes-playlist")
    cmd.append(url)
    if run_command(cmd):
        st.session_state.downloaded_files = list_downloaded_files()
        if config.get("isplaylist"):
            st.session_state.zip_file = zip_playlist()
        return True
    return False

def start_cli(raw_command):
    if not raw_command:
        st.warning("⚠️ No command provided.")
        return False
    if any(c in raw_command for c in ";|&"):
        st.error("Invalid command: disallowed characters detected.")
        return False
    cleanup_downloads()
    parts = raw_command.strip().split()
    if parts[0].lower() not in ["yt-dlp", "./yt-dlp"]:
        parts.insert(0, YT_DLP_EXEC)
    else:
        parts[0] = YT_DLP_EXEC
    if "-o" not in parts:
        parts.insert(1, "-o")
        parts.insert(2, f"{DOWNLOAD_DIR}/%(title)s.%(ext)s")
    if run_command(parts):
        st.session_state.downloaded_files = list_downloaded_files()
        return True
    return False

def show_download_buttons():
    if st.session_state.downloaded_files:
        st.subheader("📁 Downloaded files")
        for i, file in enumerate(st.session_state.downloaded_files):
            with open(path.join(DOWNLOAD_DIR, file), "rb") as f:
                st.download_button(
                    f"⬇️ Download {file}",
                    f,
                    file_name=file,
                    key=f"download_{i}"
                )
    if st.session_state.zip_file:
        zip_path = path.join(DOWNLOAD_DIR, st.session_state.zip_file)
        with open(zip_path, "rb") as f:
            st.download_button(
                "📦 Download playlist ZIP",
                f,
                file_name=st.session_state.zip_file,
                key="zip_download"
            )

