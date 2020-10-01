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

def view_gamelog():
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

    menu = ["Planet Earth", "Chat Room", "Settings"]
    choice = st.sidebar.selectbox("Navigation", menu)
    players = []
    username = ''
    session_state = SessionState.get(q=1, money=0, hp=100)

    # ========================== chat room ============================== #
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

    # ========================== settings ============================== #
    elif choice == "Settings":
        st.title("Hacker Zone")
        st.subheader("empty DB and start new game")
        if st.button('reset chatlog'):
            if st.button('really do it?'):
                empty_db()
                start_game()

    # ========================== gameplay ==============================#
    elif choice == 'Planet Earth':

        st.title("🌎 Welcome to Earth")
        st.text(f"------------ q{session_state.q} -------------")

        q = session_state.q

        if q == 1:
            st.subheader("Do you wish to run for president?")
            if st.button('Yes'):
                st.success('Congratulations, you have won the race!')
                st.text('Welcome, President.\n\nYou have recieved £250 from corporate lobbyists.')
                session_state.money = session_state.money + 250
                session_state.hp = session_state.hp - 1
                session_state.q = 2
                st.button('Next')

        if q == 2:
            st.subheader("What is your first policy agenda?")
            if st.button('💠 Green new deal'):
                st.success('Congratulations! The Bill Has Passed!')
                st.text('You take a deep breath of fresh air.\n\nThe FTSE100 remains stable.')
                session_state.money = session_state.money - 50
                session_state.hp = session_state.hp - 1
                session_state.q = 3
                st.button('Next')
            if st.button('💠 Open national reserves for oil exploration'):
                st.success('Your nation will be rich!')
                st.text('You have found a bountiful plateau of crude oil (Gain £20)')
                session_state.money = session_state.money + 20
                session_state.hp = session_state.hp - 1
                session_state.q = 3
                st.button('Next')
        
        if q == 3:
            st.error('WARNING!')
            st.subheader("You've started a trade war.")
            st.text('Your access to Chinese manufacturing is severly restricted.')
            session_state.q = 4
            st.button('Next')

    if st.sidebar.button('reset'):
        session_state.q = 1
        session_state.money = 0
        session_state.hp = 100
        
    st.sidebar.title(f"💰 Wealth: £{session_state.money}")
    st.sidebar.title(f"🌱 HP: {session_state.hp}")
    st.sidebar.text(f"q{session_state.q}")



if __name__ == '__main__':
    main()
