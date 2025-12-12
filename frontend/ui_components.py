import streamlit as st
import base64

def get_img_as_base64(file_path):
    """Reads an image file and converts it to a Base64 string."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def apply_terminator_style(bg_image_path, icon_image_path):
    """Applies custom CSS for the Terminator theme."""
    bg_base64 = get_img_as_base64(bg_image_path)
    icon_base64 = get_img_as_base64(icon_image_path)
    bg_css = ""
    if bg_base64:
        bg_css = f"""
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bg_base64}");
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
        }}
        """

    icon_css = ""
    if icon_base64:
        icon_css = f"""
        div[data-testid="stChatInput"] textarea {{
            background-image: url("data:image/png;base64,{icon_base64}");
            background-size: 35px;
            background-position: right 60px center;
            background-repeat: no-repeat;
            padding-right: 50px !important;
        }}
        """

    common_css = """
    .stChatMessage {
        background-color: rgba(0, 0, 0, 0.8) !important;
        color: #ffffff !important;
        border-radius: 10px;
        border-left: 5px solid #ff2b2b;
    }
    h1, h2, h3, p, span, div {
        text-shadow: 1px 1px 2px #000000;
        color: #e0e0e0;
    }
    .stChatInputContainer {
        background-color: rgba(0, 0, 0, 0.0) !important;
    }
    """

    st.markdown(f"<style>{bg_css} {icon_css} {common_css}</style>", unsafe_allow_html=True)