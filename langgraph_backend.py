## importing all the main libraries
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated,List
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

## activating up all the secret variables
load_dotenv()
checkpointer = InMemorySaver()
llm = ChatOpenAI()
config = {"configurable":{"thread_id":"1"}}

class State(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

def basic_chatbot(state:State):
    message = state["messages"]
    response = llm.invoke(message)
    return {"messages":[response]}

## now defining the graph in the backend

graph = StateGraph(State)
graph.add_node("basic_chatbot",basic_chatbot)
graph.add_edge(START,"basic_chatbot")
graph.add_edge("basic_chatbot",END)
chatbot= graph.compile(checkpointer = checkpointer)

# question = 'waht is realtionship netween statistics and agentic ai'
# response = chatbot.invoke({"messages":[question]},config = config)
# print(response["messages"][-1].content)


## this all is the backend code for creating the chatbot
## there are lot of changes and advancements can be done on this chatbot
## which will be done later, as of now we are just creating a simple chatbot


## using streaming in the langgraph
## what will be the benifit of using streaming in the langgraph
## and what actually the streaming means in the langgraph
## now the chatbot we have made gives the response in one go
## and if the output is large first it will take a lot of time
## and will display the long text in one go only
## which will make the user experience bad on our chatbot
## so we want that our chatbot should generate token by token 
## which will engage the user on the website 
## that is why streaming is used in langgraph for making the good cahtbots

# for message_chunk,metadat in chatbot.stream(
#     {"messages":[HumanMessage(content = "How the applied mathematics is used in the Agentic AI?")]},
#     config = config,
#     stream_mode = "messages"
# ):
#     if message_chunk.content:
#        print(message_chunk.content,end = " ",flush = True)

