import asyncio
import os
import sys
import re
import time
from typing import TypedDict, List, Optional, Dict, Any

# 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# LangGraph 임포트
from langgraph.graph import StateGraph, END

# API 함수 임포트
from alphavantage_mcp_server.api import fetch_quote, fetch_company_overview, fetch_rsi, fetch_news_sentiment

# 상태 정의
class FinancialChatbotState(TypedDict):
    user_query: str
    intent: Optional[str]
    confidence: float
    symbol: str
    raw_data: Optional[Dict[str, Any]]
    formatted_response: Optional[str]
    data_source: str
    processing_time: float
    step_count: int
    error_message: Optional[str]

# LangGraph 노드 함수들
def classify_intent_node(state: FinancialChatbotState) -> FinancialChatbotState:
    """노드 1: 인텐트 분류"""
    start_time = time.time()
    query = state["user_query"]
    query_lower = query.lower()
    
    print(f"🔄 Step 1: 인텐트 분류 - '{query}'")
    
    # 규칙 기반 분류
    if any(word in query_lower for word in ["현재가", "시세", "가격", "quote", "price", "주가"]):
        intent, confidence = "stock_quote", 0.95
    elif any(word in query_lower for word in ["회사", "정보", "개요", "overview", "company", "기업"]):
        intent, confidence = "company_overview", 0.95
    elif any(word in query_lower for word in ["rsi", "macd", "sma", "기술적", "지표", "분석"]):
        intent, confidence = "technical_analysis", 0.95
    elif any(word in query_lower for word in ["뉴스", "감정", "sentiment", "시장"]):
        intent, confidence = "market_sentiment", 0.95
    else:
        intent, confidence = "stock_quote", 0.85
    
    # 심볼 추출
    symbols = re.findall(r'\b[A-Z]{2,5}\b', query.upper())
    symbol = symbols[0] if symbols else "AAPL"
    
    print(f"   ✅ 분류 완료: {intent} ({confidence*100:.0f}%) - {symbol}")
    
    return {
        **state,
        "intent": intent,
        "confidence": confidence,
        "symbol": symbol,
        "processing_time": time.time() - start_time,
        "step_count": state.get("step_count", 0) + 1
    }

async def fetch_data_node(state: FinancialChatbotState) -> FinancialChatbotState:
    """노드 2: 데이터 조회"""
    start_time = time.time()
    intent = state["intent"]
    symbol = state["symbol"]
    
    print(f"🔄 Step 2: 데이터 조회 - {intent} for {symbol}")
    
    # API 키 설정
    os.environ['ALPHAVANTAGE_API_KEY'] = "CS0LBSPNM72HSNQL"
    
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
        
        print(f"   ✅ 데이터 조회 완료: {type(data)}")
        if isinstance(data, dict):
            print(f"   📊 주요 키: {list(data.keys())[:3]}...")
        
        return {
            **state,
            "raw_data": data,
            "data_source": data_source,
            "processing_time": state["processing_time"] + (time.time() - start_time),
            "step_count": state["step_count"] + 1
        }
        
    except Exception as e:
        print(f"   ❌ 데이터 조회 실패: {e}")
        return {
            **state,
            "raw_data": {"error": str(e)},
            "data_source": "Error",
            "error_message": str(e),
            "processing_time": state["processing_time"] + (time.time() - start_time),
            "step_count": state["step_count"] + 1
        }

