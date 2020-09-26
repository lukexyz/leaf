import streamlit as st
import sqlite3 

# DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()

#@st.cache
def create_usertable():
    c.execute("""CREATE TABLE IF NOT EXISTS userstable (
                    username TEXT, id INTEGER PRIMARY KEY)""")

def add_user(username):
    c.execute('INSERT INTO userstable (username) VALUES (?)', [username])
    conn.commit()

def create_chatlog():
    c.execute("""CREATE TABLE IF NOT EXISTS chatlog(
                    id INTEGER PRIMARY KEY, 
                    username TEXT, 
                    message TEXT,
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    add_chat('Admin', 'Welcome to the chatroom')                

def empty_db():
    c.execute('DROP TABLE IF EXISTS userstable')
    c.execute('DROP TABLE IF EXISTS chatlog')

def add_chat(username, message):
    c.execute('INSERT INTO chatlog(username, message) VALUES (?,?)', (username, message))
    conn.commit()

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def view_chat():
    c.execute('SELECT * FROM chatlog ORDER BY Timestamp DESC LIMIT 10')
    data = c.fetchall()
    return data

def start_game():
    create_usertable()
    create_chatlog()

def main():
    """Boardgame App"""

    st.title("Game Room")

    menu = ["Play Game", "Settings",]
    choice = st.sidebar.selectbox("Settings", menu)
    players = []
    username = ''

    if st.sidebar.button('Reset'):
        empty_db()
        start_game()

    if choice == "Play Game":
        
        username = st.sidebar.text_input("User Name")
        st.text(f"hi {username}")

        if st.sidebar.checkbox("Start Playing!"):
            add_user(username)
            st.success(f"New User: {username}")

            message = st.text_input("Press enter to send")

            if st.button("Chat"):
                add_chat(username, message)

            for m in view_chat():
                st.text(f'{m[3][-8:]} \t{m[1]}: {m[2]}')
                
    elif choice == "Settings":
        st.subheader("Change Settings here")

if __name__ == '__main__':
    main()
