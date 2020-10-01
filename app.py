import streamlit as st
from streamlit.hashing import _CodeHasher
try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server
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

@st.cache
def start_game():
    create_usertable()
    create_chatlog()


def main():
    """Boardgame App"""

    start_game()
    state = _get_state()

    menu = ["Planet Earth", "Chat Room", "Settings"]
    choice = st.sidebar.selectbox("Settings", menu)
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
                add_chat(username, message)

            for m in view_chat():
                st.text(f'{m[3][-8:]} \t{m[1]}: {m[2]}')


    elif choice == "Settings":
        st.title("Hacker Zone")
        st.subheader("empty DB and start new game")

        if st.button('reset'):
            if st.button('really do it?'):
                empty_db()
                start_game()


    elif choice == 'Planet Earth':
        
        state.money = int(st.text_input("Set money.", state.input or ""))
        # st.write("Input state:", state.input)


        st.title("🌎 Welcome to Earth")
        st.sidebar.title(f"💰 Wealth: £{state.money}")
        st.sidebar.title(f"💪 HP: {100}")


        st.subheader("Do you wish to run for president?")
        if st.button('Yes'):
            st.balloons()
            st.text('Congratulations, you have won the race.\n\nWelcome Mr President.')

            st.text('You have recieved £250 from corporate lobbyists.')
            state.money += 250

        st.subheader("What is your first policy agenda?")
        if st.button('Green new deal'):
            st.text('You have sealed the deal. (Economy shrinks £3 trillion for two turns)')
            # money -= 100
        if st.button('Open national reserves for oil exploration'):
            st.text('You have found a bountiful plateau of crude oil (Economy gains £1 trillion) ')
            # money += 100
    
    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()



class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)
        
    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()
    
    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False
        
        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state


if __name__ == '__main__':
    main()