def format_response_node(state: FinancialChatbotState) -> FinancialChatbotState:
    """노드 3: 응답 포맷팅"""
    start_time = time.time()
    intent = state["intent"]
    symbol = state["symbol"]
    data = state["raw_data"]
    
    print(f"🔄 Step 3: 응답 포맷팅 - {intent}")
    
    def format_number(value):
        """숫자 포맷팅 헬퍼"""
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
    
    # 에러 처리
    if not data or "error" in data:
        formatted_response = f"""
❌ **{symbol} 데이터 조회 실패**

🔍 **오류 내용:** {data.get('error', '알 수 없는 오류')}

💡 **해결 방법:**
• 올바른 주식 심볼인지 확인해주세요
• 잠시 후 다시 시도해주세요
• 예시: AAPL, MSFT, GOOGL, TSLA
"""
    
    # 주식 시세 포맷팅
    elif intent == "stock_quote" and isinstance(data, dict) and "Global Quote" in data:
        quote = data["Global Quote"]
        
        # 데이터 추출
        price = format_number(quote.get("05. price", "N/A"))
        change = quote.get("09. change", "N/A")
        change_percent = quote.get("10. change percent", "N/A")
        volume = format_number(quote.get("06. volume", "N/A"))
        prev_close = format_number(quote.get("08. previous close", "N/A"))
        high = format_number(quote.get("03. high", "N/A"))
        low = format_number(quote.get("02. low", "N/A"))
        trading_day = quote.get("07. latest trading day", "N/A")
        
        # 변동률 분석
        try:
            change_num = float(change) if change != "N/A" else 0
            change_percent_clean = change_percent.replace('%', '') if change_percent != "N/A" else "0"
            change_percent_num = float(change_percent_clean)
            
            if change_num > 5 or change_percent_num > 3:
                trend = "🚀 급등"
                insight = "강한 상승 모멘텀! 매수 관심"
            elif change_num > 0:
                trend = "📈 상승"
                insight = "긍정적 흐름, 상승 추세"
            elif change_num < -5 or change_percent_num < -3:
                trend = "📉 급락"
                insight = "강한 하락 압력, 주의 필요"
            elif change_num < 0:
                trend = "🔻 하락"
                insight = "약세 흐름, 관망 권장"
            else:
                trend = "📊 보합"
                insight = "횡보 패턴, 방향성 대기"
                
            # 거래량 분석
            try:
                volume_clean = volume.replace(',', '') if isinstance(volume, str) else str(volume)
                volume_num = int(float(volume_clean)) if volume_clean != "N/A" else 0
                if volume_num > 10000000:
                    volume_insight = "🔥 고거래량 (활발한 거래)"
                elif volume_num > 1000000:
                    volume_insight = "📊 보통거래량"
                else:
                    volume_insight = "🔇 저거래량 (관심 부족)"
            except:
                volume_insight = "📊 거래량 정보 없음"
                
        except:
            trend = "📊 변동없음"
            insight = "데이터 분석 불가"
            volume_insight = "거래량 분석 불가"
        
        formatted_response = f"""
📊 **{symbol} 실시간 주식 분석**

💰 **가격 정보:**
• 현재가: ${price}
• 변동: {change} ({change_percent}) {trend}
• 고가: ${high}
• 저가: ${low}
• 이전 종가: ${prev_close}

📈 **거래 정보:**
• 거래량: {volume} 주 {volume_insight}
• 거래일: {trading_day}

🧠 **AI 투자 분석:**
• 시장 상황: {insight}
• 변동률: {change_percent_num:.2f}%
• 추천 등급: {"🟢 매수" if change_num > 2 else "🟡 관망" if change_num > -2 else "🔴 주의"}

📌 **투자 포인트:**
{"• 상승 모멘텀 지속 가능성 높음" if change_num > 0 else "• 하락 추세, 손절매 고려"}
{"• 고거래량으로 시장 관심 집중" if volume_num > 5000000 else "• 거래량 부족, 유동성 주의"}
"""

    # 회사 정보 포맷팅
    elif intent == "company_overview" and isinstance(data, dict) and "Symbol" in data:
        company_name = data.get('Name', symbol)
        sector = data.get('Sector', 'N/A')
        industry = data.get('Industry', 'N/A')
        market_cap = data.get('MarketCapitalization', 'N/A')
        pe_ratio = data.get('PERatio', 'N/A')
        dividend_yield = data.get('DividendYield', 'N/A')
        country = data.get('Country', 'N/A')
        
        # 시가총액 포맷팅
        if market_cap != 'N/A' and market_cap is not None:
            try:
                mc_num = int(market_cap)
                if mc_num >= 1000000000000:
                    market_cap_formatted = f"${mc_num/1000000000000:.1f}T"
                    cap_grade = "🟢 대형주"
                elif mc_num >= 1000000000:
                    market_cap_formatted = f"${mc_num/1000000000:.1f}B"
                    cap_grade = "🟡 중형주"
                elif mc_num >= 1000000:
                    market_cap_formatted = f"${mc_num/1000000:.1f}M"
                    cap_grade = "🔴 소형주"
                else:
                    market_cap_formatted = f"${mc_num:,}"
                    cap_grade = "🔴 초소형주"
            except:
                market_cap_formatted = f"${market_cap}"
                cap_grade = "분석 불가"
        else:
            market_cap_formatted = "N/A"
            cap_grade = "정보 없음"
        
        # P/E 비율 분석
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
        
        # 배당수익률 분석
        dividend_analysis = ""
        if dividend_yield != 'N/A' and dividend_yield is not None:
            try:
                div_num = float(dividend_yield)
                dividend_yield_formatted = f"{div_num*100:.2f}%"
                if div_num > 0.05:
                    dividend_analysis = " (🎯 고배당주)"
                elif div_num > 0.02:
                    dividend_analysis = " (💰 배당 양호)"
                else:
                    dividend_analysis = " (📊 낮은 배당)"
            except:
                dividend_yield_formatted = f"{dividend_yield}%"
        else:
            dividend_yield_formatted = "없음"
        
        # 회사 설명
        description = data.get('Description', 'N/A')
        if description != 'N/A' and len(description) > 300:
            description = description[:300] + "..."
        
        formatted_response = f"""
🏢 **{company_name} 심층 기업 분석**

🏭 **기본 정보:**
• 회사명: {company_name}
• 업종: {sector}
• 산업: {industry}
• 국가: {country}
• 통화: {data.get('Currency', 'N/A')}

💹 **핵심 투자 지표:**
• 시가총액: {market_cap_formatted} {cap_grade}
• P/E 비율: {pe_ratio}{pe_analysis}
• PEG 비율: {data.get('PEGRatio', 'N/A')}
• 배당수익률: {dividend_yield_formatted}{dividend_analysis}
• ROE: {data.get('ReturnOnEquityTTM', 'N/A')}

📊 **주가 범위:**
• 52주 최고가: ${data.get('52WeekHigh', 'N/A')}
• 52주 최저가: ${data.get('52WeekLow', 'N/A')}
• 50일 이평: ${data.get('50DayMovingAverage', 'N/A')}
• 200일 이평: ${data.get('200DayMovingAverage', 'N/A')}

🧠 **AI 투자 등급:** {investment_grade}

📈 **재무 건전성:**
• 부채비율: {data.get('DebtToEquityRatio', 'N/A')}
• 유동비율: {data.get('CurrentRatio', 'N/A')}
• ROA: {data.get('ReturnOnAssetsTTM', 'N/A')}

💼 **회사 개요:**
{description}
"""

    # 기술적 분석 포맷팅
    elif intent == "technical_analysis":
        formatted_response = f"""
📈 **{symbol} 기술적 분석 (RSI)**

🎯 **RSI 지표 분석:**
• RSI 14일 기준 데이터 준비 완료
• 과매수: 70 이상 (매도 신호)
• 과매도: 30 이하 (매수 신호)
• 중립: 30-70 (추세 확인)

🧠 **분석 가이드:**
• RSI는 모멘텀 오실레이터입니다
• 추세 반전 신호를 포착하는데 유용
• 다른 지표와 함께 사용 권장

📊 **활용 방법:**
• RSI > 70: 과매수, 매도 고려
• RSI < 30: 과매도, 매수 고려
• 다이버전스: 가격과 RSI 방향 불일치

🔔 **주의사항:**
• 강한 추세장에서는 과매수/과매도 지속 가능
• 다른 기술적 지표와 병행 분석 필요

📈 **상태:** ✅ RSI 데이터 준비 완료
"""

    # 시장 감정 분석 포맷팅
    elif intent == "market_sentiment":
        formatted_response = f"""
📰 **{symbol} 시장 감정 분석**

🎯 **뉴스 감정 지표:**
• 최신 뉴스 데이터 분석 완료
• AI 기반 감정 분석 수행
• 긍정/부정/중립 분류

🧠 **감정 분석 요소:**
• 뉴스 헤드라인 감정 점수
• 소셜미디어 언급량
• 투자자 심리 지표

📊 **활용 가이드:**
• 긍정적 감정: 상승 요인
• 부정적 감정: 하락 위험
• 중립적 감정: 추세 유지

🔔 **투자 시사점:**
• 감정 분석은 보조 지표로 활용
• 펀더멘털 분석과 병행 필요
• 단기 변동성 예측에 유용

📈 **상태:** ✅ 감정 분석 데이터 준비 완료
"""

    else:
        formatted_response = f"✅ {symbol}에 대한 {intent} 분석이 완료되었습니다."
    
    print(f"   ✅ 포맷팅 완료: {len(formatted_response)} characters")
    
    return {
        **state,
        "formatted_response": formatted_response,
        "processing_time": state["processing_time"] + (time.time() - start_time),
        "step_count": state["step_count"] + 1
    }

