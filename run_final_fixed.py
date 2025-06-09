import asyncio
import os
import sys

# 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from alphavantage_mcp_server.final_main import FinalFixedChatbot

async def main():
    print("""
🚀 **Final Fixed LangGraph 금융 챗봇**
💡 완전 수정된 버전 - OpenAI 선택 가능

🔧 **최종 수정 사항:**
• ✅ ChatPromptTemplate 변수 오류 완전 해결
• ✅ 규칙 기반 폴백 시스템 강화
• ✅ OpenAI 사용/비사용 선택 가능
• ✅ 모든 디버깅 정보 추가
""")
    print("=" * 70)
    
    # OpenAI 사용 여부 선택
    use_openai = input("OpenAI를 사용하시겠습니까? (y/n, 기본값: n): ").lower().startswith('y')
    
    chatbot = FinalFixedChatbot(use_openai=use_openai)
    
    print(f"\n🤖 챗봇 초기화 완료 (OpenAI: {'사용' if use_openai else '미사용'})")
    
    # 예제 질문 표시
    examples = [
        "🟢 TSLA 현재가",
        "🔵 AAPL 회사 정보", 
        "🟡 NVDA RSI 분석",
        "🟣 MSFT 뉴스 감정",
        "🟠 GOOGL MACD"
    ]
    
    print("\n💡 **테스트 질문:**")
    for example in examples:
        print(f"   {example}")
    
    print(f"\n📝 **명령어:** 'quit' (종료), 'clear' (초기화), 'stats' (통계), 'toggle' (OpenAI 토글)")
    print("=" * 70)
    
    while True:
        try:
            user_input = input("\n🤖 질문: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료', 'q']:
                print("👋 Final Fixed 챗봇을 종료합니다!")
                break
            
            elif user_input.lower() == 'clear':
                chatbot.clear_history()
                print("🗑️ 대화 기록이 초기화되었습니다.")
                continue
            
            elif user_input.lower() == 'toggle':
                result = chatbot.toggle_openai()
                print(f"🔄 {result}")
                continue
            
            elif user_input.lower() == 'stats':
                stats = chatbot.get_stats()
                print(f"""
📊 **챗봇 통계:**
• 총 대화 수: {stats['total_conversations']}
• OpenAI 상태: {'활성화' if stats['openai_enabled'] else '비활성화'}
• 최근 질문: {stats['recent_queries'][-1] if stats['recent_queries'] else '없음'}
""")
                continue
            
            if not user_input:
                print("❓ 질문을 입력해주세요.")
                continue
            
            print("🔄 Final Fixed 워크플로우 실행 중...")
            response = await chatbot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 챗봇을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 시스템 오류: {e}")

if __name__ == "__main__":
    asyncio.run(main())