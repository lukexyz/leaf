import streamlit as st
import sqlite3
import time, random
import SessionState
import numpy as np
import pandas as pd
import altair as alt

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

# ========================== scoreboard fns ========================== #
def create_scoreboard():
    c.execute("""CREATE TABLE IF NOT EXISTS scoreboard(
                    id INTEGER PRIMARY KEY, 
                    money FLOAT,
                    temp FLOAT,
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""") 
    add_score(123, 250, 1)

def add_score(user_id, money, temp):
    c.execute('INSERT INTO scoreboard(id, money, temp) VALUES (?,?,?)', (user_id, money, temp))
    conn.commit()

def view_score(user_id):
    c.execute(f'SELECT * FROM scoreboard WHERE id = {user_id} ORDER BY Timestamp DESC LIMIT 1')
    data = c.fetchall()
    return data
# ==================================================================== #

@st.cache
def start_game():
    create_usertable()
    create_gamelog()
    create_scoreboard()

def main():
    """Boardgame App"""
    start_game()

    menu = ["Planet Earth", "Chat Room", "Settings"]
    choice = st.sidebar.selectbox("Navigation", menu)
    players = []
    username = ''
    user_id = random.randint(0, 1e6)
    session_state = SessionState.get(user_id=user_id, q=1, money=0, hp=100, temp=1.0)

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

    # ========================== gameplay ============================== #
    elif choice == 'Planet Earth':

        st.title("🌎 Welcome to Earth")
        st.text(f'user id {session_state.user_id}')

        st.text(f"------------ q{session_state.q} -------------")
        q = session_state.q

        if q == 1:
            st.subheader("Do you wish to run for president?")
            if st.button('Yes'):
                st.success('Congratulations, you have won the race!')
                st.text('Welcome, President.\n\nYou have recieved £250 from corporate lobbyists.')
                session_state.money = session_state.money + 250
                session_state.hp = session_state.hp - 1
                session_state.temp = session_state.temp * 1.1
                session_state.q = 2
                add_score(session_state.user_id, session_state.money, session_state.temp)
                st.button('Next')

        if q == 2:
            st.subheader("What is your first policy agenda?")
            if st.button('💠 Green new deal'):
                st.success('Congratulations! The Bill Has Passed!')
                st.text('You take a deep breath of fresh air.\n\nThe FTSE100 remains stable.')
                session_state.money = session_state.money - 50
                session_state.hp = session_state.hp - 1
                session_state.temp = session_state.temp * 1.1
                session_state.q = 3
                st.button('Next')
            if st.button('💠 Open national reserves for oil exploration'):
                st.success('Your nation will be rich!')
                st.text('You have found a bountiful plateau of crude oil (Gain £20)')
                session_state.money = session_state.money + 20
                session_state.hp = session_state.hp - 1
                session_state.temp = session_state.temp * 1.1
                session_state.q = 3
                st.button('Next')
        
        if q == 3:
            st.error('WARNING!')
            st.subheader("The People's Repulic of China have started a trade war against you.")
            st.text('Your access to manufacturing is severly restricted.')
            session_state.temp = session_state.temp * 1.1
            session_state.q = 4
            st.button('Next')
        
        if q == 4:
            st.subheader("Q4")
            st.text('Subtext 4')
            session_state.temp = session_state.temp * 1.1
            session_state.q = 5
            st.button('Next')

        if q == 5:
            st.subheader("Q5")
            st.text('Subtext 5')
            session_state.temp = session_state.temp * 1.1
            session_state.q = 5
            st.button('Next')

    # ========================== score ============================== #
    st.text('\n')
    for m in view_score(session_state.user_id):
        st.text(f'{m}')

    # ========================== sidebar ============================== #
    if st.sidebar.button('reset'):
        session_state.q = 1
        session_state.money = 0
        session_state.hp = 100
        session_state.temp = 1.0
    
    st.sidebar.title(f"💰 £{session_state.money}")
    st.sidebar.title(f"🌍 {session_state.hp}")
    st.sidebar.title(f"🌡️ {session_state.temp:0.2f}°")

    #st.sidebar.markdown("---")
    df = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
    c = alt.Chart(df).mark_line().encode(
        x='a', y='b', size='c', color='c')

    st.sidebar.altair_chart(c, use_container_width=True)

if __name__ == '__main__':
    main()
