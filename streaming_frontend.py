import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

config = {"configurable":{"thread_id":"1"}}

## there is a dictionary in the streamlit named as st.session_state
## we can store the chat history in this dictionary
## such that even after the streamlit is called 
## we will define a messages list in this dictionary as a key
## which will be storing the entire chat history
st.title("simple chatbot ")
if "messages" not in st.session_state:
    st.session_state["messages"] = []

## loading the conversation history

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])
## till here all previous chat has been displayed on the user interface
## now we can get the answer of our current user question using the backend code 


## taking the input from the user
user_input = st.chat_input("Enter your question here")

if user_input:
    st.session_state["messages"].append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.text(user_input)
    ## now getting the response from backend based on the user question
    ## this time the response will be printed along with streaming
    ## means token by token will be printed

    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {"messages":[HumanMessage(content = user_input)]},
                config = config,
                stream_mode = "messages"
            )
        )
        st.session_state["messages"].append({"role":"assistant","content":ai_message}) ## just for display on the suer interface






