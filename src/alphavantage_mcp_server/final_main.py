import asyncio
import os
from .advanced_chatbot_models import AdvancedChatbotState
from .final_fixed_chatbot import create_final_chatbot_graph

class FinalFixedChatbot:
    def __init__(self, use_openai=False):  # 기본값을 False로 변경
        # API 키 환경변수 설정
        os.environ['ALPHAVANTAGE_API_KEY'] = "CS0LBSPNM72HSNQL"
        
        # LangGraph 워크플로우 생성
        self.graph = create_final_chatbot_graph(use_openai=use_openai)
        self.conversation_history = []
        self.use_openai = use_openai
    
    async def chat(self, user_input: str) -> str:
        # 대화 기록 추가
        self.conversation_history.append(user_input)
        
        # 초기 상태 설정
        initial_state = AdvancedChatbotState(
            messages=[{"role": "user", "content": user_input}],
            user_query=user_input,
            conversation_history=self.conversation_history[-5:],
            intent=None,
            confidence=0.0,
            entities={},
            financial_data=None,
            analysis_result=None,
            formatted_response=None,
            step_count=0,
            processing_time=0.0,
            data_source=None,
            error_context=None
        )
        
        try:
            print(f"Debug - 초기 상태 설정 완료: {user_input}")
            print(f"Debug - OpenAI 사용: {self.use_openai}")
            
            # LangGraph 워크플로우 실행
            result = await self.graph.ainvoke(initial_state)
            
            print(f"Debug - 워크플로우 실행 완료")
            
            # 결과 반환
            response = result.get("formatted_response")
            if not response:
                response = result.get("analysis_result", "처리할 수 없습니다.")
            
            # 응답 기록 추가
            self.conversation_history.append(response)
            
            return response
            
        except Exception as e:
            import traceback
            print(f"Debug - 전체 오류: {e}")
            traceback.print_exc()
            
            error_msg = f"❌ 처리 중 오류가 발생했습니다: {str(e)}"
            self.conversation_history.append(error_msg)
            return error_msg
    
    def chat_sync(self, user_input: str) -> str:
        """동기 버전"""
        return asyncio.run(self.chat(user_input))
    
    def toggle_openai(self):
        """OpenAI 사용 토글"""
        self.use_openai = not self.use_openai
        self.graph = create_final_chatbot_graph(use_openai=self.use_openai)
        return f"OpenAI 사용: {'활성화' if self.use_openai else '비활성화'}"
    
    def clear_history(self):
        """대화 기록 초기화"""
        self.conversation_history = []
    
    def get_stats(self) -> dict:
        """챗봇 통계"""
        return {
            "total_conversations": len(self.conversation_history),
            "recent_queries": self.conversation_history[-3:] if self.conversation_history else [],
            "openai_enabled": self.use_openai
        }