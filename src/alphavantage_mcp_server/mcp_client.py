import os
import sys
import json
from typing import Dict, Any, Optional

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

class AlphaVantageMCPClient:
    """AlphaVantage MCP 서버와 통신하는 클라이언트"""
    
    def __init__(self):
        self.api_key = "IZLU4YURP1R1YVYW"
    
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """MCP 도구 호출"""
        try:
            # 상대 임포트로 api 모듈 가져오기
            from . import api
            
            # 도구명에 따른 함수 매핑
            tool_mapping = {
                "stock_quote": api.fetch_quote,
                "company_overview": api.fetch_company_overview,
                "rsi": api.fetch_rsi,
                "macd": api.fetch_macd,
                "sma": api.fetch_sma,
                "ema": api.fetch_ema,
                "time_series_daily": api.fetch_time_series_daily,
                "news_sentiment": api.fetch_news_sentiment,
                "intraday": api.fetch_intraday,
                "earnings": api.fetch_earnings,
                "balance_sheet": api.fetch_balance_sheet,
                "income_statement": api.fetch_income_statement,
                "fx_daily": api.fetch_fx_daily,
                "crypto_daily": api.fetch_digital_currency_daily,
            }
            
            func = tool_mapping.get(tool_name)
            if func:
                # API 키를 파라미터에 추가
                params['apikey'] = self.api_key
                result = func(**params)
                return result
            else:
                return {"error": f"도구 '{tool_name}'을 찾을 수 없습니다."}
                
        except Exception as e:
            return {"error": f"MCP 호출 중 오류: {str(e)}"}