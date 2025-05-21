
import json
import streamlit as st
from os import path

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "downloadtype": "Video",
    "isplaylist": False,
    "audioformat": "mp3",
    "videoformat": "mp4"
}

def load_config():
    if path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Error loading config: {e}. Using default settings.")
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        st.success("Settings saved!")
    except Exception as e:
        st.error(f"Error saving config: {e}")
