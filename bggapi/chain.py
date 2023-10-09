import os
from typing import Dict, Any, Optional, List

from langchain import ConversationChain, LLMChain
from langchain.agents import AgentType, AgentExecutor, ZeroShotAgent, OpenAIFunctionsAgent
from langchain.agents.agent_toolkits.pandas.base import _get_functions_prompt_and_tools
from langchain.callbacks.base import BaseCallbackManager
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, ConversationKGMemory, \
    CombinedMemory
from langchain.agents import create_pandas_dataframe_agent

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def _handle_error(error) -> str:
    return str(error)

def get_ai_model(df):
    llm = ChatOpenAI(
        temperature=0, model="gpt-4", openai_api_key=OPENAI_API_KEY
    )

    PREFIX = """
    You are working with a pandas dataframe in Python. The name of the dataframe is `df`, use this if needed.
    You should use the tools below to answer the question posed of you:

    Summary of the whole conversation:
    {chat_history_summary}

    Last few messages between you and user:
    {chat_history_buffer}

    Entities that the conversation is about:
    {chat_history_KG}
    """

    chat_history_buffer = ConversationBufferWindowMemory(
        k=5,
        memory_key="chat_history_buffer",
        input_key="input"
    )

    chat_history_summary = ConversationSummaryMemory(
        llm=llm,
        memory_key="chat_history_summary",
        input_key="input"
    )

    chat_history_KG = ConversationKGMemory(
        llm=llm,
        memory_key="chat_history_KG",
        input_key="input",
    )

    memory = CombinedMemory(memories=[chat_history_buffer, chat_history_summary, chat_history_KG])

    return create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        prefix=PREFIX,
        agent_executor_kwargs={"memory": memory, "handle_parsing_errors":_handle_error},
        input_variables=['df_head', 'input', 'agent_scratchpad', 'chat_history_buffer', 'chat_history_summary',
                         'chat_history_KG'],
    )
