from typing import TypedDict, List, Optional, Dict, Any

class ChatbotState(TypedDict):
    messages: List[Dict[str, str]]
    user_query: str
    intent: Optional[str]
    symbol: Optional[str]
    parameters: Dict[str, Any]
    financial_data: Optional[Dict[str, Any]]
    analysis_result: Optional[str]
    response: Optional[str]
    step_count: int