import os
from langchain.agents import AgentType
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Retrieve the API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_ai_model(df):

    llm = ChatOpenAI(
        temperature=0, model="gpt-4", openai_api_key=OPENAI_API_KEY, streaming=True
    )

    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True,
    )

