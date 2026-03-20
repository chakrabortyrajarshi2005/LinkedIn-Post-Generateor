import streamlit as st
from few_shot_prompting import FewShotPrompting
from post_generator import generate_post
import base64

st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="✍️",
    layout="centered"
)

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Bengali"]


def apply_theme(is_dark):
    if is_dark:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #0e1117;
                color: white;
            }
            div[data-baseweb="select"] > div {
                background-color: #262730;
                color: white;
            }
            textarea {
                background-color: #262730 !important;
                color: white !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: white;
                color: black;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        
def get_download_link(text):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="linkedin_post.txt">📥 Download as .txt</a>'


def main():
    if "theme" not in st.session_state:
       st.session_state.theme = False
       
    toggle = st.toggle("🌙 Dark Mode", value=st.session_state.theme)

    st.session_state.theme = toggle
    apply_theme(st.session_state.theme)

    st.markdown(
        "<h1 style='text-align:center;'>✍️ LinkedIn Post Generator</h1>",
        unsafe_allow_html=True
    )

    file_system = FewShotPrompting()
    tags = file_system.get_tags()

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_tag = st.selectbox("📌 Topic", options=tags, key="topic")

    with col2:
        selected_length = st.selectbox("📏 Length", options=length_options, key="length")

    with col3:
        selected_language = st.selectbox("🌐 Language", options=language_options, key="language")

    generate_clicked = st.button("🚀 Generate Post", use_container_width=True)

    if generate_clicked:
        with st.spinner("Generating..."):
            post = generate_post(selected_length, selected_language, selected_tag)

        st.markdown("### 📝 Preview")
        st.markdown(post)

        st.text_area("", value=post, height=200, key="output")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(
                f"""
                <button onclick="navigator.clipboard.writeText(`{post}`)" 
                style="width:100%;padding:10px;border-radius:8px;border:none;background:#4CAF50;color:white;">
                📋 Copy to Clipboard
                </button>
                """,
                unsafe_allow_html=True
            )

        with col_b:
            st.markdown(get_download_link(post), unsafe_allow_html=True)


if __name__ == "__main__":
    main()