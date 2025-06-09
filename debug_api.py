import os
import sys

# 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# API 함수 확인
from alphavantage_mcp_server.api import fetch_quote, fetch_company_overview
import inspect

def debug_api_functions():
    print("=== API 함수 시그니처 확인 ===")
    
    # fetch_quote 함수 시그니처
    print("fetch_quote:")
    print(f"  시그니처: {inspect.signature(fetch_quote)}")
    print(f"  독스트링: {fetch_quote.__doc__}")
    
    print("\nfetch_company_overview:")
    print(f"  시그니처: {inspect.signature(fetch_company_overview)}")
    print(f"  독스트링: {fetch_company_overview.__doc__}")
    
    # 테스트 호출
    print("\n=== 테스트 호출 ===")
    
    # 환경변수 설정
    os.environ['ALPHAVANTAGE_API_KEY'] = "CS0LBSPNM72HSNQL"
    
    try:
        print("fetch_quote('AAPL') 테스트...")
        result = fetch_quote(symbol="AAPL")
        print(f"결과 타입: {type(result)}")
        print(f"결과 키: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
    except Exception as e:
        print(f"fetch_quote 오류: {e}")
    
    try:
        print("\nfetch_company_overview('AAPL') 테스트...")
        result = fetch_company_overview(symbol="AAPL")
        print(f"결과 타입: {type(result)}")
        print(f"결과 키: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
    except Exception as e:
        print(f"fetch_company_overview 오류: {e}")

if __name__ == "__main__":
    debug_api_functions()