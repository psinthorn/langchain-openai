from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables, describe_tables_tool

load_dotenv()

chat = ChatOpenAI()
tables = list_tables()
tools = [run_query_tool, describe_tables_tool]


prompt = ChatPromptTemplate(
    messages = [
        SystemMessage(content=("You are AI and talking to a sqlite database./n"
                                f"Here are the tables in the database: {tables}./n"
                                "do not assumtions about the table exist in the database "
                                "or what column exist. instead use 'describe_tables' tool function to get the schema of the table./n"
                                 )),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name = 'agent_scratchpad'),
    ]
)

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools,

)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tools,
)

# agent_executor("Please give me a half of users are in the database?")
agent_executor("give me a name, email and addresses of user who has id 1? and if any column is empty, please give me a null value. and if column it is not exist please skip it and next.")
# agent_executor("give me a list of column name in users table?")

