import asyncio
from .chatbot_models import ChatbotState
from .chatbot_graph import create_chatbot_graph

class AlphaVantageFinancialChatbot:
    def __init__(self):
        self.graph = create_chatbot_graph()
    
    async def chat(self, user_input: str) -> str:
        initial_state = ChatbotState(
            messages=[{"role": "user", "content": user_input}],
            user_query=user_input,
            intent=None,
            symbol=None,
            parameters={},
            financial_data=None,
            analysis_result=None,
            response=None,
            step_count=0
        )
        
        try:
            result = await self.graph.ainvoke(initial_state)
            return result["response"]
        except Exception as e:
            return f"처리 중 오류가 발생했습니다: {str(e)}"
    
    def chat_sync(self, user_input: str) -> str:
        return asyncio.run(self.chat(user_input))