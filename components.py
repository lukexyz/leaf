import streamlit as st
import codecs
import streamlit.components.v1 as stc 

def main():
    """A calculator app with Streamlit components"""

    # Using st.beta_columns
    col1, col2 = st.beta_columns(2)

    choice = st.radio("Calculator Type", ["Simple", "Advanced"])


    if choice == "Advanced":
        st.header("Advanced Calculator")

    elif choice == "Simple":
        st.header("Simple Calculator")
    
if __name__ == '__main__':
    main()
