import streamlit as st
from few_shot_prompting import FewShotPrompting


def main():
    st.title("LinkedIn Post Generator by Rajarshi")
    col1, col2, col3 = st.columns(3)
    file_system = FewShotPrompting()
    tags = file_system.get_tags()
    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    # with col2:
    #     selected_length = st.selectbox("Length", options=length_options)

    # with col3:
    #     selected_language = st.selectbox("Language", options=language_options)


if __name__ == "__main__":
    main()
