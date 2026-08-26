import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="AI Search Agent", page_icon="🌐")

st.title("🌐 Real-Time Web Search AI Agent")
st.write("Ask questions about current events, live news, or real-time data using Google Search.")

# Retrieve API key from Streamlit secrets or sidebar
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if "search_chat_history" not in st.session_state:
    st.session_state.search_chat_history = []

if st.sidebar.button("Clear Search History"):
    st.session_state.search_chat_history = []
    st.rerun()

# Display previous chat messages
for message in st.session_state.search_chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process user input
if user_prompt := st.chat_input("Ask about real-time topics..."):
    if not api_key:
        st.error("Please provide a Gemini API Key to continue.")
    else:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.search_chat_history.append({"role": "user", "content": user_prompt})

       # Enable Google Search Tool for live grounding
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            tools=[types.Tool(google_search=types.GoogleSearch())]
                        )
                    )
                        config=types.GenerateContentConfig(
                            tools=[types.Tool(google_search=types.GoogleSearch())]
                        )
                    )
                    
                    assistant_text = response.text
                    st.markdown(assistant_text)
                    st.session_state.search_chat_history.append({"role": "assistant", "content": assistant_text})
                except Exception as e:
                    st.error(f"API Error: {e}")