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
            result = fetch_quote(symbol=symbol, apikey=self.api_key)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def get_company_info(self, symbol: str):
        """회사 정보 조회"""
        try:
            result = fetch_company_overview(symbol=symbol, apikey=self.api_key)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def chat(self, user_input: str) -> str:
        """간단한 채팅 처리"""
        user_input = user_input.upper()
        
        # 간단한 키워드 매칭
        if "현재가" in user_input or "시세" in user_input or "가격" in user_input:
            # 심볼 추출
            import re
            symbols = re.findall(r'\b[A-Z]{2,5}\b', user_input)
            symbol = symbols[0] if symbols else "AAPL"
            
            data = self.get_stock_quote(symbol)
            
            if "error" in data:
                return f"❌ {symbol} 데이터 조회 실패: {data['error']}"
            
            if "Global Quote" in data:
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
        
        elif "회사" in user_input or "정보" in user_input or "개요" in user_input:
            import re
            symbols = re.findall(r'\b[A-Z]{2,5}\b', user_input)
            symbol = symbols[0] if symbols else "AAPL"
            
            data = self.get_company_info(symbol)
            
            if "error" in data:
                return f"❌ {symbol} 회사 정보 조회 실패: {data['error']}"
            
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
        
        else:
            return """
사용 가능한 명령어:
• "[심볼] 현재가" - 주식 시세 조회 (예: AAPL 현재가)
• "[심볼] 회사 정보" - 회사 개요 (예: TSLA 회사 정보)

예시: AAPL 현재가, MSFT 회사 정보
"""

def main():
    print("🤖 Simple AlphaVantage 챗봇 시작!")
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
            print(f"❌ 오류: {e}")

if __name__ == "__main__":
    main()