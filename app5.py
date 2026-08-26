import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

st.set_page_config(page_title="AI Search Agent", page_icon="🌐")

st.title("🌐 Real-Time Web Search AI Agent")
st.write("Ask questions about current events, live news, or real-time data using Google Search.")

# Sidebar settings
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

enable_grounding = st.sidebar.checkbox("Enable Live Web Search", value=True)

if "search_chat_history" not in st.session_state:
    st.session_state.search_chat_history = []

if st.sidebar.button("Clear Search History"):
    st.session_state.search_chat_history = []
    st.rerun()

# Display previous messages
for message in st.session_state.search_chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process user prompt
if user_prompt := st.chat_input("Ask about real-time topics..."):
    if not api_key:
        st.error("Please provide a Gemini API Key to continue.")
    else:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.search_chat_history.append({"role": "user", "content": user_prompt})

        with st.chat_message("assistant"):
            with st.spinner("Processing prompt..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    # Configure tools based on toggle
                    config = None
                    if enable_grounding:
                        config = types.GenerateContentConfig(
                            tools=[types.Tool(google_search=types.GoogleSearch())]
                        )

                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=user_prompt,
                        config=config
                    )
                    
                    assistant_text = response.text
                    st.markdown(assistant_text)
                    st.session_state.search_chat_history.append({"role": "assistant", "content": assistant_text})

                except (APIError, Exception) as e:
                    err_msg = str(e)
                    if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                        st.error("⏳ **Quota Exceeded (429 Rate Limit)**")
                        st.warning(
                            "You have hit Google's free-tier API rate limit for Search Grounding.\n\n"
                            "**Quick Fixes:**\n"
                            "1. Uncheck **'Enable Live Web Search'** in the sidebar to ask questions using normal AI processing.\n"
                            "2. Wait **60 seconds** for your rate limit window to reset.\n"
                            "3. Generate a new API key in Google AI Studio if daily limits were reached."
                        )
                    else:
                        st.error(f"API Error: {e}")