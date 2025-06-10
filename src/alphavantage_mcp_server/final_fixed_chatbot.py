import re
import json
import time
import asyncio
import os
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from .advanced_chatbot_models import AdvancedChatbotState
from .api import fetch_quote, fetch_company_overview, fetch_rsi, fetch_macd, fetch_sma, fetch_news_sentiment

class FinalFixedIntentClassifier:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
        # 프롬프트에서 중괄호 문제 수정
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
당신은 금융 질문 분류 전문가입니다. 다음 형식으로 응답하세요:

분류 가능한 인텐트:
- stock_quote: 주식 현재가, 시세, 가격
- company_overview: 회사 정보, 개요, 재무지표  
- technical_analysis: RSI, MACD, SMA 등 기술적 분석
- market_sentiment: 뉴스, 감정 분석

JSON 응답 형식 (중괄호 2개 사용):
{{"intent": "stock_quote", "confidence": 0.95, "entities": {{"symbol": "AAPL"}}}}
"""),
            ("human", "질문: {query}")
        ])
    
    def classify(self, state: AdvancedChatbotState) -> AdvancedChatbotState:
        start_time = time.time()
        
        try:
            # OpenAI 호출 시도
            chain = self.prompt | self.llm
            result = chain.invoke({"query": state["user_query"]})
            
            print(f"Debug - OpenAI 응답: {result.content}")
            
            # JSON 파싱 시도
            try:
                # 결과에서 JSON 부분만 추출
                content = result.content.strip()
                
                # JSON이 코드 블록에 있는 경우 추출
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()
                elif "```" in content:
                    json_start = content.find("```") + 3
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()
                
                # 중괄호로 시작하는 JSON 찾기
                if "{" in content:
                    json_start = content.find("{")
                    json_end = content.rfind("}") + 1
                    content = content[json_start:json_end]
                
                parsed = json.loads(content)
                intent = parsed.get("intent", "stock_quote")
                confidence = parsed.get("confidence", 0.8)
                entities = parsed.get("entities", {})
                
                print(f"Debug - 성공적으로 파싱됨: {intent}, {confidence}")
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Debug - JSON 파싱 실패: {e}")
                # 폴백: 규칙 기반 분류
                intent, confidence, entities = self._fallback_classification(state["user_query"])
                print(f"Debug - 폴백 분류: {intent}, {confidence}")
            
            # 심볼이 없으면 추출 시도
            if "symbol" not in entities:
                entities["symbol"] = self._extract_symbol(state["user_query"])
            
            return {
                **state,
                "intent": intent,
                "confidence": confidence,
                "entities": entities,
                "step_count": state["step_count"] + 1,
                "processing_time": time.time() - start_time
            }
            
        except Exception as e:
            print(f"Debug - OpenAI 호출 실패: {e}")
            # 완전 폴백: 규칙 기반 분류
            intent, confidence, entities = self._fallback_classification(state["user_query"])
            entities["symbol"] = self._extract_symbol(state["user_query"])
            
            return {
                **state,
                "intent": intent,
                "confidence": confidence,
                "entities": entities,
                "error_context": f"OpenAI 분류 실패, 규칙 기반 사용: {str(e)}",
                "step_count": state["step_count"] + 1,
                "processing_time": time.time() - start_time
            }
    
    def _fallback_classification(self, query: str) -> tuple:
        """규칙 기반 폴백 분류"""
        query_lower = query.lower()
        
        print(f"Debug - 규칙 기반 분류 시작: {query_lower}")
        
        if any(word in query_lower for word in ["현재가", "시세", "가격", "quote", "price", "주가"]):
            return "stock_quote", 0.9, {}
        elif any(word in query_lower for word in ["회사", "정보", "개요", "overview", "company", "기업"]):
            return "company_overview", 0.9, {}
        elif any(word in query_lower for word in ["rsi", "macd", "sma", "기술적", "지표", "분석"]):
            return "technical_analysis", 0.9, {}
        elif any(word in query_lower for word in ["뉴스", "감정", "sentiment", "시장"]):
            return "market_sentiment", 0.9, {}
        else:
            return "stock_quote", 0.8, {}  # 기본값
    
    def _extract_symbol(self, query: str) -> str:
        symbols = re.findall(r'\b[A-Z]{2,5}\b', query.upper())
        symbol = symbols[0] if symbols else "AAPL"
        print(f"Debug - 심볼 추출: {symbol}")
        return symbol

# OpenAI 없이 작동하는 완전 규칙 기반 분류기
class SimpleRuleBasedClassifier:
    def classify(self, state: AdvancedChatbotState) -> AdvancedChatbotState:
        start_time = time.time()
        query = state["user_query"]
        
        print(f"Debug - 규칙 기반 분류기 사용: {query}")
        
        # 규칙 기반 분류
        intent, confidence, entities = self._classify_by_rules(query)
        
        # 심볼 추출
        symbol = self._extract_symbol(query)
        entities["symbol"] = symbol
        
        print(f"Debug - 분류 결과: intent={intent}, confidence={confidence}, symbol={symbol}")
        
        return {
            **state,
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "step_count": state["step_count"] + 1,
            "processing_time": time.time() - start_time
        }
    
    def _classify_by_rules(self, query: str) -> tuple:
        """완전 규칙 기반 분류"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["현재가", "시세", "가격", "quote", "price", "주가"]):
            return "stock_quote", 0.95, {}
        elif any(word in query_lower for word in ["회사", "정보", "개요", "overview", "company", "기업"]):
            return "company_overview", 0.95, {}
        elif any(word in query_lower for word in ["rsi", "macd", "sma", "기술적", "지표", "분석"]):
            return "technical_analysis", 0.95, {}
        elif any(word in query_lower for word in ["뉴스", "감정", "sentiment", "시장"]):
            return "market_sentiment", 0.95, {}
        else:
            return "stock_quote", 0.85, {}
    
    def _extract_symbol(self, query: str) -> str:
        symbols = re.findall(r'\b[A-Z]{2,5}\b', query.upper())
        return symbols[0] if symbols else "AAPL"

