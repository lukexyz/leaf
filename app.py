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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER, 
                    money FLOAT,
                    temp FLOAT,
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""") 
    add_score(123, 250, 1)

def add_score(user_id, money, temp):
    c.execute('INSERT INTO scoreboard(user_id, money, temp) VALUES (?,?,?)', (user_id, money, temp))
    conn.commit()

def view_score(user_id, limit=1):
    c.execute(f'SELECT * FROM scoreboard WHERE user_id = {user_id} ORDER BY id DESC LIMIT {limit}')
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
    session_state = SessionState.get(user_id=user_id, q=1, money=50, hp=50, temp=50)

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
        st.text(f"------------ q{session_state.q} -------------")
        q = session_state.q
        
        if q == 1:
            add_score(session_state.user_id, session_state.money, session_state.temp)
            st.subheader("Do you wish to run for World President?")
            if st.button('Yes'):
                st.success('Congratulations, you have won the race!')
                st.text('Welcome to the Office.')
                session_state.money = session_state.money + 2
                session_state.hp = session_state.hp + 1
                session_state.temp = session_state.temp + 0
                session_state.q = 2
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)

        if q == 2:
            st.subheader("What is your first policy?")
            if st.button('💠 Green new deal'):
                st.success('Congratulations! The Bill Has Passed!')
                st.text('You take a deep breath of fresh air.')
                st.text('3 Economy points are removed from the global budget')
                session_state.money = session_state.money - 3
                session_state.hp = session_state.hp + 1
                session_state.temp = session_state.temp + 0
                session_state.q = 3
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
            if st.button('💠 Open national reserves for oil exploration'):
                st.success('Your friends will be rich!')
                st.text('You have found a bountiful plateau of crude oil. Gain 10 Economy points.')
                st.text('The global temperature rises by 0.1°.')
                session_state.money = session_state.money + 10
                session_state.hp = session_state.hp - 10
                session_state.temp = session_state.temp - 1
                session_state.q = 3
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
        
        if q == 3:
            st.error('📰 Breaking News: British businessman Stephen Fitzpatrick has launched a new flying vehicle!')
            st.text('Increase government subsidies for personal electric flights?')
            st.text('Support an global initiative for electric scooters?')
            st.subheader("What is you decision?")
            if st.button('💠 Glide into the future of air travel'):
                st.success('A shadowy figure enters the room')
                st.text('Stephen Fitzpatrick emerges, and personally shakes your hand.')
                st.text('"Thank you, World President. You will not regret this."')
                st.text('You have installed a helipad on top of your garage. Lose 1 Economy point.')
                session_state.money = session_state.money - 1
                session_state.hp = session_state.hp + 10
                session_state.temp = session_state.temp + 10
                session_state.q = 4
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
            if st.button('💠 Scoot around the red tape with two wheels'):
                st.text('“Get off the pavement!” say pedestrians. “Get out of the road!” say motorists')
                st.text('"Thank goodness for bike lanes" say scooter boys and girls')
                st.text("You gain 2 Equality points.")
                session_state.money = session_state.money + 5
                session_state.hp = session_state.hp + 10
                session_state.temp = session_state.temp + 5
                session_state.q = 4
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
        
        if q == 4:
            st.subheader("Your scientists have told you our reliance on meat and fish has massively increased the world's carbon footprint.")
            st.text('What will you do about it?')
            if st.button('💠 Increase research funding for plant based products'):
                st.success('Research is under way!')
                st.text('Is it Tofu Tuesday already?')
                st.text('The research is slower than expected. It will take some time to see the benefit. Gain £10')
                session_state.money = session_state.money + 10
                session_state.hp = session_state.hp + 10
                session_state.temp = session_state.temp + 15
                session_state.q = 5
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
            if st.button('💠 Ban eating meat and fish'):
                st.success('The great Meat and Fish prohibition of 2020 has begun.')
                st.text("Your scientists praise your bold action.\n\nBut you've made a lot of carnivourous enemies today and\ncreated a huge ilegal market for back alley smoked salmon.")
                st.text("Ecology gains 20 points.")
                session_state.money = session_state.money - 20
                session_state.hp = session_state.hp + 20
                session_state.temp = session_state.temp - 20
                session_state.q = 5
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
            if st.button('💠 Subsidise plant based food and increase taxes on meat and fish'):
                st.success('Cheap apples for everyone!')
                st.text("You've made a small impact on eating habits\n but your scientists tell you that won't be enough.")
                session_state.money = session_state.money - 10
                session_state.hp = session_state.hp + 10
                session_state.temp = session_state.temp + 10
                session_state.q = 5
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)

        if q == 5:
            st.warning("🏭 BREAKING: Carbon dioxide at Record Levels in the Atmosphere")
            st.text('Your scientists suggest capturing carbon and taking\nit out of the atmosphere could be a big help.')
            st.subheader('What will you do?')
            if st.button('💠 Plant lots of trees'):
                st.success('Shovels to the ready!')
                st.text("A popular measure that's good for carbon cutting and clean air")
                st.text('')
                session_state.money = session_state.money - 10
                session_state.hp = session_state.hp + 15
                session_state.temp = session_state.temp + 15
                session_state.q = 6
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
            if st.button('💠 Invest in carbon capture technology'):
                st.success('Tech to the rescue!')
                st.text("Your tech industry is excitedly getting to work.\nThis technology will take a long time to develop though.")
                session_state.money = session_state.money + 20
                session_state.hp = session_state.hp + 5
                session_state.temp = session_state.temp - 0
                session_state.q = 6
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
            if st.button('💠 Turn all that nasty carbon into diamonds!'):
                st.success('Diamonds are forever')
                st.text("But you might not be.")
                st.text("Your population is angry that you signed off on such a ridiculous plan.")
                st.text("Acquire new bling. Gain £40")
                session_state.money = session_state.money + 40
                session_state.hp = session_state.hp - 10
                session_state.temp = session_state.temp - 10
                session_state.q = 6
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
         
        if q == 6:
            st.subheader("You are invited to a international dinner with powerful elites.")
            st.text("Elon takes you aside and asks to partner on electric planes.") 
            st.text("A UN retiree says Plan Zero could go international.")
            st.subheader("Who do you exchange numbers with?")
            if st.button('💠 Ash we need to book a space for a cybertruck'):
                st.success('“It’s no hyperloop but the slide is still fun” says Elon')
                st.text('Ovo international travel uses a BFR')
                st.text('Spend £30, but save precious minutes.')
                session_state.money = session_state.money + 15
                session_state.hp = session_state.hp + 15
                session_state.temp = session_state.temp + 15
                session_state.q = 7
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
            if st.button('💠 Ban ki-moon is coming to town'):
                st.success('UN instigates the Bristol Accord')
                st.text("The wheels are turning but how long will it take….?")
                session_state.money = session_state.money + 10
                session_state.hp = session_state.hp + 10
                session_state.temp = session_state.temp + 10
                session_state.q = 7
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
        
        if q == 7:
            st.text("A report has highlighted that petrol cars are one of the worlds biggest poluters")
            st.subheader("Your people want action. How will you respond?")
            if st.button('💠 Make everyone switch to electric cars right now'):
                st.success('The big electric switch has started!')
                st.text('Polution from petrol goes down dramatically, but the environment takes a hit\nfrom having to build so many new electric cars so quickly. ')
                st.text('')
                session_state.money = session_state.money - 10
                session_state.hp = session_state.hp - 15
                session_state.temp = session_state.temp - 30
                session_state.q = 8
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
            if st.button('💠Leave things as they are. People will give up their petrol cars eventually.'):
                st.success('Keep on rolling')
                st.text("Life continues as normal. Which means increasing polution and carbon emissions.\nPeople are angry you're not doing anything to help. ")
                session_state.money = session_state.money - 10
                session_state.hp = session_state.hp - 15
                session_state.temp = session_state.temp - 15
                session_state.q = 8
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)
            if st.button('💠 Give big grants to everyone who wants to buy electric cars'):
                st.success('Deals, deals, deals!')
                st.text("Electric cars are flying off the forecourt and you've made Elon Musk very happy.\nDue to the success of the scheme, this will be costly.")
                session_state.money = session_state.money - 20
                session_state.hp = session_state.hp + 20
                session_state.temp = session_state.temp - 20
                session_state.q = 8
                st.button('Next')
                add_score(session_state.user_id, session_state.money, session_state.temp)

        if q == 8:
            st.text('Your term has come to and end.')
            st.subheader('The citizens of the world thank you!')
            st.markdown('---')
            st.text('Your scores are')
            st.title(f"💰 {session_state.money} / 100")
            st.title(f"🌍 {session_state.hp} / 100")
            st.title(f"🕊️ {session_state.temp} / 100")

    # ========================== sidebar ============================== #
    if st.sidebar.button('reset'):
        session_state.q = 1
        session_state.money = 50
        session_state.hp = 50
        session_state.temp = 50
        session_state.user_id = random.randint(0, 1e6)
    
    st.sidebar.title(f"💰 {session_state.money} / 100")
    st.sidebar.title(f"🌍 {session_state.hp} / 100")
    st.sidebar.title(f"🕊️ {session_state.temp} / 100")
    st.sidebar.markdown('---')
    st.sidebar.text('\nBalance your\n💰ECONOMY 🌍ECOLOGY 🕊️EQUALITY')

if __name__ == '__main__':
    main()
