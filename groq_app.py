import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load knowledge base
with open("o2c_knowledge.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()

# Page config
st.set_page_config(
    page_title="SAP O2C Assistant",
    page_icon="robot",
    layout="centered"
)

# Header
st.title("SAP O2C Assistant")
st.caption("Ask me anything about SAP Order to Cash process")
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am your SAP O2C Assistant. Ask me anything about the Order to Cash process, transaction codes, or SAP SD module."
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Type your SAP question here..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            prompt = f"""You are an SAP O2C expert assistant.
Answer the user question ONLY based on the knowledge base below.
If answer is not in knowledge base, say "I do not have information on this topic yet. Please contact your SAP consultant."
Keep answers clear, simple and practical.

KNOWLEDGE BASE:
{knowledge}

USER QUESTION:
{user_input}

Answer:"""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )

            answer = response.choices[0].message.content
            st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
