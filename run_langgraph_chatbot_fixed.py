import asyncio
import os
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from alphavantage_mcp_server.langgraph_chatbot import AlphaVantageFinancialChatbot

async def main():
    print("🤖 AlphaVantage LangGraph 챗봇 시작!")
    print("금융 데이터에 대해 질문해보세요. (종료: 'quit')")
    print("-" * 50)
    
    chatbot = AlphaVantageFinancialChatbot()
    
    while True:
        try:
            user_input = input("\n💬 질문: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료']:
                print("챗봇을 종료합니다!")
                break
            
            if not user_input:
                continue
            
            print("🔍 분석 중...")
            response = await chatbot.chat(user_input)
            print(f"\n{response}")
            
        except KeyboardInterrupt:
            print("\n챗봇을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류: {e}")

if __name__ == "__main__":
    asyncio.run(main())