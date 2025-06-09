import streamlit as st
from src.alphavantage_mcp_server.langgraph_chatbot import AlphaVantageFinancialChatbot

def main():
    st.title("🏦 AlphaVantage LangGraph 챗봇")
    st.write("LangGraph와 AlphaVantage API를 활용한 금융 챗봇입니다!")
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = AlphaVantageFinancialChatbot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # 채팅 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("금융 질문을 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("LangGraph로 분석 중..."):
                response = st.session_state.chatbot.chat_sync(prompt)
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 사이드바 예제
    with st.sidebar:
        st.header("💡 예제 질문")
        examples = [
            "AAPL 주식 현재가 알려줘",
            "테슬라 회사 정보 보여줘",
            "MSFT RSI 지표 분석해줘",
            "구글 MACD 지표는?",
            "아마존 20일 이동평균 알려줘"
        ]
        
        for example in examples:
            if st.button(example, key=example):
                st.session_state.messages.append({"role": "user", "content": example})
                with st.chat_message("assistant"):
                    response = st.session_state.chatbot.chat_sync(example)
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

if __name__ == "__main__":
    main()