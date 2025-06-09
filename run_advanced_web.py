import streamlit as st
import sys
import os

# 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from alphavantage_mcp_server.advanced_langgraph_main import AdvancedLangGraphChatbot

def main():
    st.set_page_config(
        page_title="Advanced LangGraph 금융 챗봇",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Advanced LangGraph 금융 챗봇")
    st.markdown("**OpenAI + AlphaVantage + LangGraph** 통합 시스템")
    
    # 초기화
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = AdvancedLangGraphChatbot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # 사이드바
    with st.sidebar:
        st.header("🎯 고급 기능")
        
        st.subheader("💡 예제 질문")
        examples = [
            "NVDA 현재가",
            "AAPL 회사 정보", 
            "TSLA RSI 분석",
            "MSFT 뉴스 감정",
            "GOOGL MACD"
        ]
        
        for example in examples:
            if st.button(example, key=f"btn_{example}"):
                st.session_state.messages.append({"role": "user", "content": example})
                
                with st.spinner("🔄 LangGraph 처리 중..."):
                    response = st.session_state.chatbot.chat_sync(example)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        st.divider()
        
        # 통계
        if st.button("📊 통계 보기"):
            stats = st.session_state.chatbot.get_stats()
            st.json(stats)
        
        if st.button("🗑️ 기록 초기화"):
            st.session_state.chatbot.clear_history()
            st.session_state.messages = []
            st.success("초기화 완료!")
            st.rerun()
    
    # 메인 채팅 영역
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 채팅 기록 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 사용자 입력
        if prompt := st.chat_input("💬 금융 질문을 입력하세요..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("🔄 Advanced LangGraph로 분석 중..."):
                    response = st.session_state.chatbot.chat_sync(prompt)
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.subheader("🎛️ 시스템 정보")
        
        if st.session_state.messages:
            last_msg = st.session_state.messages[-1]
            if "분석 신뢰도:" in last_msg["content"]:
                # 신뢰도 추출 및 표시
                import re
                confidence_match = re.search(r'분석 신뢰도:\s*(\d+)%', last_msg["content"])
                if confidence_match:
                    confidence = int(confidence_match.group(1))
                    st.metric("🎯 신뢰도", f"{confidence}%")
                    st.progress(confidence / 100)
        
        st.metric("💬 총 대화", len(st.session_state.messages))
        
        # 시스템 상태
        st.success("🟢 LangGraph 연결됨")
        st.success("🟢 OpenAI 연결됨") 
        st.success("🟢 AlphaVantage 연결됨")

if __name__ == "__main__":
    main()