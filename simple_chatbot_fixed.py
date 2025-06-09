import os
import sys
import asyncio

# 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 직접 API 함수 임포트
from alphavantage_mcp_server.api import fetch_quote, fetch_company_overview

class SimpleChatbot:
    def __init__(self):
        self.api_key = "CS0LBSPNM72HSNQL"
    
    def get_stock_quote(self, symbol: str):
        """주식 시세 조회"""
        try:
            # API 키를 환경변수로 설정
            os.environ['ALPHAVANTAGE_API_KEY'] = self.api_key
            
            # apikey 파라미터 없이 호출
            result = fetch_quote(symbol=symbol)
            return result
        except Exception as e:
            print(f"Debug - fetch_quote 오류: {e}")
            return {"error": str(e)}
    
    def get_company_info(self, symbol: str):
        """회사 정보 조회"""
        try:
            # API 키를 환경변수로 설정
            os.environ['ALPHAVANTAGE_API_KEY'] = self.api_key
            
            # apikey 파라미터 없이 호출
            result = fetch_company_overview(symbol=symbol)
            return result
        except Exception as e:
            print(f"Debug - fetch_company_overview 오류: {e}")
            return {"error": str(e)}
    
    def chat(self, user_input: str) -> str:
        """간단한 채팅 처리"""
        user_input_lower = user_input.lower()
        user_input_upper = user_input.upper()
        
        # 간단한 키워드 매칭
        if any(word in user_input_lower for word in ["현재가", "시세", "가격", "quote", "price"]):
            # 심볼 추출
            import re
            symbols = re.findall(r'\b[A-Z]{2,5}\b', user_input_upper)
            symbol = symbols[0] if symbols else "AAPL"
            
            print(f"Debug - 주식 시세 조회: {symbol}")
            data = self.get_stock_quote(symbol)
            
            if "error" in data:
                return f"❌ {symbol} 데이터 조회 실패: {data['error']}"
            
            if "Global Quote" in data:
                quote = data["Global Quote"]
                price = quote.get("05. price", "N/A")
                change = quote.get("09. change", "N/A")
                change_percent = quote.get("10. change percent", "N/A")
                volume = quote.get("06. volume", "N/A")
                prev_close = quote.get("08. previous close", "N/A")
                
                return f"""
📊 {symbol} 주식 현재 정보:
• 현재가: ${price}
• 변동: {change} ({change_percent})
• 거래량: {volume}
• 이전 종가: ${prev_close}
"""
            else:
                return f"❌ {symbol} 데이터 형식 오류: {data}"
        
        elif any(word in user_input_lower for word in ["회사", "정보", "개요", "overview", "company"]):
            import re
            symbols = re.findall(r'\b[A-Z]{2,5}\b', user_input_upper)
            symbol = symbols[0] if symbols else "AAPL"
            
            print(f"Debug - 회사 정보 조회: {symbol}")
            data = self.get_company_info(symbol)
            
            if "error" in data:
                return f"❌ {symbol} 회사 정보 조회 실패: {data['error']}"
            
            if "Symbol" in data:
                return f"""
🏢 {data.get('Name', symbol)} 회사 정보:
• 업종: {data.get('Sector', 'N/A')}
• 산업: {data.get('Industry', 'N/A')}
• 시가총액: {data.get('MarketCapitalization', 'N/A')}
• P/E 비율: {data.get('PERatio', 'N/A')}
• 배당수익률: {data.get('DividendYield', 'N/A')}
• 52주 최고가: ${data.get('52WeekHigh', 'N/A')}
• 52주 최저가: ${data.get('52WeekLow', 'N/A')}
• 설명: {data.get('Description', 'N/A')[:200]}...
"""
            else:
                return f"❌ {symbol} 회사 데이터 형식 오류: {data}"
        
        else:
            return """
🤖 사용 가능한 명령어:
• "[심볼] 현재가" - 주식 시세 조회 
• "[심볼] 회사 정보" - 회사 개요

📝 예시:
• NVDA 현재가
• TSLA 회사 정보  
• AAPL 시세
• MSFT 개요

💡 팁: 주식 심볼(티커)을 대문자로 입력하세요!
"""

def main():
    print("🤖 Fixed AlphaVantage 챗봇 시작!")
    print("금융 데이터에 대해 질문해보세요. (종료: 'quit')")
    print("-" * 50)
    
    chatbot = SimpleChatbot()
    
    while True:
        try:
            user_input = input("\n💬 질문: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료']:
                print("챗봇을 종료합니다!")
                break
            
            if not user_input:
                continue
            
            print("🔍 처리 중...")
            response = chatbot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n챗봇을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 메인 오류: {e}")

if __name__ == "__main__":
    main()