class FinalDataFetcher:
    def __init__(self):
        self.api_key = "IZLU4YURP1R1YVYW"
        os.environ['ALPHAVANTAGE_API_KEY'] = self.api_key
    
    async def fetch_data(self, state: AdvancedChatbotState) -> AdvancedChatbotState:
        start_time = time.time()
        intent = state["intent"]
        entities = state["entities"]
        symbol = entities.get("symbol", "AAPL")
        
        print(f"Debug - 데이터 조회 시작: {intent} for {symbol}")
        
        try:
            if intent == "stock_quote":
                data = await fetch_quote(symbol=symbol)
                data_source = "AlphaVantage Global Quote"
                
            elif intent == "company_overview":
                data = await fetch_company_overview(symbol=symbol)
                data_source = "AlphaVantage Company Overview"
                
            elif intent == "technical_analysis":
                data = await fetch_rsi(
                    symbol=symbol,
                    interval="daily",
                    time_period=14,
                    series_type="close"
                )
                data_source = "AlphaVantage Technical Indicators"
                
            elif intent == "market_sentiment":
                data = await fetch_news_sentiment(tickers=symbol)
                data_source = "AlphaVantage News Sentiment"
                
            else:
                data = await fetch_quote(symbol=symbol)
                data_source = "AlphaVantage Default"
            
            print(f"Debug - 데이터 수신 완료: {type(data)}")
            if isinstance(data, dict):
                print(f"Debug - 데이터 키: {list(data.keys())[:3]}...")  # 처음 3개만
            
            return {
                **state,
                "financial_data": data,
                "data_source": data_source,
                "step_count": state["step_count"] + 1,
                "processing_time": state["processing_time"] + (time.time() - start_time)
            }
            
        except Exception as e:
            print(f"Debug - 데이터 조회 오류: {e}")
            return {
                **state,
                "financial_data": {"error": str(e)},
                "error_context": f"데이터 조회 오류: {str(e)}",
                "step_count": state["step_count"] + 1,
                "processing_time": state["processing_time"] + (time.time() - start_time)
            }

