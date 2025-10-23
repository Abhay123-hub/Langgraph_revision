from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,END,START
from dotenv import load_dotenv
from typing import TypedDict,List
from langgraph.checkpoint.memory import MemorySaver


## activating all the secret variables
load_dotenv()

llm = ChatOpenAI()
# response = llm.invoke("what is Data Science and Machine Learning?").content
# print(response) ## llm is working fine


checkpointer = MemorySaver() ## saves the memory in the Computer RAM,used for study and experiment
## for production or in industry we use DataBase for storing the chats in the chatbot

class State(TypedDict):
    topic:str
    joke:str
    explanation:str

def get_joke(state:State):
    topic = state.get("topic")
    prompt = f"Generate a joke on this topic {topic}"
    joke = llm.invoke(prompt).content
    return {"joke":joke}

def get_explanation(state:State):
    joke = state.get("joke")
    prompt = f"Explain the following joke \n {joke}"
    explanation = llm.invoke(prompt).content

    return {"explanation":explanation}


graph = StateGraph(State)

graph.add_node("get_joke",get_joke)
graph.add_node("get_explanation",get_explanation)

graph.add_edge(START,"get_joke")
graph.add_edge("get_joke","get_explanation")
graph.add_edge("get_explanation",END)

workflow = graph.compile(checkpointer = checkpointer)

config_1 = {"configurable":{"thread_id":"1"}}

response = workflow.invoke({"topic":"pizza"},config = config_1)
print(response)
