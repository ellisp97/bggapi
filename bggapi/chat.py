import json
import pandas as pd
from boardgame import Boardgame
from chain import get_ai_model
from user import User
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from langchain.callbacks import get_openai_callback


class ChatAI():
    user = None
    boardgame = None
    pandas_ai = None
    df = None

    PLOT_TYPES = ["bar", "line", "table"]
    PLOT_ALIASES = ["plot", "chart", "graph", "draw"]

    def parse_query(self, query: str):
        df = self.user.boardgame_dict[self.boardgame.name]
        if not self.pandas_ai or self.df is not df:
            self.pandas_ai = get_ai_model(df)
        self.df = df
        try:
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            with get_openai_callback() as cb:
                response = self.pandas_ai.run(self.get_prompt(query), callbacks=[st_cb])
                st.write(f'Spent a total of {cb.total_tokens} tokens')
                self.parse_response(response)
        except Exception as e:
            # TODO: Handle errors from the LLM
            raise e

        return response

    def parse_response(self, response):
        response_dict = None

        print("This is the response: ", response)
        try:
            response_dict = json.loads(response) if type(response) == str else response
        except Exception as e:
            print("Error converting response to dict: ", e)

        if response_dict and any(plot_type in response for plot_type in self.PLOT_TYPES):
            if "bar" in response_dict:
                data = response_dict["bar"]
                df = pd.DataFrame(data["data"], columns=data["columns"])
                df.set_index(data["columns"][0], inplace=True)
                st.bar_chart(df)

            # Check if the response is a line chart.
            if "line" in response_dict:
                data = response_dict["line"]
                df = pd.DataFrame(data["data"], columns=data["columns"])
                df.set_index(data["columns"][0], inplace=True)
                df = df.T
                st.line_chart(df)

            # Check if the response is a table.
            if "table" in response_dict:
                data = response_dict["table"]
                df = pd.DataFrame(data["data"], columns=data["columns"])
                st.table(df)
    def get_prompt(self, query: str):
        # If no plot aliases are found we don't need to reinforce the prompt to return json data
        if not any(plot_type in query for plot_type in self.PLOT_ALIASES):
            return query

        return """
            For the following query, if it requires drawing a table, reply as follows:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

            If the query requires creating a bar chart, reply as follows:
            {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a line chart, reply as follows:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            There can only be two types of chart, "bar" and "line".

            All strings and booleans in "columns" list and data list, should be in double quotes,

            For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

            Below is the query.
            Query: 
            """ + query

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