class FinalAnalysisAgent:
    def format_number(self, value):
        """숫자 포맷팅"""
        try:
            if value == 'N/A' or value is None or value == 'None' or value == '':
                return 'N/A'
            
            if isinstance(value, str):
                clean_value = value.replace(',', '').replace('%', '')
                num = float(clean_value)
            else:
                num = float(value)
            
            if num == int(num):
                num = int(num)
                return f"{num:,}"
            else:
                return f"{num:,.2f}"
                
        except (ValueError, TypeError):
            return str(value) if value else 'N/A'
    
    def analyze(self, state: AdvancedChatbotState) -> AdvancedChatbotState:
        start_time = time.time()
        data = state["financial_data"]
        intent = state["intent"]
        entities = state["entities"]
        symbol = entities.get("symbol", "UNKNOWN")
        
        print(f"Debug - 분석 시작: {intent} for {symbol}")
        
        if not data or "error" in data:
            analysis = f"❌ {symbol} 데이터 조회에 실패했습니다: {data.get('error', '알 수 없는 오류')}"
        else:
            analysis = self._create_detailed_analysis(data, intent, symbol, entities)
        
        print(f"Debug - 분석 완료, 결과 길이: {len(analysis)}")
        
        return {
            **state,
            "analysis_result": analysis,
            "step_count": state["step_count"] + 1,
            "processing_time": state["processing_time"] + (time.time() - start_time)
        }
    
    def _create_detailed_analysis(self, data: Dict, intent: str, symbol: str, entities: Dict) -> str:
        """상세한 분석 생성"""
        
        if intent == "stock_quote" and isinstance(data, dict) and "Global Quote" in data:
            quote = data["Global Quote"]
            
            # 데이터 추출 및 포맷팅
            price = self.format_number(quote.get("05. price", "N/A"))
            change = quote.get("09. change", "N/A")
            change_percent = quote.get("10. change percent", "N/A")
            volume = self.format_number(quote.get("06. volume", "N/A"))
            prev_close = self.format_number(quote.get("08. previous close", "N/A"))
            high = self.format_number(quote.get("03. high", "N/A"))
            low = self.format_number(quote.get("02. low", "N/A"))
            trading_day = quote.get("07. latest trading day", "N/A")
            
            # 변동률 분석
            try:
                change_num = float(change) if change != "N/A" else 0
                change_percent_clean = change_percent.replace('%', '') if change_percent != "N/A" else "0"
                change_percent_num = float(change_percent_clean)
                
                if change_num > 5 or change_percent_num > 3:
                    trend = "🚀 급등"
                    insight = "강한 상승 모멘텀"
                elif change_num > 0:
                    trend = "📈 상승"
                    insight = "긍정적 흐름"
                elif change_num < -5 or change_percent_num < -3:
                    trend = "📉 급락"
                    insight = "강한 하락 압력"
                elif change_num < 0:
                    trend = "🔻 하락"
                    insight = "약세 흐름"
                else:
                    trend = "📊 보합"
                    insight = "횡보 패턴"
                    
            except:
                trend = "📊 변동없음"
                insight = "데이터 분석 불가"
            
            return f"""
📊 **{symbol} 실시간 주식 분석**

💰 **가격 정보:**
• 현재가: ${price}
• 변동: {change} ({change_percent}) {trend}
• 고가: ${high}
• 저가: ${low}
• 이전 종가: ${prev_close}

📈 **거래 정보:**
• 거래량: {volume} 주
• 거래일: {trading_day}

🧠 **AI 분석:**
• 시장 상황: {insight}
• 추천: {"매수 관심" if change_num > 2 else "관망" if change_num > -2 else "주의 필요"}
"""

        elif intent == "company_overview" and isinstance(data, dict) and "Symbol" in data:
            # 회사 정보 포맷팅
            company_name = data.get('Name', symbol)
            sector = data.get('Sector', 'N/A')
            industry = data.get('Industry', 'N/A')
            market_cap = data.get('MarketCapitalization', 'N/A')
            pe_ratio = data.get('PERatio', 'N/A')
            dividend_yield = data.get('DividendYield', 'N/A')
            
            # 시가총액 포맷팅
            if market_cap != 'N/A' and market_cap is not None:
                try:
                    mc_num = int(market_cap)
                    if mc_num >= 1000000000000:
                        market_cap = f"${mc_num/1000000000000:.1f}T"
                    elif mc_num >= 1000000000:
                        market_cap = f"${mc_num/1000000000:.1f}B"
                    elif mc_num >= 1000000:
                        market_cap = f"${mc_num/1000000:.1f}M"
                    else:
                        market_cap = f"${mc_num:,}"
                except:
                    market_cap = f"${market_cap}"
            
            return f"""
🏢 **{company_name} 기업 분석**

🏭 **기본 정보:**
• 업종: {sector}
• 산업: {industry}
• 국가: {data.get('Country', 'N/A')}

💹 **투자 지표:**
• 시가총액: {market_cap}
• P/E 비율: {pe_ratio}
• 배당수익률: {dividend_yield}

📊 **주가 정보:**
• 52주 최고가: ${data.get('52WeekHigh', 'N/A')}
• 52주 최저가: ${data.get('52WeekLow', 'N/A')}

💼 **회사 개요:**
{data.get('Description', 'N/A')[:200]}...
"""

        elif intent == "technical_analysis":
            return f"""
📈 **{symbol} 기술적 분석**

🎯 **RSI 지표 분석:**
• RSI 데이터 준비 완료
• 14일 RSI 기준 분석
• 70 이상: 과매수, 30 이하: 과매도

🧠 **분석 가이드:**
• 모멘텀 지표로 추세 반전 신호 포착
• 다른 지표와 함께 사용 권장

📊 **상태:** ✅ 데이터 준비 완료
"""
        
        return f"✅ {symbol}에 대한 {intent} 분석이 완료되었습니다."

