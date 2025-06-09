from typing import TypedDict, List, Optional, Dict, Any, Literal

class AdvancedChatbotState(TypedDict):
    # 대화 관리
    messages: List[Dict[str, str]]
    user_query: str
    conversation_history: List[str]
    
    # 인텐트 및 엔티티
    intent: Optional[Literal["stock_quote", "company_overview", "technical_analysis", "market_sentiment", "portfolio_analysis"]]
    confidence: float
    entities: Dict[str, Any]  # symbol, timeframe, indicators 등
    
    # 데이터 및 분석
    financial_data: Optional[Dict[str, Any]]
    analysis_result: Optional[str]
    formatted_response: Optional[str]
    
    # 메타데이터
    step_count: int
    processing_time: float
    data_source: Optional[str]
    error_context: Optional[str]