import os
import streamlit as st
from anthropic import Anthropic

st.set_page_config(page_title="Secure Claude AI", page_icon="🔒")

# 1. Authentication (पासवर्ड चेक)
APP_PASSWORD = st.secrets.get("APP_PASSWORD") or os.environ.get("APP_PASSWORD", "1234")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 लॉगिन आवश्यक है")
    user_pass = st.text_input("ऐप का एक्सेस पासवर्ड दर्ज करें:", type="password")
    if st.button("लॉगिन करें"):
        if user_pass == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("गलत पासवर्ड! कृपया दोबारा कोशिश करें।")
    st.stop()

# 2. API Key चेक
api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("⚠️ API Key सेट नहीं है!")
    st.stop()

client = Anthropic(api_key=api_key)

# 3. Chat Interface Logic
st.title("🤖 सुरक्षित Claude चैट सहायक")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("अपना सवाल पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Claude सोच रहा है..."):
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=st.session_state.messages
            )
            reply = response.content[0].text
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
