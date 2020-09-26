import streamlit as st

def main():
    """Boardgame App"""

    st.title("Game Room")

    menu = ["Home", "Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)


    if choice == "Home":
        st.subheader("Home")
    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        if st.button("Start Playing"):
            st.success(f"New User:{username}")
    elif choice == "SignUp":
        st.subheader("Create New Account")


if __name__ == '__main__':
    main()
