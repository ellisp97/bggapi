import streamlit as st

from chat import ChatAI

def main():
    # Get or create the session state dictionary
    if 'session_state' not in st.session_state:
        st.session_state['session_state'] = {}

    # Retrieve the ChatAI object from the session state
    if 'chat' not in st.session_state['session_state']:
        st.session_state['session_state']['chat'] = ChatAI()

    # Retrieve the ChatAI object from the session state
    chat = st.session_state['session_state']['chat']

    st.title('BGG API Analysis')
    st.sidebar.header('Board Game Play Data')
    st.sidebar.write('This app allows you to query the BGG API for play data and perform analysis on the results.')

    # Load the user / boardgame data into the side bar
    chat.subheader_boardgame()
    chat.subheader_user()

    # Store LLM generated responses
    if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input(disabled=not (chat.user and chat.boardgame)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                st.write(response := chat.parse_query())
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)




if __name__ == '__main__':
    main()
