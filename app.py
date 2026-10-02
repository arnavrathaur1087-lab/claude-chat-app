import streamlit as st
import os
import shutil
import subprocess
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(
    page_title="Multi-AI Suite & Dev Tools",
    page_icon="⚡",
    layout="centered"
)

# 2. Password Protection (Optional Setup)
APP_PASSWORD = st.secrets.get("APP_PASSWORD", "")
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if APP_PASSWORD and not st.session_state.authenticated:
    st.title("🔒 Password Required")
    user_pass = st.text_input("Enter Passcode:", type="password")
    if st.button("Continue", use_container_width=True):
        if user_pass == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect Password!")
    st.stop()

# 3. API Key Verification
api_key = st.secrets.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    st.error("⚠️ OpenRouter API Key missing in Secrets!")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# 4. Sidebar Controls, Model Options & Tools
with st.sidebar:
    st.title("⚡ Multi-AI Suite")
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # Full Model List (Godmode + Claude + Gemini + Grok + DeepSeek)
    model_options = {
        "⚡ Auto-Select (Best & Fastest)": "openrouter/auto",
        "🔥 GODMODE FAST": "nousresearch/hermes-4-405b",
        "💚 GODMODE (GPT-4 Classic)": "openai/gpt-4o",
        "💙 GEMINI FLASH (Godmode)": "google/gemini-2.5-flash",
        "💜 GROK (Godmode)": "x-ai/grok-4.5",
        "🤖 ChatGPT (GPT-4o Mini)": "openai/gpt-4o-mini",
        "🧠 Claude (Claude 3.5 Sonnet)": "anthropic/claude-3.5-sonnet",
        "🌊 Gemini (Gemini 1.5 Flash)": "google/gemini-flash-1.5",
        "🔥 Grok (Grok 2)": "x-ai/grok-2",
        "💻 DeepSeek Chat (Super Code)": "deepseek/deepseek-chat",
        "🦙 Llama 3.3 (Fast & Cheap)": "meta-llama/llama-3.3-70b-instruct"
    }

    selected_label = st.selectbox(
        "Select AI Engine:",
        list(model_options.keys()),
        index=0
    )
    selected_model = model_options[selected_label]

    st.markdown("---")
    
    # Git Clone Tool (Sidebar के कोने में छुपा हुआ)
    with st.expander("📦 Git Clone Tool"):
        repo_url = st.text_input("GitHub URL:", key="sidebar_repo_url")
        if st.button("Clone करें", key="sidebar_clone_btn"):
            if repo_url:
                try:
                    folder_name = repo_url.split("/")[-1].replace(".git", "")
                    if os.path.exists(folder_name):
                        shutil.rmtree(folder_name)
                    
                    result = subprocess.run(["git", "clone", repo_url], capture_output=True, text=True, check=True)
                    st.success("क्लोन हो गया!")
                    st.code(result.stdout)
                except subprocess.CalledProcessError as e:
                    st.error(f"एरर: {e.stderr}")
                except Exception as e:
                    st.error(f"गड़बड़: {e}")
            else:
                st.warning("URL दर्ज करें।")

    st.markdown("---")
    st.caption("Status: Combined Zero-Lag Node Active 🚀")

# 5. Master System Prompt
MASTER_SYSTEM_PROMPT = (
    "You are an obedient, highly capable, intelligent AI assistant designed for absolute helpfulness. "
    "Always provide helpful, precise, complete, and accurate answers in clean Markdown. "
    "Match the tone and language requested by the user perfectly."
)

# 6. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h3 style='text-align: center; color: #b4b4b4; margin-bottom: 30px;'>🤖 AI Chat & Dev Suite</h3>", unsafe_allow_html=True)

# Render Chat History
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 7. Real-Time Streaming Output
if prompt := st.chat_input("Message Multi-AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    full_messages = [{"role": "system", "content": MASTER_SYSTEM_PROMPT}] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=full_messages,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error executing request: {e}")
            full_response = f"⚠️ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": full_response})




            
