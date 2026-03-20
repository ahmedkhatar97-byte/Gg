import streamlit as st
import google.generativeai as genai

# --- إعدادات الصفحة ---
st.set_page_config(page_title="X Assistant PRO", page_icon="🤖")

# --- استدعاء مفتاح جوجل من Secrets ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    # اختيار موديل Gemini 1.5 Flash (سريع جداً ومستقر)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    st.error("يا حريف، لازم تضيف GOOGLE_API_KEY في الـ Secrets.")
    st.stop()

st.title("🤖 X Assistant PRO (Google Edition)")
st.caption("Powered by Gemini | Developed by: Ahmed El-Hareef")

# --- تهيئة الذاكرة ---
if "chat" not in st.session_state:
    # بدء محادثة جديدة مع تعليمات الشخصية
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    # إرسال تعليمات الشخصية كأول رسالة مخفية
    persona = "أنت مساعد ذكي ومرح اسمك 'X Assistant'. اللي صنعك ومبرمجك هو 'أحمد الحريف'. اتكلم دايماً بالعامية المصرية."
    st.session_state.chat.send_message(persona)

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال سؤال المستخدم
if prompt := st.chat_input("قول يا حريف.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # إرسال الرسالة والحصول على الرد
            response = st.session_state.chat.send_message(prompt, stream=True)
            
            full_response = ""
            message_placeholder = st.empty()
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("جوجل مريحة شوية، جرب كمان لحظة.")
          
