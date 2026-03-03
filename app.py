import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="LLM Coding Assistant", page_icon="🤖")

st.title("🤖 LLM Coding Assistant & Code Reviewer")
st.caption("وضعين: مساعد برمجي + مراجع كود")

# Sidebar
st.sidebar.header("الإعدادات")
mode = st.sidebar.selectbox("اختر الوضع", ["Coding Assistant", "Code Reviewer"])
api_key_input = st.sidebar.text_input("API Key (اختياري)", type="password")
clear = st.sidebar.button("🧹 Clear Chat")

# API Key logic
api_key = api_key_input or os.getenv("OPENAI_API_KEY")

if clear:
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# System prompts per mode
ASSISTANT_PROMPT = "أنت مساعد برمجي خبير. ساعد المستخدم على كتابة كود نظيف وشرح وتصحيح أخطاء."
REVIEWER_PROMPT = "أنت مراجع كود Senior. راجع الكود بدقة من ناحية الأخطاء والأمان والأداء وأعطِ ملاحظات قابلة للتطبيق."

system_prompt = ASSISTANT_PROMPT if mode == "Coding Assistant" else REVIEWER_PROMPT

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_text = st.chat_input("اكتب سؤالك أو الصق الكود هنا...")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    if not api_key:
        with st.chat_message("assistant"):
            st.error("🚫 ما في API Key. حط المفتاح في Sidebar أو داخل .env")
    else:
        client = OpenAI(api_key=api_key)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.messages
                    ],
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"صار خطأ: {e}")