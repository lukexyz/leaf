import streamlit as st
import sqlite3
import numpy as np
import time
import SessionState

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

def create_gamelog():
    c.execute("""CREATE TABLE IF NOT EXISTS gamelog(
                    id INTEGER PRIMARY KEY, 
                    username TEXT, 
                    message TEXT,
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    add_gamelog('Admin', 'Welcome to the chatroom')                

def empty_db():
    c.execute('DROP TABLE IF EXISTS userstable')
    c.execute('DROP TABLE IF EXISTS gamelog')

def add_gamelog(username, message):
    c.execute('INSERT INTO gamelog(username, message) VALUES (?,?)', (username, message))
    conn.commit()

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def view_log():
    c.execute('SELECT * FROM gamelog ORDER BY Timestamp DESC LIMIT 10')
    data = c.fetchall()
    return data

    
@st.cache
def start_game():
    create_usertable()
    create_gamelog()

def main():
    """Boardgame App"""
    start_game()

    menu = ["Planet Earth", "Chapter 2", "Chapter 3", "Chat Room", "Settings"]
    choice = st.sidebar.selectbox("Navigation", menu)
    players = []
    username = ''


    if choice == "Chat Room":
        st.title("Chat Room")

        username = st.sidebar.text_input("User Name")
        st.text(f"hi {username}")

        if st.sidebar.checkbox("Start Playing!"):
            add_user(username)
            st.success(f"New User: {username}")
            message = st.text_input("Press enter to send")
            if st.button("Chat"):
                add_gamelog(username, message)
            for m in view_gamelog():
                st.text(f'{m[3][-8:]} \t{m[1]}: {m[2]}')


    elif choice == "Settings":
        st.title("Hacker Zone")
        st.subheader("empty DB and start new game")

        if st.button('reset'):
            if st.button('really do it?'):
                empty_db()
                start_game()


    elif choice == 'Planet Earth':

        session_state = SessionState.get(user_name='', money=0, favorite_color='black')
        st.text(session_state.user_name)
        session_state.user_name = 'Mary'
        st.text(session_state.favorite_color)
        money = session_state.money

        st.title("🌎 Welcome to Earth")

        st.sidebar.title(f"🏃‍♂️ HP: {100}")
        session_state.money = session_state.money + 250

        st.subheader("Do you wish to run for president?")
        if st.button('Yes'):
            session_state.user_name = 'Luke'
            st.text(session_state.user_name)
            st.text('Congratulations, you have won the race.\n\nWelcome Mr President.')
            st.text('You have recieved £250 from corporate lobbyists.')

        st.subheader("What is your first policy agenda?")
        if st.button('Green new deal'):
            st.text('You have sealed the deal. (Economy shrinks. Lose £50)')
            money -= 50
            st.text(money)
            st.sidebar.title(f"💰 Wealth: £{money}")
        if st.button('Open national reserves for oil exploration'):
            st.text('You have found a bountiful plateau of crude oil (Gain £20) ')
            money += 20
            st.balloons()
        st.text('You have sealed the deal. (Economy shrinks. Lose £50)')

        st.sidebar.title(f"💰 Wealth: £{money}")

if __name__ == '__main__':
    main()