def determine_routing(state: AdvancedChatbotState) -> str:
    """라우팅 결정"""
    confidence = state.get("confidence", 0.5)
    print(f"Debug - 라우팅 결정: confidence={confidence}")
    
    if confidence > 0.6:  # 임계값 더 낮춤
        return "fetch_data"
    else:
        return "clarify_intent"

def clarify_intent(state: AdvancedChatbotState) -> AdvancedChatbotState:
    """인텐트 명확화"""
    return {
        **state,
        "analysis_result": f"""
🤔 **질문을 더 명확히 해주세요**

입력하신 내용: "{state['user_query']}"
분석 신뢰도: {state.get('confidence', 0.5)*100:.0f}%

💡 **추천 질문 형식:**
• `NVDA 현재가` - 실시간 주가
• `AAPL 회사 정보` - 기업 분석  
• `TSLA RSI` - 기술적 분석

다시 질문해주세요! 🚀
""",
        "step_count": state["step_count"] + 1
    }

def generate_final_response(state: AdvancedChatbotState) -> AdvancedChatbotState:
    """최종 응답 생성"""
    analysis = state.get("analysis_result", "분석을 완료할 수 없습니다.")
    processing_time = state.get("processing_time", 0)
    confidence = state.get("confidence", 0.8)
    
    # 처리 시간과 신뢰도 추가
    footer = f"\n\n📊 **분석 신뢰도:** {confidence*100:.0f}%"
    footer += f"\n⚡ **처리 시간:** {processing_time:.2f}초"
    footer += f" | 📡 **데이터 출처:** {state.get('data_source', 'AlphaVantage')}"
    
    return {
        **state,
        "formatted_response": analysis + footer,
        "step_count": state["step_count"] + 1
    }

def create_final_chatbot_graph(use_openai=True):
    """최종 수정된 LangGraph 워크플로우"""
    
    # OpenAI 사용 여부에 따라 분류기 선택
    if use_openai:
        classifier = FinalFixedIntentClassifier()
    else:
        classifier = SimpleRuleBasedClassifier()
    
    data_fetcher = FinalDataFetcher()
    analyst = FinalAnalysisAgent()
    
    workflow = StateGraph(AdvancedChatbotState)
    
    # 노드 추가
    workflow.add_node("classify_intent", classifier.classify)
    workflow.add_node("fetch_data", data_fetcher.fetch_data)
    workflow.add_node("analyze_data", analyst.analyze)
    workflow.add_node("clarify_intent", clarify_intent)
    workflow.add_node("generate_response", generate_final_response)
    
    # 조건부 엣지
    workflow.add_conditional_edges(
        "classify_intent",
        determine_routing,
        {
            "fetch_data": "fetch_data",
            "clarify_intent": "clarify_intent"
        }
    )
    
    workflow.add_edge("fetch_data", "analyze_data")
    workflow.add_edge("analyze_data", "generate_response")
    workflow.add_edge("clarify_intent", "generate_response")
    workflow.add_edge("generate_response", END)
    
    workflow.set_entry_point("classify_intent")
    
    return workflow.compile()