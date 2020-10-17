import streamlit as st
import codecs
import streamlit.components.v1 as stc 

import numpy as np
import pandas as pd

@st.cache(persist=True) # persist cache on disk
def create_df(size):
    df = pd.DataFrame(np.random.randn(size[0], size[1]),
        columns=(f'col{i}' for i in range(size[1])))
    return df

def main():
    """A calculator app with Streamlit components"""

    st.beta_set_page_config(
        page_title="Fx",               # String or None. Strings get appended with "• Streamlit". 
        page_icon="📼",                # String, anything supported by st.image, or None.
        layout="centered",             # Can be "centered" or "wide". In the future also "dashboard", etc.
        initial_sidebar_state="auto")  # Can be "auto", "expanded", "collapsed"

    # ================== Using st.beta_columns ================== #
    col1, col2 = st.beta_columns([3, 1]) # first column 3x the size of second


    choice = "Simple"

    with col2:  # Need to run selections first!
        choice = st.radio("", ["Simple", "Advanced"])

    with col1:
        if choice == "Advanced":
            st.header("📠 Advanced Calculator")

        elif choice == "Simple":
            st.header("📺 Simple Calculator")
    
        st.subheader("random dataframe")

        # ================== Mutate data with st.table() ================== #

        df1 = create_df(size=(1,5))
        my_table = st.table(df1)

        if st.button('add rows'):
            df2 = pd.DataFrame(np.random.randn(3, 5),
                        columns=(f'col{i}' for i in range(5)))
            my_table.add_rows(df2)



    
if __name__ == '__main__':
    main()
