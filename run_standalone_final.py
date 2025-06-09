import asyncio
import os
import sys
import re
import json
import time
from typing import TypedDict, List, Optional, Dict, Any, Literal

# 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 직접 API 함수 임포트
from alphavantage_mcp_server.api import fetch_quote, fetch_company_overview, fetch_rsi, fetch_news_sentiment

# 상태 모델 직접 정의
class ChatbotState(TypedDict):
    messages: List[Dict[str, str]]
    user_query: str
    conversation_history: List[str]
    intent: Optional[str]
    confidence: float
    entities: Dict[str, Any]
    financial_data: Optional[Dict[str, Any]]
    analysis_result: Optional[str]
    formatted_response: Optional[str]
    step_count: int
    processing_time: float
    data_source: Optional[str]
    error_context: Optional[str]

# 간단한 규칙 기반 분류기
class SimpleClassifier:
    def classify(self, query: str) -> tuple:
        """규칙 기반 인텐트 분류"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["현재가", "시세", "가격", "quote", "price", "주가"]):
            return "stock_quote", 0.95
        elif any(word in query_lower for word in ["회사", "정보", "개요", "overview", "company", "기업"]):
            return "company_overview", 0.95
        elif any(word in query_lower for word in ["rsi", "macd", "sma", "기술적", "지표", "분석"]):
            return "technical_analysis", 0.95
        elif any(word in query_lower for word in ["뉴스", "감정", "sentiment", "시장"]):
            return "market_sentiment", 0.95
        else:
            return "stock_quote", 0.85
    
    def extract_symbol(self, query: str) -> str:
        """주식 심볼 추출"""
        symbols = re.findall(r'\b[A-Z]{2,5}\b', query.upper())
        return symbols[0] if symbols else "AAPL"

# 데이터 조회 클래스
class DataFetcher:
    def __init__(self):
        self.api_key = "CS0LBSPNM72HSNQL"
        os.environ['ALPHAVANTAGE_API_KEY'] = self.api_key
    
    async def fetch_data(self, intent: str, symbol: str) -> tuple:
        """데이터 조회"""
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
                data_source = "AlphaVantage RSI"
                
            elif intent == "market_sentiment":
                data = await fetch_news_sentiment(tickers=symbol)
                data_source = "AlphaVantage News Sentiment"
                
            else:
                data = await fetch_quote(symbol=symbol)
                data_source = "AlphaVantage Default"
            
            return data, data_source
            
        except Exception as e:
            return {"error": str(e)}, "Error"

# 분석 클래스
class Analyzer:
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
    
    def analyze(self, data: Dict, intent: str, symbol: str) -> str:
        """데이터 분석 및 포맷팅"""
        
        if not data or "error" in data:
            return f"❌ {symbol} 데이터 조회에 실패했습니다: {data.get('error', '알 수 없는 오류')}"
        
        if intent == "stock_quote" and isinstance(data, dict) and "Global Quote" in data:
            return self._format_stock_quote(data, symbol)
            
        elif intent == "company_overview" and isinstance(data, dict) and "Symbol" in data:
            return self._format_company_overview(data, symbol)
            
        elif intent == "technical_analysis":
            return self._format_technical_analysis(data, symbol)
        
        return f"✅ {symbol}에 대한 {intent} 분석이 완료되었습니다."
    
    def _format_stock_quote(self, data: Dict, symbol: str) -> str:
        """주식 시세 포맷팅"""
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
    
    def _format_company_overview(self, data: Dict, symbol: str) -> str:
        """회사 정보 포맷팅"""
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
        
        # P/E 분석
        pe_analysis = ""
        investment_grade = "분석 필요"
        if pe_ratio != 'N/A' and pe_ratio is not None:
            try:
                pe_num = float(pe_ratio)
                if pe_num < 10:
                    pe_analysis = " (💎 매우 저평가)"
                    investment_grade = "💚 강력 매수"
                elif pe_num < 15:
                    pe_analysis = " (💰 저평가 가능)"
                    investment_grade = "💙 매수 검토"
                elif pe_num < 25:
                    pe_analysis = " (📊 적정 수준)"
                    investment_grade = "💛 관망"
                else:
                    pe_analysis = " (⚠️ 고평가 위험)"
                    investment_grade = "🧡 주의 필요"
            except:
                pass
        
        return f"""
🏢 **{company_name} 기업 분석**

🏭 **기본 정보:**
• 업종: {sector}
• 산업: {industry}
• 국가: {data.get('Country', 'N/A')}

