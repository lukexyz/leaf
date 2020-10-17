import streamlit as st
import codecs
import streamlit.components.v1 as stc 


def main():
    """A calculator app with Streamlit components"""

    st.beta_set_page_config(
        page_title="Fx",               # String or None. Strings get appended with "• Streamlit". 
        page_icon="📼",                # String, anything supported by st.image, or None.
        layout="centered",             # Can be "centered" or "wide". In the future also "dashboard", etc.
        initial_sidebar_state="auto")  # Can be "auto", "expanded", "collapsed"

    # Using st.beta_columns
    col1, col2 = st.beta_columns(2)

    choice = "Simple"

    with col2:  # Need to run selections first!
        choice = st.radio("", ["Simple", "Advanced"])

    with col1:
        if choice == "Advanced":
            st.header("Advanced Calculator")

        elif choice == "Simple":
            st.header("Simple Calculator")





    
if __name__ == '__main__':
    main()
