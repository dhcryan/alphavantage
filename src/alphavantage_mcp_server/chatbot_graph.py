import re
import json
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from .chatbot_models import ChatbotState
from .mcp_client import AlphaVantageMCPClient

class IntentClassifier:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
            당신은 금융 데이터 질문을 분석하는 전문가입니다.
            다음 중 하나로 분류하고 필요한 파라미터를 추출하세요:
            
            도구들:
            - stock_quote: 주식 현재가 (symbol 필요)
            - company_overview: 회사 정보 (symbol 필요)  
            - rsi: RSI 지표 (symbol, interval 필요)
            - macd: MACD 지표 (symbol, interval, series_type 필요)
            - sma: 단순이동평균 (symbol, interval, time_period, series_type 필요)
            - time_series_daily: 일간 시계열 (symbol 필요)
            - news_sentiment: 뉴스 감정분석 (tickers 필요)
            - fx_daily: 환율 (from_symbol, to_symbol 필요)
            - crypto_daily: 암호화폐 (symbol, market 필요)
            
            응답 형식: {{"tool": "도구명", "symbol": "심볼", "기타파라미터": "값"}}
            """),
            ("human", "{query}")
        ])
    
    def classify(self, state: ChatbotState) -> ChatbotState:
        chain = self.prompt | self.llm
        result = chain.invoke({"query": state["user_query"]})
        
        try:
            parsed = json.loads(result.content)
            intent = parsed.get("tool", "stock_quote")
            symbol = parsed.get("symbol", self._extract_symbol(state["user_query"]))
            
            # 기본 파라미터 설정
            params = {"symbol": symbol}
            
            if intent in ["rsi", "macd", "sma"]:
                params["interval"] = "daily"
                
            if intent == "macd":
                params["series_type"] = "close"
                
            if intent == "sma":
                params["time_period"] = 20
                params["series_type"] = "close"
                
        except:
            intent = "stock_quote"
            symbol = self._extract_symbol(state["user_query"])
            params = {"symbol": symbol}
        
        return {
            **state,
            "intent": intent,
            "symbol": symbol,
            "parameters": params,
            "step_count": state["step_count"] + 1
        }
    
    def _extract_symbol(self, query: str) -> str:
        symbols = re.findall(r'\b[A-Z]{2,5}\b', query.upper())
        return symbols[0] if symbols else "AAPL"

class DataFetcher:
    def __init__(self):
        self.mcp_client = AlphaVantageMCPClient()
    
    async def fetch_data(self, state: ChatbotState) -> ChatbotState:
        intent = state["intent"]
        params = state["parameters"]
        
        try:
            data = await self.mcp_client.call_tool(intent, params)
        except Exception as e:
            data = {"error": f"데이터 조회 실패: {str(e)}"}
        
        return {
            **state,
            "financial_data": data,
            "step_count": state["step_count"] + 1
        }

class FinancialAnalyst:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    
    def analyze(self, state: ChatbotState) -> ChatbotState:
        data = state["financial_data"]
        intent = state["intent"]
        symbol = state["symbol"]
        
        if not data or "error" in data:
            analysis = f"죄송합니다. {symbol}의 데이터를 가져올 수 없습니다."
        else:
            analysis = self._create_analysis(data, intent, symbol)
        
        return {
            **state,
            "analysis_result": analysis,
            "step_count": state["step_count"] + 1
        }
    
    def _create_analysis(self, data: Dict, intent: str, symbol: str) -> str:
        if intent == "stock_quote" and "Global Quote" in data:
            quote = data["Global Quote"]
            price = quote.get("05. price", "N/A")
            change = quote.get("09. change", "N/A")
            change_percent = quote.get("10. change percent", "N/A")
            
            return f"""
📊 {symbol} 주식 현재 정보:
• 현재가: ${price}
• 변동: {change} ({change_percent})
• 거래량: {quote.get('06. volume', 'N/A')}
• 이전 종가: ${quote.get('08. previous close', 'N/A')}
"""

        elif intent == "company_overview" and "Symbol" in data:
            return f"""
🏢 {data.get('Name', symbol)} 회사 정보:
• 업종: {data.get('Sector', 'N/A')}
• 산업: {data.get('Industry', 'N/A')}
• 시가총액: {data.get('MarketCapitalization', 'N/A')}
• P/E 비율: {data.get('PERatio', 'N/A')}
• 배당수익률: {data.get('DividendYield', 'N/A')}
• 52주 최고가: ${data.get('52WeekHigh', 'N/A')}
• 52주 최저가: ${data.get('52WeekLow', 'N/A')}
"""

        elif intent in ["rsi", "macd", "sma"]:
            return f"📈 {symbol}의 {intent.upper()} 기술적 분석 데이터가 준비되었습니다."
        
        return f"{symbol}에 대한 {intent} 분석이 완료되었습니다."

def determine_next_step(state: ChatbotState) -> str:
    """다음 단계 결정"""
    return "fetch_data"

def generate_response(state: ChatbotState) -> ChatbotState:
    """최종 응답 생성"""
    analysis = state.get("analysis_result", "분석을 완료할 수 없습니다.")
    
    return {
        **state,
        "response": analysis,
        "step_count": state["step_count"] + 1
    }

def create_chatbot_graph():
    """LangGraph 워크플로우 생성"""
    
    classifier = IntentClassifier()
    data_fetcher = DataFetcher()
    analyst = FinancialAnalyst()
    
    workflow = StateGraph(ChatbotState)
    
    # 노드 추가
    workflow.add_node("classify", classifier.classify)
    workflow.add_node("fetch_data", data_fetcher.fetch_data)
    workflow.add_node("analyze", analyst.analyze)
    workflow.add_node("generate_response", generate_response)
    
    # 엣지 정의
    workflow.add_conditional_edges(
        "classify",
        determine_next_step,
        {"fetch_data": "fetch_data"}
    )
    
    workflow.add_edge("fetch_data", "analyze")
    workflow.add_edge("analyze", "generate_response")
    workflow.add_edge("generate_response", END)
    
    workflow.set_entry_point("classify")
    
    return workflow.compile()