import os
import sys
import asyncio
import re

# 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 비동기 API 함수 임포트
from alphavantage_mcp_server.api import fetch_quote, fetch_company_overview

class FixedAsyncChatbot:
    def __init__(self):
        self.api_key = "CS0LBSPNM72HSNQL"
        # 환경변수 설정
        os.environ['ALPHAVANTAGE_API_KEY'] = self.api_key
    
    def format_number(self, value):
        """숫자 포맷팅 (천 단위 구분 등)"""
        try:
            if value == 'N/A' or value is None or value == 'None':
                return 'N/A'
            
            # 문자열을 숫자로 변환 시도
            if isinstance(value, str):
                # 쉼표 제거 후 숫자 변환
                clean_value = value.replace(',', '')
                num = float(clean_value)
            else:
                num = float(value)
            
            # 정수인 경우 정수로 표시
            if num == int(num):
                num = int(num)
                return f"{num:,}"
            else:
                return f"{num:,.2f}"
                
        except (ValueError, TypeError):
            return str(value)
    
    async def get_stock_quote(self, symbol: str):
        """주식 시세 조회 (비동기)"""
        try:
            result = await fetch_quote(symbol=symbol)
            return result
        except Exception as e:
            print(f"Debug - fetch_quote 오류: {e}")
            return {"error": str(e)}
    
    async def get_company_info(self, symbol: str):
        """회사 정보 조회 (비동기)"""
        try:
            result = await fetch_company_overview(symbol=symbol)
            return result
        except Exception as e:
            print(f"Debug - fetch_company_overview 오류: {e}")
            return {"error": str(e)}
    
    async def chat(self, user_input: str) -> str:
        """비동기 채팅 처리"""
        user_input_lower = user_input.lower()
        user_input_upper = user_input.upper()
        
        # 심볼 추출
        symbols = re.findall(r'\b[A-Z]{2,5}\b', user_input_upper)
        symbol = symbols[0] if symbols else "AAPL"
        
        # 키워드 매칭
        if any(word in user_input_lower for word in ["현재가", "시세", "가격", "quote", "price"]):
            print(f"🔍 {symbol} 주식 시세 조회 중...")
            data = await self.get_stock_quote(symbol)
            
            if "error" in data:
                return f"❌ {symbol} 데이터 조회 실패: {data['error']}"
            
            if isinstance(data, dict) and "Global Quote" in data:
                quote = data["Global Quote"]
                price = quote.get("05. price", "N/A")
                change = quote.get("09. change", "N/A")
                change_percent = quote.get("10. change percent", "N/A")
                volume = quote.get("06. volume", "N/A")
                prev_close = quote.get("08. previous close", "N/A")
                high = quote.get("03. high", "N/A")
                low = quote.get("02. low", "N/A")
                trading_day = quote.get("07. latest trading day", "N/A")
                
                # 거래량 포맷팅 (안전하게)
                formatted_volume = self.format_number(volume)
                
                # 변동률에 따른 이모지
                try:
                    change_num = float(change) if change != "N/A" else 0
                    if change_num > 2:
                        trend = "🚀 강한 상승"
                    elif change_num > 0:
                        trend = "📈 상승"
                    elif change_num < -2:
                        trend = "📉 강한 하락"
                    elif change_num < 0:
                        trend = "🔻 하락"
                    else:
                        trend = "📊 보합"
                except:
                    trend = "📊 변동없음"
                
                return f"""
📊 **{symbol} 주식 현재 정보**

💰 **가격 정보:**
• 현재가: ${price}
• 변동: {change} ({change_percent}) {trend}
• 고가: ${high}
• 저가: ${low}
• 이전 종가: ${prev_close}

📈 **거래 정보:**
• 거래량: {formatted_volume} 주

⏰ **업데이트:** {trading_day}
"""
            else:
                return f"❌ {symbol} 데이터 형식 오류 또는 잘못된 심볼입니다."
        
        elif any(word in user_input_lower for word in ["회사", "정보", "개요", "overview", "company"]):
            print(f"🔍 {symbol} 회사 정보 조회 중...")
            data = await self.get_company_info(symbol)
            
            if "error" in data:
                return f"❌ {symbol} 회사 정보 조회 실패: {data['error']}"
            
            if isinstance(data, dict) and "Symbol" in data:
                # 시가총액 포맷팅
                market_cap = data.get('MarketCapitalization', 'N/A')
                if market_cap != 'N/A' and market_cap != 'None' and market_cap is not None:
                    try:
                        mc_num = int(market_cap)
                        if mc_num >= 1000000000:
                            market_cap = f"${mc_num/1000000000:.1f}B"
                        elif mc_num >= 1000000:
                            market_cap = f"${mc_num/1000000:.1f}M"
                        else:
                            market_cap = f"${mc_num:,}"
                    except:
                        market_cap = f"${market_cap}"
                
                # P/E 비율 분석
                pe_ratio = data.get('PERatio', 'N/A')
                pe_analysis = ""
                if pe_ratio != 'N/A' and pe_ratio != 'None' and pe_ratio is not None:
                    try:
                        pe_num = float(pe_ratio)
                        if pe_num < 15:
                            pe_analysis = " (저평가 가능)"
                        elif pe_num > 25:
                            pe_analysis = " (고평가 위험)"
                        else:
                            pe_analysis = " (적정 수준)"
                    except:
                        pass
                
                # 배당수익률 포맷팅
                dividend_yield = data.get('DividendYield', 'N/A')
                if dividend_yield != 'N/A' and dividend_yield != 'None' and dividend_yield is not None:
                    try:
                        div_num = float(dividend_yield)
                        dividend_yield = f"{div_num*100:.2f}%"
                    except:
                        dividend_yield = f"{dividend_yield}%"
                else:
                    dividend_yield = "없음"
                
                return f"""
🏢 **{data.get('Name', symbol)} 회사 정보**

🏭 **기본 정보:**
• 업종: {data.get('Sector', 'N/A')}
• 산업: {data.get('Industry', 'N/A')}
• 국가: {data.get('Country', 'N/A')}
• 통화: {data.get('Currency', 'N/A')}

💹 **투자 지표:**
• 시가총액: {market_cap}
• P/E 비율: {pe_ratio}{pe_analysis}
• PEG 비율: {data.get('PEGRatio', 'N/A')}
• 배당수익률: {dividend_yield}

📊 **주가 정보:**
• 52주 최고가: ${data.get('52WeekHigh', 'N/A')}
• 52주 최저가: ${data.get('52WeekLow', 'N/A')}
• 50일 이평: ${data.get('50DayMovingAverage', 'N/A')}
• 200일 이평: ${data.get('200DayMovingAverage', 'N/A')}

💼 **회사 설명:**
{data.get('Description', 'N/A')[:300]}...
"""
            else:
                return f"❌ {symbol} 회사 데이터를 찾을 수 없습니다."
        
        else:
            return f"""
🤖 **AlphaVantage 챗봇 사용법**

📝 **명령어:**
• **"[심볼] 현재가"** - 실시간 주식 시세
• **"[심볼] 회사 정보"** - 회사 개요 및 재무지표

💡 **예시 질문:**
• `NVDA 현재가` - 엔비디아 현재 주가
• `TSLA 시세` - 테슬라 주식 정보  
• `AAPL 회사 정보` - 애플 회사 개요
• `MSFT 개요` - 마이크로소프트 정보

🎯 **팁:** 
• 주식 심볼을 대문자로 입력하세요
• 미국 주식 심볼을 사용하세요 (NASDAQ, NYSE 등)
• 종료하려면 'quit'를 입력하세요

현재 입력하신 내용: "{user_input}"
위 형식으로 다시 질문해보세요! 🚀
"""

async def main():
    print("🚀 Fixed AlphaVantage 챗봇!")
    print("실시간 금융 데이터 조회")
    print("=" * 50)
    
    chatbot = FixedAsyncChatbot()
    
    # 환영 메시지
    print("""
💡 **테스트 질문:**
• NVDA 현재가
• AAPL 시세  
• TSLA 회사 정보
• MSFT 개요

종료: 'quit'
""")
    
    while True:
        try:
            user_input = input("\n💬 질문: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료', 'q']:
                print("👋 챗봇을 종료합니다!")
                break
            
            if not user_input:
                print("❓ 질문을 입력해주세요.")
                continue
            
            response = await chatbot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 챗봇을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())