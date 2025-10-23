from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage,AIMessage,HumanMessage
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,List,Annotated
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()

## defining the checkpointer
checkpointer = MemorySaver()
llm = ChatOpenAI()
 ## print(llm.invoke("what is machine learning").content)
 ## creating the State

class State(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]

def get_chat(state:State):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages":[response]}

workflow = StateGraph(State)
workflow.add_node("get_chat",get_chat)
workflow.add_edge(START,"get_chat")
workflow.add_edge("get_chat",END)

graph = workflow.compile(checkpointer = checkpointer)

# input = {"messages":[HumanMessage("what is machine Learning")]}
# output = graph.invoke(input)
# print(output)
# print(output["messages"][-1].content)

## since it is not giving the vibe of a chatbot
## so in order to get the vibe of a chatbot i will use the while loop here


##chat_history = []
thread_id = 1
while True:
    user_input = input("Enter your question:\n")
    config = {"configurable":{"thread_id":thread_id}}
    if user_input.lower().strip() in ["exit","stop","break"]:
        break ## come out of the loop in this case ,user wants to stop the chatting
    ##chat_history.append(HumanMessage(user_input))
    messages = {"messages":[HumanMessage(user_input)]}

    response = graph.invoke(messages,config=config)

    print(response["messages"][-1].content)
    # chat_history.append(AIMessage(content = response["messages"][-1].content))
    







