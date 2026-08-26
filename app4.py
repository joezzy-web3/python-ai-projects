import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="AI Chat Assistant", page_icon="💬")

st.title("💬 Multi-Turn AI Document Chat")
st.write("Upload a file and have a continuous conversation about its contents.")

api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
uploaded_file = st.sidebar.file_uploader("Upload a document", type=["txt", "pdf"])

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()

if uploaded_file and api_key:
    file_bytes = uploaded_file.read()
    st.sidebar.success(f"Loaded: `{uploaded_file.name}`")
    
    # Display previous messages from memory
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input field at the bottom
    if user_input := st.chat_input("Ask a follow-up question..."):
        # 1. Display user message in UI and save to state
        st.chat_message("user").markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # 2. Generate response from Gemini
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    # Package history + new input as context
                    history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history])
                    
                    if uploaded_file.name.endswith(".pdf"):
                        contents = [
                            types.Part.from_bytes(data=file_bytes, mime_type="application/pdf"),
                            f"Conversation History:\n{history_context}\n\nAnswer the latest question."
                        ]
                    else:
                        doc_text = file_bytes.decode("utf-8")
                        contents = f"Document:\n{doc_text}\n\nHistory:\n{history_context}"

                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=contents,
                    )
                    
                    assistant_text = response.text
                    st.markdown(assistant_text)
                    
                    # 3. Save assistant response to state
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})
                except Exception as e:
                    st.error(f"API Error: {e}")

elif not api_key:
    st.info("Please enter your Gemini API Key in the sidebar.")
elif not uploaded_file:
    st.info("Please upload a document to start chatting.")