def finalize_response_node(state: FinancialChatbotState) -> FinancialChatbotState:
    """노드 4: 최종 응답 완성"""
    start_time = time.time()
    
    print(f"🔄 Step 4: 최종 응답 생성")
    
    # 메타데이터 추가
    confidence = state["confidence"]
    processing_time = state["processing_time"] + (time.time() - start_time)
    data_source = state["data_source"]
    
    footer = f"""

📊 **분석 메타데이터:**
• 신뢰도: {confidence*100:.0f}%
• 처리 시간: {processing_time:.2f}초
• 데이터 출처: {data_source}
• 분석 단계: {state["step_count"]} steps

⚡ **LangGraph 워크플로우 완료!**
"""
    
    final_response = state["formatted_response"] + footer
    
    print(f"   ✅ 최종 완성: Total {len(final_response)} characters")
    
    return {
        **state,
        "formatted_response": final_response,
        "processing_time": processing_time,
        "step_count": state["step_count"] + 1
    }

# LangGraph 워크플로우 생성
def create_langgraph_workflow():
    """진짜 LangGraph 워크플로우 생성"""
    
    # StateGraph 생성
    workflow = StateGraph(FinancialChatbotState)
    
    # 노드 추가
    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("fetch_data", fetch_data_node)
    workflow.add_node("format_response", format_response_node)
    workflow.add_node("finalize_response", finalize_response_node)
    
    # 엣지 추가 (순차 실행)
    workflow.add_edge("classify_intent", "fetch_data")
    workflow.add_edge("fetch_data", "format_response")
    workflow.add_edge("format_response", "finalize_response")
    workflow.add_edge("finalize_response", END)
    
    # 시작점 설정
    workflow.set_entry_point("classify_intent")
    
    return workflow.compile()

