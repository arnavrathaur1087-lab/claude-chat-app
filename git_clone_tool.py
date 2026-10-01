import streamlit as st
import subprocess
import os

st.title("📦 Git Clone Tool")
st.markdown("यहाँ से आप आसानी से गिट रिपॉजिटरी क्लोन कर सकते हैं।")

repo_url = st.text_input("GitHub URL डालें:")

if st.button("Clone करें"):
    if repo_url:
        try:
            # ==========================================
            # 🔥 https://github.com/elder-plinius/G0DM0D3.git
            # ==========================================
            
            # यह रहा डिफ़ॉल्ट क्लोन कोड (तू चाहे तो इसे रख या बदल ले):
            result = subprocess.run(["git", "clone", repo_url], capture_output=True, text=True, check=True)
            st.success("सफलतापूर्वक क्लोन हो गया!")
            st.code(result.stdout)
            
        except Exception as e:
            st.error(f"एरर आ गया: {e}")
    else:
        st.warning("कृपया पहले लिंक डालें।")