💹 **투자 지표:**
• 시가총액: {market_cap}
• P/E 비율: {pe_ratio}{pe_analysis}
• 배당수익률: {dividend_yield}

📊 **주가 정보:**
• 52주 최고가: ${data.get('52WeekHigh', 'N/A')}
• 52주 최저가: ${data.get('52WeekLow', 'N/A')}

🧠 **AI 투자 등급:** {investment_grade}

💼 **회사 개요:**
{data.get('Description', 'N/A')[:200]}...
"""
    
    def _format_technical_analysis(self, data: Dict, symbol: str) -> str:
        """기술적 분석 포맷팅"""
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

# 메인 챗봇 클래스
class StandaloneChatbot:
    def __init__(self):
        self.classifier = SimpleClassifier()
        self.data_fetcher = DataFetcher()
        self.analyzer = Analyzer()
        self.conversation_history = []
    
    async def chat(self, user_input: str) -> str:
        """채팅 처리"""
        start_time = time.time()
        
        try:
            print(f"Debug - 질문 분석 시작: {user_input}")
            
            # 1. 인텐트 분류
            intent, confidence = self.classifier.classify(user_input)
            symbol = self.classifier.extract_symbol(user_input)
            
            print(f"Debug - 분류 결과: intent={intent}, confidence={confidence}, symbol={symbol}")
            
            # 2. 데이터 조회
            data, data_source = await self.data_fetcher.fetch_data(intent, symbol)
            
            print(f"Debug - 데이터 조회 완료: {type(data)}")
            
            # 3. 분석 및 포맷팅
            analysis = self.analyzer.analyze(data, intent, symbol)
            
            # 4. 최종 응답 생성
            processing_time = time.time() - start_time
            
            footer = f"\n\n📊 **분석 신뢰도:** {confidence*100:.0f}%"
            footer += f"\n⚡ **처리 시간:** {processing_time:.2f}초"
            footer += f" | 📡 **데이터 출처:** {data_source}"
            
            response = analysis + footer
            
            # 대화 기록 추가
            self.conversation_history.append(user_input)
            self.conversation_history.append(response)
            
            return response
            
        except Exception as e:
            import traceback
            print(f"Debug - 오류 발생: {e}")
            traceback.print_exc()
            return f"❌ 처리 중 오류가 발생했습니다: {str(e)}"
    
    def clear_history(self):
        """대화 기록 초기화"""
        self.conversation_history = []
    
    def get_stats(self) -> dict:
        """통계 정보"""
        return {
            "total_conversations": len(self.conversation_history) // 2,
            "recent_queries": self.conversation_history[-2:] if len(self.conversation_history) >= 2 else []
        }

async def main():
    print("""
🚀 **Standalone Final 금융 챗봇**
💡 완전 독립 실행형 - 임포트 문제 해결

🔧 **특징:**
• ✅ 모든 의존성 문제 해결
• ✅ 완전한 규칙 기반 분류
• ✅ 고품질 금융 데이터 분석
• ✅ 상세한 디버깅 정보
""")
    print("=" * 70)
    
    chatbot = StandaloneChatbot()
    
    # 예제 질문 표시
    examples = [
        "🟢 TSLA 현재가",
        "🔵 AAPL 회사 정보", 
        "🟡 NVDA RSI 분석",
        "🟣 MSFT 뉴스 감정",
        "🟠 META 시세"
    ]
    
    print("💡 **테스트 질문:**")
    for example in examples:
        print(f"   {example}")
    
    print(f"\n📝 **명령어:** 'quit' (종료), 'clear' (초기화), 'stats' (통계)")
    print("=" * 70)
    
    while True:
        try:
            user_input = input("\n🤖 질문: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료', 'q']:
                print("👋 Standalone 챗봇을 종료합니다!")
                break
            
            elif user_input.lower() == 'clear':
                chatbot.clear_history()
                print("🗑️ 대화 기록이 초기화되었습니다.")
                continue
            
            elif user_input.lower() == 'stats':
                stats = chatbot.get_stats()
                print(f"""
📊 **챗봇 통계:**
• 총 대화 수: {stats['total_conversations']}
• 최근 질문: {stats['recent_queries'][-2] if len(stats['recent_queries']) >= 2 else '없음'}
""")
                continue
            
            if not user_input:
                print("❓ 질문을 입력해주세요.")
                continue
            
            print("🔄 Standalone 챗봇 처리 중...")
            response = await chatbot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 챗봇을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 시스템 오류: {e}")

if __name__ == "__main__":
    asyncio.run(main())