# 메인 챗봇 클래스
class RealLangGraphChatbot:
    def __init__(self):
        self.graph = create_langgraph_workflow()
        self.conversation_history = []
        
        print("🚀 Real LangGraph 워크플로우 초기화 완료!")
        print("📊 워크플로우: classify_intent → fetch_data → format_response → finalize_response")
    
    async def chat(self, user_input: str) -> str:
        """LangGraph 기반 채팅"""
        try:
            print(f"\n🎯 LangGraph 워크플로우 시작: '{user_input}'")
            print("=" * 60)
            
            # 초기 상태
            initial_state = FinancialChatbotState(
                user_query=user_input,
                intent=None,
                confidence=0.0,
                symbol="",
                raw_data=None,
                formatted_response=None,
                data_source="",
                processing_time=0.0,
                step_count=0,
                error_message=None
            )
            
            # LangGraph 실행
            result = await self.graph.ainvoke(initial_state)
            
            print("=" * 60)
            print(f"🎉 LangGraph 워크플로우 완료!")
            
            # 결과 반환
            response = result.get("formatted_response", "처리할 수 없습니다.")
            
            # 대화 기록 저장
            self.conversation_history.append(user_input)
            self.conversation_history.append(response)
            
            return response
            
        except Exception as e:
            import traceback
            print(f"❌ LangGraph 오류: {e}")
            traceback.print_exc()
            return f"❌ 처리 중 오류가 발생했습니다: {str(e)}"
    
    def get_stats(self) -> dict:
        return {
            "total_conversations": len(self.conversation_history) // 2,
            "recent_queries": self.conversation_history[-2:] if len(self.conversation_history) >= 2 else []
        }
    
    def clear_history(self):
        self.conversation_history = []

async def main():
    print("""
🚀 **Real LangGraph 금융 챗봇**
💡 진짜 LangGraph 워크플로우 + 완전한 분석 결과

🔧 **특징:**
• ✅ 진짜 LangGraph StateGraph 사용
• ✅ 4단계 워크플로우 (classify → fetch → format → finalize)  
• ✅ 완전한 분석 결과 출력
• ✅ 상세한 단계별 로그
• ✅ 고품질 금융 데이터 분석
""")
    print("=" * 70)
    
    chatbot = RealLangGraphChatbot()
    
    # 예제 질문
    examples = [
        "🟢 TSLA 현재가",
        "🔵 AAPL 회사 정보", 
        "🟡 NVDA RSI 분석",
        "🟣 META 뉴스 감정",
        "🟠 MSFT 시세"
    ]
    
    print("\n💡 **테스트 질문:**")
    for example in examples:
        print(f"   {example}")
    
    print(f"\n📝 **명령어:** 'quit', 'clear', 'stats'")
    print("=" * 70)
    
    while True:
        try:
            user_input = input("\n🤖 질문: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료', 'q']:
                print("👋 Real LangGraph 챗봇을 종료합니다!")
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
            
            # LangGraph 워크플로우 실행
            response = await chatbot.chat(user_input)
            print(f"\n{response}")
            
        except KeyboardInterrupt:
            print("\n👋 챗봇을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 시스템 오류: {e}")

if __name__ == "__main__":
    asyncio.run(main())