from boardgame import Boardgame
from chain import get_ai_model
from user import User
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st


class ChatAI():
    user = None
    boardgame = None
    pandas_ai = None

    def parse_query(self):
        df = self.user.boardgame_dict[self.boardgame.name]
        self.pandas_ai = get_ai_model(df)
        try:
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = self.pandas_ai.run(st.session_state.messages, callbacks=[st_cb])
        except Exception as e:
            # TODO: Handle errors from the LLM
            raise e

        return response

    def subheader_user(self):
        st.sidebar.subheader('User Data')
        username = st.sidebar.text_input('Enter a username:', '')
        if not self.user or self.user.username != username:
            try:
                if username:
                    self.user = User(username=username)
            except Exception as e:
                print(e)
                st.sidebar.write('Username {} not found'.format(username))

        if self.user:
            st.sidebar.subheader(self.user.username)
            st.sidebar.write("Boardgames: ", list(self.user.boardgame_dict.keys()))


    def subheader_boardgame(self):
        st.sidebar.subheader('Boardgame Data')
        name = st.sidebar.text_input('Enter a boardgame name:', '')
        if not self.boardgame or self.boardgame.name != name:
            try:
                if name:
                    self.boardgame = Boardgame(name=name)
                    st.sidebar.subheader(self.boardgame.name)
            except Exception as e:
                print(e)
                st.sidebar.write('Boardgame {} not found'.format(name))
